<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <link rel="stylesheet" href="styles.css">
    <script src="app.js" defer></script>

    <title>Blog</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
  <body>
    <header id="header">
      <?php echo require_once("../../nav.php"); ?>
    </header>
    
   
    <div class="container">

      <div class="blog-header">
        <h1 class="blog-title">Project Blog</h1>
        <p class="lead blog-description">An archive of completed or ongoing development projects that I'm working on. Will likely range from game development projects like mods or small game experiences, web apps or possibly Android apps if I can stomach opening Android Studio for ten minutes.</p>
      </div>

      <div class="row">

        <div class="col-sm-8 blog-main">

          <div class="blog-post" id="intention">
            <h2 class="blog-post-title">Intention.</h2>
            <p class="blog-post-meta">January 12, 2022</p>

          
            <img src="./images/blogtemplate.JPG" id="image">
            
            
            <p>This is the mockup that I created in Adobe XD before I began actually coding. Then, when I began coding I thought: "I wonder how much faster this would go with Bootstrap." Turns out Bootstrap had a template that was basically the exact same UI design.</p>
            
            <p>I'd never used Bootstrap before so this was a good opportunity for me to get acquainted with it. I'm sure I'm the first person to realize that it makes developing projects extremely fast and easy.</p>
            
            <p> This is also the first project I've used Adobe XD, despite my incredible mockup skills. It wasn't too difficult to pick up, and having a vague picture of the UI that I wanted in my head made it easier to actually implement. Even though I used a Bootstrap template for the HTML, when I was looking for templates I already knew what I was looking for and what basic features I needed to be sure were included.
            </p>
            
          </div><!-- /.blog-post -->





          <div><!-- This is where new blog posts go -->

          </div><!-- /.blog-post -->

          

          

        </div><!-- /.blog-main -->

        <div class="col-sm-3 col-sm-offset-1 blog-sidebar">
          <div class="sidebar-module sidebar-module-inset">
            <h4>About</h4>
            <p>Chronological order of completed projects.</p>
          </div>
          <div class="sidebar-module">
            <h4>Archives</h4>
            <ol class="list-unstyled">
            
            <!--
            <a href="http://www.arbelaezch.ca/blog/blog.php/#intention">Link</a>
            <li><a href="./blog.php/#intention">January 2022</a></li>-->

              <li><a href="./jan22.php">January 2022</a></li>


            </ol>
          </div>
          <div class="sidebar-module">
            <h4>Elsewhere</h4>
            <ol class="list-unstyled">
              <li><a href="https://github.com/Arbelaezch">GitHub</a></li>
              <li><a href="https://www.linkedin.com/in/christian-arbelaez2021/">LinkedIn</a></li>
              <li><a href="https://www.facebook.com/christian.arbelaez.9">Facebook</a></li>
            </ol>
          </div>
        </div><!-- /.blog-sidebar -->

      </div><!-- /.row -->

    </div><!-- /.container -->

    <footer class="blog-footer">
      
    </footer>


<!-- Bootstrap core JavaScript
================================================== -->
<!-- Placed at the end of the document so the pages load faster -->
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://code.jquery.com/jquery-1.12.4.min.js" integrity="sha384-nvAa0+6Qg9clwYCGGPpDQLVpLNn0fRaROjHqs13t4Ggj3Ez50XnGQqc/r8MhnRDZ" crossorigin="anonymous"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
  </body>
</html>