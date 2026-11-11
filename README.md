# [ChristianDonovan.ca](http://christiandonovan.ca/)

## Overview
A professional portfolio website built with Django, showcasing my projects and development experience. The application is hosted on a personal Linux server, utilizing Gunicorn as the application server and Nginx for handling web requests. Static files are efficiently managed and served through WhiteNoise, while MySQL powers both development and production databases to maintain strong [dev/prod parity](https://12factor.net/dev-prod-parity).

## Technologies & Skills Developed
Through the development and continuous improvement of this portfolio since 2020, I've gained extensive experience in:

### Core Technologies
- Django (Python web framework), with CKEditor 5 for rich-text editing in the admin
- MySQL database management
- Nginx web server
- Gunicorn application server
- HTML/CSS/JavaScript
- Responsive Design

### DevOps & Infrastructure
- Linux server administration
- SSL certificate management
- DNS configuration
- Automated CI/CD pipeline with GitHub Actions
  - Automated testing
  - Branch-based deployments
- Environment management
- Security best practices

### Additional Experience
- Docker containerization
- Serverless architectures (Google Cloud Run, AWS Lambda)
- Cloud platforms (Azure App Service, AWS EC2, Digital Ocean)
- Static content delivery (Firebase Storage, AWS S3)

## Local Development Setup

### Prerequisites
- Python 3.12+ (matches the server and CI)
- MySQL (or SQLite for a quick local run, see below)
- Git

### Initial Setup
1. Clone the repository and create a virtual environment (at the repository root):
   ```bash
   git clone git@github.com:Arbelaezch/Personal-Website.git
   cd Personal-Website
   python3 -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

2. Install dependencies (`requirements-dev.txt` adds `coverage` on top of `requirements.txt`):
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Configure environment variables. Django lives in `website/`, and settings read `website/website/.env`:
   ```bash
   cp website/website/.env.example website/website/.env
   ```
   Then edit it: set a `SECRET_KEY`, keep `DEBUG=1` for local development (production leaves it off, which turns on
   the HTTPS redirect, secure cookies, etc.), and fill in the `DEV_DB_*` database values. For a quick run without MySQL use
   `DEV_DB_ENGINE=django.db.backends.sqlite3` and `DEV_DB_NAME=db.sqlite3`, other `DEV_DB_*` values blank.

4. Database setup (run from the `website/` folder):
   ```bash
   cd website
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Running the Development Server
```bash
python manage.py runserver      # from website/
```
The site will be available at `http://localhost:8000` and the admin at `/admin/`.

### Tests
```bash
cd website
python manage.py test                         # the suite (SQLite, no MySQL needed when DEV_DB_* points at sqlite)
coverage run manage.py test && coverage report
python manage.py makemigrations --check --dry-run   # fails if a model change has no migration
```
CI runs these plus `check --deploy` (see `.github/workflows/main.yml`).

### Development Workflow
1. Create feature branches from main
2. Push changes to trigger automated tests
3. Open a PR into main; CI runs the tests
4. Merged changes automatically deploy to production (with a health check and automatic rollback)

There is no separate development server; run the site locally to try changes.

### Project layout
- `website/` - the Django project: `portfolio/` (home + projects), `films/`, `blog/`, `recipes/` (models and the read-only
  public API at `/api/v1/recipes/`, used by the [family-food](https://github.com/Arbelaezch/family-food) frontend), `api/urls.py` (API routing), `website/` (settings, shared helpers)
- `deploy/` - versioned server configuration (nginx, systemd units, Docker daemon settings); see `devops.txt`
- `devops.txt` - the server runbook (layout, services, deploys, firewall, backups, troubleshooting)

## Future Considerations
While the current implementation effectively serves its purpose, there are several potential areas for enhancement:
- Integration of modern CSS frameworks (Sass/Tailwind)
- Migration to a React/Vite frontend
- Additional interactive features
- Enhanced monitoring and logging

However, the focus remains on maintaining a stable, performant platform while directing development efforts toward new projects and learning opportunities.

## Contact
I welcome discussions about software development and appreciate constructive feedback. Feel free to reach out:
- Email: arbelaezch@gmail.com
- Website: [ChristianDonovan.ca](http://christiandonovan.ca/)
