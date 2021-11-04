<!DOCTYPE html>
<html lang="en">
<head>
  <title>Movie Blog</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="style.css">
</head>


<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
?>


<body>
  <?php echo require_once("../../nav.php"); ?>
  
  <!-- MAIN CONTENT-->
  <article class="center">
    <div id="content">
      <header>
        <h1 class="title">My Top 250 Movies</h1>
      </header>
      <section class="mid">
        <div class="list">
          <ol>
            <a href="./Decades/1980s/movies/thing.php">
              <li>The Thing (1982)</li>
            </a>
            <a href="./Decades/2000s/movies/NoCountry.php">
              <li>No Country For Old Men (2007)</li>
            </a>
            <a href="./Decades/2020s/movies/nomadland.php">
              <li>Nomadland (2020)</li>
            </a>
            <a href="./Decades/1990s/movies/terminator2.php">
              <li>Terminator 2: Judgement Day (1991)</li>
            </a>
            <a href="./Decades/1930s/movies/smithWashington.php">
              <li>Mr. Smith Goes to Washington (1939)</li>
            </a>
            <a href="./Decades/2020s/movies/minari.php">
              <li>Minari (2020)</li>
            </a>
            <a href="./Decades/2010s/movies/interstellar.php">
              <li>Interstellar (2014)</li>
            </a>
            <a href="./Decades/1940s/movies/miniver.php">
              <li>Mrs. Miniver (1942))</li>
            </a>
            <a href="./Decades/1900s/movies/sherlock.php">
              <li>Sherlock Jr. (1924)</li>
            </a>
            <a href="./Decades/1960s/movies/2001.php">
              <li>2001: A Space Odyssey (1968)</li>
            </a>
            <a href="./Decades/1940s/movies/philadelphia.php">
              <li>The Philadelphia Story (1940)</li>
            </a>
            <a href="./Decades/2010s/movies/gravity.php">
              <li>Gravity (2013)</li>
            </a>
            <a href="./Decades/1990s/movies/matrix.php">
              <li>The Matrix (1999)</li>
            </a>
            <a href="./Decades/1970s/movies/tora.php">
              <li>Tora! Tora! Tora! (1970)</li>
            </a>
            <a href="./Decades/1930s/movies/kingKong.php">
              <li>King Kong (1933)</li>
            </a>
            <a href="./Decades/1930s/movies/cityLights.php">
              <li>City Lights (1931)</li>
            </a>
            <a href="./Decades/1940s/movies/grapes.php">
              <li>The Grapes of Wrath (1940)</li>
            </a>
            <a href="./Decades/1930s/movies/dirtyFaces.php">
              <li>Angels With Dirty Faces (1938)</li>
            </a>
            <a href="./Decades/1930s/movies/modernTimes.php">
              <li>Modern Times (1936)</li>
            </a>
            <a href="./Decades/1900s/movies/sunrise.php">
              <li>Sunrise: A Song of Two Humans (1927)</li>
            </a>
            <a href="./Decades/1990s/movies/eyesWideShut.php">
              <li>Eyes Wide Shut (1999)</li>
            </a>
            <a href="./Decades/1940s/movies/malteseFalcon.php">
              <li>The Maltese Falcon (1941)</li>
            </a>
            <a href="./Decades/1900s/movies/goldRush.php"> 
              <li>The Gold Rush (1925)</li>
            </a>
            <a href="./Decades/2000s/movies/humanCentipede.php">
              <li>The Human Centipede (First Sequence) (2009)</li>
            </a>
            <a href="./Decades/1940s/movies/kane.php">
              <li>Citizen Kane (1941)</li>
            </a>
            <a href="./Decades/1930s/movies/happenedOneNight.php">
              <li>It Happened One Night (1934)</li>
            </a>
            <a href="./Decades/1940s/movies/dictator.php"> 
              <li>The Great Dictator (1940)</li>
            </a>
            <a href="./Decades/2000s/movies/translation.php">
              <li>Lost in Translation (2003)</li>
            </a>
            <a href="./Decades/2010s/movies/sistersBrothers.php">
              <li>The Sisters Brothers (2018)</li>
            </a>
            <a href="./Decades/2010s/movies/busan.php">
              <li>Train to Busan (2016)</li>
            </a>
            <a href="./Decades/1930s/movies/westernFront.php">
              <li>All Quiet on the Western Front (1930)</li>
            </a>
            <a href="./Decades/1930s/movies/snowWhite.php">
              <li>Snow White (1937)</li>
            </a>
            <a href="./Decades/1990s/movies/matilda.php">
              <li>Matilda (1996)</li>
            </a>
            <a href="./Decades/1930s/movies/deeds.php">
              <li>Mr. Deeds Goes to Town (1936)</li>
            </a>
            <a href="./Decades/1900s/movies/steamboatWillie.php">
              <li>Steamboat Willie (1928)</li>
            </a>
          </ol>  
        </div>
      </section>
    </div>
      
    <!-- SIDEBAR -->
    <div id="sidebar">
      <div id="sideHeader">
        <a href="./250.php">
          <img style="width: 250px; height: 200px;" src="./images/Nav/top250.jpg" alt="top 250 movies">
        </a>
        <a href="./Decades/1900s/1900s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1900s.jpg" alt="1900s">
        </a>
        <a href="./Decades/1930s/1930s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1930s.jpg" alt="1930s">
        </a>
        <a href="./Decades/1940s/1940s.php">
          <img style="width: 250px; height: 55px;" src="./images/Nav/1940s.jpg" alt="1940s">
        </a>
        <a href="./Decades/1950s/1950s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1950s.jpg" alt="1950s">
        </a>
        <a href="./Decades/1960s/1960s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1960s.jpg" alt="1960s">
        </a>
        <a href="./Decades/1970s/1970s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1970s.jpg" alt="1970s">
        </a>
        <a href="./Decades/1980s/1980s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1980s.jpg" alt="1980s">
        </a>
        <a href="./Decades/1990s/1990s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/1990s.jpg" alt="1990s">
        </a>
        <a href="./Decades/2000s/2000s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/2000s.jpg" alt="2000s">
        </a>
        <a href="./Decades/2010s/2010s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/2010s.jpg" alt="2010s">
        </a>
        <a href="./Decades/2020s/2020s.php">
          <img style="width: 250px; height: 65px;" src="./images/Nav/2020s.jpg" alt="2020s">
        </a>
      </div>
    </div>


  </article>
  

	
  <footer>
	  <p>
      Build by Christian Arbelaez for his online portfolio. Copyright © by Christian Arbelaez. You are allowed to use this webpage for both personal or commercial use.
    </p>
	</footer>
  
	

</body>
</html>
