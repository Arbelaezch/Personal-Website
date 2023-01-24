# Repo for my personal portfolio/blog website, [ChristianDonovan.ca](http://christiandonovan.ca/)

*CHRISTIANDONOVAN.CA STILL UNDER DEVELOPMENT*

My website is currently built on top of a Django back end, configured to use a Firebase storage bucket for static and media files and a Supabase database for relational data, and deployed as a Docker image on Google Cloud Run. Of course, none of this is immediately apparent because it still only uses basic HTML/CSS/JS for the front-end as though it's trapped in the early 2000s...

I've spent more than a hundred hours of my life overengineering an app that gets maybe one visitor every twelve months because:

1. It has been an invaluable teacher. When I started this website I had no design experience, I had only passing familiarity with HTML/CSS, and I still thought buying a domain name was all I needed to access my website online. So far, because of this website I have learned:
    * HTML/CSS/JS (for real this time)
    * Responsive Design
    * Database Management
    * Docker
    * Serverless Functions
    * Supplemental Python/Django skills
2. I'm a cheap bastard and I was tired of paying more than $100/year for web hosting. Firebase, Supabase, and Google Cloud all have generous free tiers that provide more than enough hosting power to handle my yearly visitor.

Anyway, thank you for checking out my code and (maybe) my website. Feel free to shoot me a message at arbelaezch@gmail.com if you wanna chat or provide constructive criticism. I always appreciate new opportunities to learn more about my craft.

[Documentation](http://christiandonovan.ca/)

[This Project's Story](http://christiandonovan.ca/)

## Documentation

All required keys can be found in website/website/.env.example. It's up to you to fill them in.

Generate new GoogleServiceAccount.json file from Firebase project settings and place it in the conf directory.
