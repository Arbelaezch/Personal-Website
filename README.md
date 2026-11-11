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
- MySQL
- Git

### Initial Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd website
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: .\env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Create `~/website/website/.env` file
   - Copy contents from `.env.example` (set `DEBUG=1` for local development; production leaves it off)
   - Update values for your local environment

5. Database setup:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

### Running the Development Server
```bash
python manage.py runserver
```
The site will be available at `http://localhost:8000`

### Development Workflow
The project follows a structured development workflow:

1. Create feature branches from main
2. Push changes to trigger automated tests
3. Open a PR into main; CI runs the tests
4. Merged changes automatically deploy to production

There is no separate development server; run the site locally (see above) to try changes.

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
