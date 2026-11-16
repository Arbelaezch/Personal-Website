"""Read-only sync from the public GitHub API (issue #102).

Two independent sections, each all-or-nothing:
  projects  repositories tagged with the "portfolio" topic become Project rows; linked projects
            get their GitHub description and last-activity date refreshed
  pipeline  recently merged pull requests, open pull requests and open "todo" issues of the
            repositories in settings.PIPELINE_REPOS, for the "How I ship with AI" panel

Only outbound HTTPS GET requests to api.github.com. Text from GitHub is stored as plain text and
must be rendered escaped.
"""
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import PipelineItem, Project, SyncState

API = 'https://api.github.com'
TOPIC = 'portfolio'
TIMEOUT = 10        # seconds per request
PER_PAGE = 100
MAX_PAGES = 10
MERGED_SHOWN = 10


class GitHubError(Exception):
    """The API could not be read. The caller leaves its section of the database untouched."""


def get(path, **params):
    """One GET of a JSON document from the GitHub API."""
    url = f'{API}{path}?{urllib.parse.urlencode(params)}'
    headers = {
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
        'User-Agent': 'christiandonovan.ca portfolio sync',
    }
    if settings.GITHUB_TOKEN:
        headers['Authorization'] = f'Bearer {settings.GITHUB_TOKEN}'
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        raise GitHubError(f'GitHub answered {error.code} for {path}') from None
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise GitHubError(f'could not reach GitHub for {path}: {error}') from None
    except ValueError:
        raise GitHubError(f'GitHub sent something that is not JSON for {path}') from None


def get_all(path, **params):
    """Every page of a list endpoint."""
    items = []
    for page in range(1, MAX_PAGES + 1):
        batch = get(path, per_page=PER_PAGE, page=page, **params)
        if not isinstance(batch, list):
            raise GitHubError(f'expected a list from {path}')
        items.extend(batch)
        if len(batch) < PER_PAGE:
            return items
    raise GitHubError(f'{path} has more than {MAX_PAGES * PER_PAGE} entries')


def parse_time(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')) if value else None


def title_from_repo(name):
    """"nba-draft-simulator" -> "Nba Draft Simulator"; words that already have capitals are kept ("FHIR")."""
    words = name.replace('_', '-').split('-')
    return ' '.join(word if word != word.lower() else word.capitalize() for word in words if word)


def clip(text, field):
    return (text or '')[:Project._meta.get_field(field).max_length]


def sync_projects(log, dry_run=False):
    """Create and refresh projects from the owner's public repositories. Returns True on success."""
    try:
        repos = get_all(f'/users/{settings.GITHUB_USER}/repos', type='owner', sort='pushed')
    except GitHubError as error:
        log(f'projects: FAILED, nothing changed: {error}')
        return False

    by_name = {repo['full_name'].lower(): repo for repo in repos if not repo.get('private')}
    tagged = {name for name, repo in by_name.items() if TOPIC in repo.get('topics', []) and not repo.get('fork')}

    with transaction.atomic():
        linked = {project.github_repo.lower(): project for project in Project.objects.exclude(github_repo=None)}

        # 1. Refresh what GitHub knows about every linked project, however it was created.
        for name, project in linked.items():
            repo = by_name.get(name)
            if repo is None:
                if project.created_by_sync and project.is_published and not project.description:
                    project.is_published = False
                    project.save(update_fields=['is_published'])
                    log(f'projects: unpublished {project.title} ({project.github_repo} is gone or private)')
                else:
                    log(f'projects: warning: {project.github_repo} is not a public repository any more; {project.title} left as it is')
                continue
            changed = []
            values = {
                'github_description': clip(repo.get('description'), 'github_description'),
                'github_pushed_at': parse_time(repo.get('pushed_at')),
            }
            if not project.primary_language and repo.get('language'):
                # only when empty: a language set by hand ("React Native") is kept
                values['primary_language'] = clip(repo['language'], 'primary_language')
            for field, value in values.items():
                if getattr(project, field) != value:
                    setattr(project, field, value)
                    changed.append(field)
            if project.created_by_sync and name not in tagged and project.is_published and not project.description:
                project.is_published = False
                changed.append('is_published')
                log(f'projects: unpublished {project.title} (the "{TOPIC}" topic was removed)')
            if changed:
                project.save(update_fields=changed)
                log(f'projects: updated {project.title}: {", ".join(changed)}')

        # 2. A tagged repository with no project yet becomes one.
        for name in sorted(tagged - set(linked)):
            repo = by_name[name]
            project = Project.objects.create(
                title=title_from_repo(repo['name']),
                github_repo=repo['full_name'],
                github_url=repo['html_url'],
                github_description=clip(repo.get('description'), 'github_description'),
                github_pushed_at=parse_time(repo.get('pushed_at')),
                primary_language=clip(repo.get('language'), 'primary_language'),
                created_by_sync=True,
            )
            log(f'projects: created {project.title} (/project/{project.slug}/) from {repo["full_name"]}')

        if dry_run:
            transaction.set_rollback(True)
        else:
            SyncState.mark('projects')
    log(f'projects: ok, {len(by_name)} public repositories, {len(tagged)} tagged "{TOPIC}"')
    return True


def pipeline_rows(repo):
    """What the panel shows for one repository, as unsaved PipelineItem objects."""
    closed = get(f'/repos/{repo}/pulls', state='closed', sort='updated', direction='desc', per_page=50)
    opened = get(f'/repos/{repo}/pulls', state='open', per_page=50)
    issues = get(f'/repos/{repo}/issues', state='open', labels='todo', per_page=50)
    for payload in (closed, opened, issues):
        if not isinstance(payload, list):
            raise GitHubError(f'expected a list for {repo}')

    merged = sorted((pull for pull in closed if pull.get('merged_at')), key=lambda pull: pull['merged_at'], reverse=True)
    rows = []
    for pull in merged[:MERGED_SHOWN]:
        rows.append(PipelineItem(kind=PipelineItem.PULL, state=PipelineItem.MERGED, merged_at=parse_time(pull['merged_at']), **common(repo, pull)))
    for pull in opened:
        rows.append(PipelineItem(kind=PipelineItem.PULL, state=PipelineItem.OPEN, **common(repo, pull)))
    for issue in issues:
        if 'pull_request' not in issue:  # the issues endpoint also lists pull requests
            rows.append(PipelineItem(kind=PipelineItem.ISSUE, state=PipelineItem.OPEN, **common(repo, issue)))
    return rows


def common(repo, item):
    return {
        'repo': repo,
        'number': item['number'],
        'title': (item.get('title') or '')[:PipelineItem._meta.get_field('title').max_length],
        'url': item['html_url'],
        'updated_at': parse_time(item.get('updated_at')) or timezone.now(),
    }


def sync_pipeline(log, dry_run=False):
    """Replace the pipeline activity with what GitHub shows now. Returns True on success."""
    try:
        rows = [row for repo in settings.PIPELINE_REPOS for row in pipeline_rows(repo)]
    except (GitHubError, KeyError, TypeError) as error:
        log(f'pipeline: FAILED, nothing changed: {error!r}')
        return False

    with transaction.atomic():
        PipelineItem.objects.all().delete()
        PipelineItem.objects.bulk_create(rows)
        if dry_run:
            transaction.set_rollback(True)
        else:
            SyncState.mark('pipeline')
    merged = sum(row.state == PipelineItem.MERGED for row in rows)
    log(f'pipeline: ok, {merged} merged, {len(rows) - merged} open, from {", ".join(settings.PIPELINE_REPOS)}')
    return True
