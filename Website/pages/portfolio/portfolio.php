<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portfolio</title>
  <link rel="stylesheet" href="styles.css">
  <form id="fcf-form-id" class="fcf-form-class" method="post" action="contact-form-process.php"></form>
  <script src="portfolio.js" defer></script>

  
</head>

<body>
	<?php echo require_once("../../nav.php"); ?>

	
	<div class="hero-image">
		<div class="hero-text">
		<h1>Christian Arbelaez</h1>
		<p>Programmer. Film nerd. Avid Alliteration Activist.</p>
		<!-- Add icon library -->
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

		<!-- Auto width -->
		<a href="./ChristianArbelaezResume.pdf" download>
			<button class="btn"><i class="fa fa-download"></i> Download Resume</button>
		</a>
		
		</div>
	</div>

	<section class="about">
		<div class="about-title">
		  <h2>ABOUT ME</h2>
		</div>
		
		<div class="about-content">
		  <p> 
			Howdy hello! My name is Christian and welcome to my website. I am a software developer by trade with a passion for building random little projects that express who I am, such as with this website. On this site you can find a lot about my favourite hobby: films and film study. There are also a few of my favourite cooking recipes, just to make sure I never forget them ;) On this portfolio page you can read about my education and previous larger scale software projects, with a few fun mini projects I felt like including. I have been developing software in a personal and academic setting for over six years and have learned many technologies and skills that continue to aid both my software development as well as my real life. One thing I love about developing software is that because it is an inherently challenging practice, it is a great teacher of resilience, patience, and being in control of your emotions (mostly lol).

			<br><br>

			In addition to software development, I have a strong drive for learning about the inner-workings of businesses and both the hard and soft skills of running one. The current project I am working on is a type of social game app that I am using to hone my software development skills as well as dip my feet into creating and marketing a real business.

			<br><br>

			I have the most experience programming in languages like Python, C/C++/C#, HTML/CSS, Javascript, and SQL, but I have become quite good at learning quickly and adapting to any technology I need to.
			<br><br>
		  </p>
		  
		</div>
	</section>
	





	<section class="technologies">
		<h2>TECHNOLOGIES I'm Familiar With</h2>
		<div class="tech-container">
			<img src="images/c.png" alt="C/C++">
			<img src="images/c++.png" alt="C/C++">
			<img src="images/java.png" alt="java" id="java">
			<br>
			<img src="images/css.png" alt="css">
			<img src="images/sql.png" alt="sql" id="sql">
			<img src="images/html.png" alt="html">
			<br>
			<img src="images/p2.png" alt="python" id="python">
			<img src="images/js.png" alt="javascript" id="javascript">
			<img src="images/Git-logo.svg.png" alt="Git" id="git">
		</div>
	</section>











	<section class="education">
		<div>
		  <h2>EDUCATION I've Completed</h2>
		</div>  
		<div>
		  <a href="https://apps.admissions.ualberta.ca/programs/sc/sc010/cmput31">
			<img src="images/UofA.png" alt="UofA">
		  </a>
		  <p>
			Bachelor of Science in Computer Science with a Business Minor 2016-2021.<br>
		  </p>
		</div>
	</section>






	<section class="projects">
		<h2>PROJECTS I've Worked On</h2>
		<div class="major-projects-container">
			<div class="prj-container">
				<a href="https://github.com/UAlberta-CMPUT401/teams-illuminator">
					<img src="./images/TeamIlluminator.png" alt="Team Illuminator" class="image">
					<div class="middle">
						<div class="text">
							<h1>Team Illuminator</h1><br> A web based educational tool designed to improve overall team productivity through personalized insights. Developed Winter 2020 in a team for a Software Engineering course. I was the team lead and so I handled all project management responsibilities in addition to doing programming on both the Frontend and Backend. We used an Agile approach to divide task responsibilities. It is primarily written in Javascript and Python.
						</div>
					</div>
				</a>
			</div>
			
			<div class="prj-container">
				<a href="https://github.com/CMPUT301F20T39/Booker">
					<img src="./images/Booker.png" alt="Booker" class="image" id="booker">
					<div class="middle">
						<div class="text">
							<h1>Booker</h1><br> A book sharing app that allows for users to lend and borrow books with other users. It was developed Fall 2020 in a team for my Software Engineering course. We used an Agile approach to divide responsibilities. It is written in Java for Android devices.
						</div>
					</div>
				</a>
			</div>
				
			<div class="prj-container">
				<a href="https://supersonic-productions.github.io/">
					<img src="./images/shipwrecked.png" alt="Shipwrecked" class="image">
					<div class="middle">
						<div class="text">
							<h1>Shipwrecked</h1><br> A video game that I helped build with an inter-disciplinary team in my Fall 2020 Games Development course. I was the team lead which meant that I handled all project management responsibilities along with additional programming and writing tasks. It is written in C# and playable by both MacOS and Windows.
						</div>
					</div>
				</a>
			</div>
		
		
		</div>



		<div class="minor-projects-container">
		  <ul>Other Minor Projects:
			<li>
			  <a href="./projects/clock/clock.html">Basic Clock using JS/HTML integration</a>
			</li>
			<li>
			  <a href="https://github.com/Arbelaezch/AHS-SMS-Auto-Responder">AHS SMS Auto Responder</a>
			</li>
			<li>
			  <a href="https://github.com/Arbelaezch/BouncingTommyLee">Bouncing Tommy Lee Jones Screeensaver</a>
			</li>
		  </ul>
  
		</div>
	</section>





	  
<!-- Contact me form code from: https://paperform.co/blog/html-contact-form/-->
	<section id="container">
		<form id="fcf-form-id" class="fcf-form-class" method="post" action="contact-form-process.php">
		
			<h2 style="text-align: center; padding: 2rem 0 1rem 0;">CONTACT ME</h2>
			<label for="Name" class="fcf-label">Your name</label>
			<div class="fcf-input-group">
				<input type="text" id="Name" name="Name" class="fcf-form-control" required>
			</div>
			<div class="fcf-form-group">
				<label for="Email" class="fcf-label">Your email address</label>
				<div class="fcf-input-group">
					<input type="email" id="Email" name="Email" class="fcf-form-control" required>
				</div>
				<div class="fcf-form-group">
					<label for="Message" class="fcf-label">Your message</label>
					<div class="fcf-input-group">
						<textarea id="Message" name="Message" class="fcf-form-control" required style="height: 10rem;"></textarea>
					</div>
				</div>
				<div class="fcf-form-group" id="submit-container">
					<button type="submit" id="fcf-button" class="fcf-btn fcf-btn-primary fcf-btn-lg fcf-btn-block">Send</button>
				</div>
			</div>
		</form>
	</section>





	<footer>
		<div class="links-box">
			<a href="https://github.com/Arbelaezch">
				<img src="./images/github.png" class="socials" alt="github">
			</a>
			<a href="https://www.facebook.com/christian.arbelaez.9">
				<img src="./images/facebook.png" class="socials" alt="facebook">
			</a>
		</div>
		<div class="copyright">
		Build by Christian Arbelaez for his online portfolio. Copyright © by Christian Arbelaez. 
		Feel free to use this webpage for both personal or commercial use.
		<br><br>
		Profile Photo by <a href="https://unsplash.com/@noland9?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Nolan Di Meo</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
  
		</div>
	</footer>


	

</body>
</html>