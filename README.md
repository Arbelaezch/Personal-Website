# [ChristianDonovan.ca](http://christiandonovan.ca/) Repo

*CHRISTIANDONOVAN.CA STILL UNDER DEVELOPMENT*

[Documentation](http://christiandonovan.ca/)

[This Project's Story](http://christiandonovan.ca/)

TLDR: I have been iterating on this website since 2020. Over that time it has gone through many redesigns and I have learned much about full-stack development.

My website is currently built on top of a Django back end, configured to use a Firebase storage bucket for static and media files and a Supabase database (PostgreSQL)for relational data, and deployed as a Docker image on Google Cloud Run. Of course, none of this is immediately apparent because it still only uses basic HTML/CSS/JS for the front-end as though it's trapped in the early 2000s...

I've spent more than a hundred hours of my life overengineering an app that gets maybe one visitor every twelve months because:

1. It has been an invaluable teacher. When I started this website I had no design experience, I had only passing familiarity with HTML/CSS, and I still thought buying a domain name was all I needed to access my website online. Some of the things I have learned iterating on this website:
    * HTML/CSS/JS (for real this time)
    * Responsive Design
    * Database Management (SQLite -> MySQL -> PostgreSQL)
    * Using environment variables for config
    * Connecting DB and storage bucket backing services
    * Docker
    * Serverless Functions
2. I'm a cheap bastard and I was tired of paying more than $100/year for web hosting. Firebase, Supabase, and Google Cloud all have generous free tiers that provide more than enough hosting power to handle my yearly visitor.

Anyway, thank you for checking out my code and (maybe) my website. Feel free to shoot me a message at arbelaezch@gmail.com if you wanna chat or provide constructive criticism. I always appreciate new opportunities to learn more about my craft.

## Documentation

All required keys can be found in website/website/.env.example. It's up to you to fill them in.

Generate new GoogleServiceAccount.json file from Firebase project settings and place it in the conf directory.

When building Docker image using an ARM Mac, include --platform linux/arm64 argument as per:
https://stackoverflow.com/questions/66127933/cloud-run-failed-to-start-and-then-listen-on-the-port-defined-by-the-port-envi

If there is a problem installing psycopg2 from requirements.txt, try running the following command:
brew install postgresql
