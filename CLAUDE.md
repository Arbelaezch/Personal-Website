# Personal-Website: rules for AI sessions

Django 5.2 LTS site for christiandonovan.ca (portfolio with case studies, films, recipes) plus a read-only public recipes API used by
the family-food Next.js app (separate repo). Runs on an on-prem Ubuntu server; **the server runbook is `devops.txt`**, the
live server config is versioned in `deploy/`. The GitHub issues are the roadmap; issues labelled `todo` are next.

## Commands
- Set up: `python3 -m venv env && env/bin/pip install -r requirements-dev.txt` (Python 3.12+), copy `website/website/.env.example`
  to `website/website/.env` (use `DEBUG=1` locally)
- All CI checks, no `.env` or MySQL needed: `scripts/test.sh` (migrations check, `check --deploy`, tests)
- Tests with coverage: `cd website && coverage run manage.py test && coverage report`
- Django lives in `website/`: run `manage.py` from there

## Frontend (redesigned 2026/11, tracking issue #106)
- Every public page extends `website/templates/base.html` (one nav, one footer). Design tokens and shared components are
  in `website/static/css/site.css`; each app's CSS holds only page-specific rules. Dark theme only. Fonts are self-hosted.
- No frontend framework and no build step: plain CSS and ES modules served by WhiteNoise. No inline `<script>`, inline
  `<style>` or event-handler attributes on public pages (a Content-Security-Policy is sent; `CSP_MODE` in settings).
- Home page: `portfolio/js/featured.js` owns which featured project is selected; `portfolio/js/orbit.js` is the tethered
  orbit, ported from `docs/design/orbit-prototype.html`. Keep its physics constants unless the owner asks. The page must
  keep working without JavaScript.
- Content that is not code: projects are featured, published and written up in the admin. `manage.py load_portfolio_content`
  holds the first drafts and only fills empty fields. `manage.py sync_github` (daily systemd timer) refreshes projects and
  the pipeline panel from GitHub and never overwrites hand-written fields.
- The resume is uploaded in the admin and served at `/resume/`. It is never committed (`docs/career/` is ignored).

## Rules
- Branch from `main`, open a PR, never push to `main`. Merging deploys production (health check + automatic code rollback).
  The owner merges PRs in the browser; workflow-file PRs cannot be merged by an agent token.
- Migrations are tracked: a model change needs its migration, and it must work with the previous release's code
  (rollback does not undo the database).
- Dependencies: exact pins, releases at least 14 days old that still carry the security fixes. Stay on Django 5.2 LTS until
  MySQL is 8.4+ (issue #80).
- The public API is read-only. Never test write methods (DELETE/PUT/PATCH/POST) against real records, use a made-up slug.
- Show stored rich text with `|safe` only for admin-authored content (`website.fields.RichTextField`).
- Anything that connects to the server uses the DNS name (the home IP is dynamic).
- Removing a static file from the source does NOT remove it from the server (`collectstatic` never deletes): delete by hand
  and restart gunicorn.
- Changes to `deploy/` are applied by hand on the server (`deploy/nginx/install.sh`, units, Docker); test them first and keep
  the security properties documented in `devops.txt`.
- No secrets, `.env`, backups or personal data in commits. Dates are written YYYY/MM/DD, units are metric.

## Verifying a change like the previous work did
Beyond the tests: run the exact CI sequence, then for risky changes a throwaway venv on the server (Python 3.12, real MySQL,
read-only) and a crawl of the public URLs compared with the live site, plus a real-browser check when JavaScript is involved.
