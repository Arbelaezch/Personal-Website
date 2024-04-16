# [ChristianDonovan.ca](http://christiandonovan.ca/)

   This current iteration of my portfolio is built with a Django backend, hosted on my own personal Linux server. Gunicorn is the application server while Nginx handles web requests. Static files are compressed and served by WhiteNoise. PostgreSQL is used for both my dev and production databases to increase [dev / prod parity](https://12factor.net/dev-prod-parity).

Since 2020 I've spent more than a hundred hours over engineering this website that has very little dynamic functionality and gets maybe one visitor every twelve months because it has been an invaluable teacher.

Because of the time I've invested, I have learned countless lessons in both full-stack and general software development. When I started this website I had no design experience, I had only passing familiarity with HTML/CSS, and I still thought buying a domain was all I needed in order to access my website online. Some of the things I have learned from this project include:
    * HTML/CSS/JS
    * Responsive Design
    * Database Management (SQLite, MySQL, and now PostgreSQL)
    * Environment variables and secret config
    * Linux server management
    * Web servers (Nginx)
    * Application servers (Gunicorn)
    * SSL certificates
    * DNS management
    * CI/CD pipelines (GitHub Actions)

Other technologies I've worked with over the many iterations of this project include:
    * Docker
    * Serverless Functions (Google Cloud Run, AWS Lambda)
    * Cloud Hosting (Azure App Service, AWS EC2, Digital Ocean droplets)
    * Static file hosting (Firebase Storage, AWS S3)

I recognize that I could update the website to use more than basic CSS for stying. Sass or Tailwind would be great, React/Vite might be better. The desire for a full re-write is strong, as it always is with legacy projects. And as with those projects I must ignore my desires in order to better spend my time building other, more important projects.

Thank you for checking out my code and (maybe) my website. Feel free to fire me a email at arbelaezch@gmail.com if you wanna chat or provide constructive criticism. I always appreciate the opportunity to learn more about my craft.
