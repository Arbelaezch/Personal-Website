<!DOCTYPE html>
<html lang="en">
<head>
  <title>Recipes</title>
  <link rel="stylesheet" href="styles.css">
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>



<body>
	<?php echo require_once("../../nav.php"); ?>


  	<article class="center">
		<header>
			<h1 class="title">Arbelaez Family Recipes</h1>
		</header>
		<section class="dishes">
			<div class="description">
				<h2>Favorite Dishes</h2>
				<p style="color: black; text-align: left; padding-left: 70px; text-indent: 20px; padding-right: 70px;">
					This page contains a collection of some of the best recipes ever discovered by human beings. The contents of this page could change the very fabric of human nature as we know it, and so therefore should be kept a secret as to not disrupt Earth's fragile ecosystems.
				</p>
			</div>
			
			<div id="grid">
				<div class="wrapper">
					 <div class="item">
						  <a href="./item/fried_rice.php">
								<img src="./images/fried_rice.jpg">
								</img>
								<p>Chicken Fried Rice</p>
						  </a>
					 </div>
					 <div class="item">
						  <a href="./item/ramen.php" class="grid">
								<img src="./images/ramen.jpg">
									 
								</img>
								<p>Ramen</p>
						  </a>
					 </div>
					 <div class="item">
						  <a href="./item/ribs.php" class="grid">
								<img src="./images/ribs.jpg">
									 
								</img>
								<p>Pork Back Ribs</p>
						  </a>
					 </div>
					 <div class="item">
						  <a href="./item/quesadilla.php" class="grid">
								<img src="./images/quesadilla.jpg">
									 
								</img>
								<p>Chicken Quesadilla  </p>
						  </a>
					 </div>	 
				</div>
		  </div>
		</section>
	</article>


	<footer>
		<p>
			Build by Christian Arbelaez for his online portfolio. 
			Copyright © by Christian Arbelaez. You are allowed to use this webpage for both 
			personal or commercial use.
		</p>
	</footer>
	

  


</body>
</html>