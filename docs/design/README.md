# Design reference for the frontend overhaul

Approved by the owner on 2026/11/16. Tracking issue: #106.

These are standalone HTML files: open them in a browser. They are reference material only and are not served by the site
(`docs/` is outside Django's static and template folders).

| File | What it is | Used by |
|---|---|---|
| `homepage-mockup.html` | The full home page: hero, tethered orbit, "More projects", the pipeline panel, About, footer | #97 (tokens, nav, footer), #100, #103 |
| `orbit-prototype.html` | The tethered-orbit showcase on its own, with the string physics | #101 |

Notes for whoever implements from these:
- Port the code, do not rewrite it from the issue text. The owner tuned the feel against these files.
- The physics constants are at the top of the script in each file. Keep them unless the owner asks for a change.
- Both files load Archivo and JetBrains Mono from Google Fonts. The site self-hosts them (#97).
- Text in square brackets (`[YOUR EMAIL]`, `[ONE-LINE DESCRIPTION]`) is a placeholder for content the owner supplies.
- The project list, the "More projects" rows and the "Up next" queue are example data. The site reads them from the database.
