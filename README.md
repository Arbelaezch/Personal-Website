# [ChristianDonovan.ca](http://christiandonovan.ca/)

## Overview
A professional portfolio website built with Django, showcasing my projects and development experience. The application is hosted on a personal Linux server, utilizing Gunicorn as the application server and Nginx for handling web requests. Static files are efficiently managed and served through WhiteNoise, while MySQL powers both development and production databases to maintain strong [dev/prod parity](https://12factor.net/dev-prod-parity).

## Technologies & Skills Developed
Through the development and continuous improvement of this portfolio since 2020, I've gained extensive experience in:

### Core Technologies
- Django (Python web framework)
- MySQL database management
- Nginx web server
- Gunicorn application server
- HTML/CSS/JavaScript
- Responsive Design

### DevOps & Infrastructure
- Linux server administration
- SSL certificate management
- DNS configuration
- CI/CD implementation (GitHub Actions)
- Environment management
- Security best practices

### Additional Experience
- Docker containerization
- Serverless architectures (Google Cloud Run, AWS Lambda)
- Cloud platforms (Azure App Service, AWS EC2, Digital Ocean)
- Static content delivery (Firebase Storage, AWS S3)

## Local Development Setup

### Prerequisites
- Python 3.8+
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
   - Copy contents from `.env.example`
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

### Deployment
The project uses GitHub Actions for CI/CD. Pushing to the main branch automatically triggers deployment to production.

## Future Considerations
While the current implementation effectively serves its purpose, there are several potential areas for enhancement:
- Integration of modern CSS frameworks (Sass/Tailwind)
- Migration to a React/Vite frontend
- Additional interactive features

However, the focus remains on maintaining a stable, performant platform while directing development efforts toward new projects and learning opportunities.

## Contact
I welcome discussions about software development and appreciate constructive feedback. Feel free to reach out:
- Email: arbelaezch@gmail.com
- Website: [ChristianDonovan.ca](http://christiandonovan.ca/)
