"""First drafts of the case studies for the featured projects that had no write-up (#104).

Every statement comes from the project's own README or status notes as of 2026/11/16. The owner
edits them in the admin; load_portfolio_content only fills sections that are still empty.
"""

SOFTWARE_FACTORY = {
    'problem': """
<p>Coding agents are strong in a single session, but they do not behave like a team. They grade their own work, they run unattended next to <code>git push</code>, and they give you no data on what each step cost or whether it worked.</p>
""",
    'description': """
<p>Harness is a plugin for Claude Code that turns one session into an engineering manager. It hands each part of the work to a specialised agent: scouts map the code, a planner writes the plan, engineers implement one task at a time, a reviewer from a different lab reviews the diff, and a verifier checks every finding against the real code.</p>
<p>Everything that should not be left to a language model lives in one Python command-line tool of about 2,900 lines that uses only the standard library: run state, branching, test gates, cost accounting, the decision to loop back or finish, and posting to GitHub. It works on single repositories and on workspaces of several, such as an API with a mobile client.</p>
""",
    'ai_usage': """
<p>Each stage uses the model that suits it. Scouts run on a small, fast model, one per repository, in parallel. The planner uses the strongest model. Engineers use a mid-sized one and move up for hard tasks. The reviewer is deliberately a model from a different lab, so it is less likely to share the engineer's blind spots; any OpenAI-compatible API can fill that role.</p>
<p>The manager session passes file paths between stages and never reads diffs or source itself, which keeps its context small over long runs.</p>
""",
    'safety': """
<ul>
<li><strong>A human approves the plan</strong> before any code is written.</li>
<li><strong>Agents cannot push.</strong> A hook parses every shell command. Subagents can never push, rewrite history or write to GitHub.</li>
<li><strong>Test gates know the baseline.</strong> Failures that existed before the change are recorded first, so a gate fails only on new ones, and an engineer cannot finish while a file it edited has no passing run on the current code.</li>
<li><strong>Tests are protected.</strong> Removed assertions, skips and loosened thresholds in existing tests are flagged, and the verifier has to judge each one.</li>
<li><strong>Reviews stay pending.</strong> Reviews posted to GitHub go up as drafts that I submit myself.</li>
</ul>
""",
    'results': """
<p>I use it daily on real projects. Every stage logs tokens, cost, duration and outcome, and a report breaks cost, quality and speed down by stage and model, so I can measure whether the pipeline is helping.</p>
<p>Court Vision, also on this site, was built with it from a design document.</p>
""",
    'lessons_learned': """
<ul>
<li>Keep the core deterministic and put the agents at the edges.</li>
<li>The agent that writes the code should never be the one that reviews it.</li>
<li>Python (standard library only), Claude Code plugins and hooks, OpenAI-compatible reviewer APIs, GitHub CLI.</li>
</ul>
""",
}

COURT_VISION = {
    'problem': """
<p>People who have never played basketball rarely learn where to move, how to space the floor, or which pass is the right one. Most basketball games reward making shots, which teaches none of that.</p>
""",
    'description': """
<p>Court Vision is a browser game built with three.js. You control one player, starting with the point guard, and run real plays: first with no defenders and heavy guidance, then against defenders who react. Shot-making is de-emphasised. What matters is where you move, who you pass to, and whether you take a good look.</p>
<p>The first version has five point guard plays (Give-and-Go, Drive-and-Kick, Dribble Handoff, High Pick-and-Roll and Horns Set) in three modes: Tutorial, Practice and Scrimmage. It is a static site with no backend. The game logic is a simulation core with no three.js or browser dependency, and plays, roles and defensive coverages are data, not code.</p>
""",
    'ai_usage': """
<p>I wrote the design document; my Software Factory pipeline built the game from it. The factory broke the document into issues along its milestones and worked through them one pull request at a time. Where the document was silent or contradicted itself, the question came to me, and the answer was recorded in a decisions log in the repository that later planning runs read.</p>
<p>More than 40 pull requests were merged in the project's first five days.</p>
""",
    'safety': """
<ul>
<li>Every pull request runs the type check, lint, unit tests and a production build. Only the main branch deploys.</li>
<li>The lint step fails if the simulation, content or AI layers import three.js or use browser globals, which keeps the game logic testable without a browser.</li>
<li>The design treats testing as part of the product, including bots that run each play making the correct read and the wrong one.</li>
</ul>
""",
    'results': """
<p>The game is playable in the browser and redeploys on every merge.</p>
""",
    'lessons_learned': """
<ul>
<li>A precise design document is what makes agent-built software come out the way you meant.</li>
<li>TypeScript, Vite, three.js, Vitest, GitHub Actions and GitHub Pages.</li>
</ul>
""",
}

CALLBACK = {
    'problem': """
<p>Tailoring a resume and cover letter to each job is slow. Generic AI rewrites are fast, but they invent experience and do not sound like the person applying.</p>
""",
    'description': """
<p>Callback takes a resume, a sample cover letter and optional supporting documents, plus a pasted job description, and writes a resume and cover letter for that job in the user's own voice. The user edits both in the app with a live preview and downloads PDFs.</p>
<p>The frontend is Next.js. The backend is Django and Django REST Framework with Celery and Redis for the generation jobs, Postgres for data and full-text search, and WeasyPrint for the PDFs.</p>
""",
    'ai_usage': """
<p>Generation runs in three stages with one Claude model each: a context scout that uses tools to find the relevant parts of the user's documents, with a cap on its steps; a writer; and a verifier that flags claims the source documents do not support. Retrieval is Postgres full-text search, with no embeddings.</p>
<p>The repository carries a written specification for AI coding agents, so that agents working on the code stay within the architecture.</p>
""",
    'safety': """
<ul>
<li>Unsupported claims are shown to the user in a flagged-claims panel instead of being silently kept.</li>
<li>Supporting documents are strictly scoped to their owner.</li>
<li>Authentication uses httpOnly cookies. Uploads and content are validated, and layout values are checked before they reach CSS.</li>
<li>Parsing, generation and sign-in are throttled, guarded against duplicate in-flight requests and capped per day, because each generation costs money.</li>
</ul>
""",
    'results': """
<p>The first version is merged: paste a job description, get both documents, edit them and export PDFs. It has been verified end to end against the real Anthropic API and in a headless browser, using a fictional resume. It is not deployed yet.</p>
""",
    'lessons_learned': """
<ul>
<li>Keep the language model on narrow tasks and put testable code around it.</li>
<li>Next.js, Django, Django REST Framework, Celery, Redis, PostgreSQL, Anthropic API, WeasyPrint, AWS S3, Docker.</li>
</ul>
""",
}
