


<?php


$ret = [];
$dir = $_SERVER['DOCUMENT_ROOT'] . "/pages/blog";
 // set directory in question

if(is_dir($dir)) {
   $ret = array_diff(scandir($dir), array(".", "..")); // get all files in dir as array and remove . and .. from it
}

usort($ret, function ($a, $b) use ($dir) {
    if(filectime($dir . "/" . $a) < filectime($dir . "/" . $b)) {
         return -1;
    } else if(filectime($dir . "/" . $a) == filectime($dir . "/" . $b)) {
         return 0;
    } else {
         return 1;
    }
}); // sort array by file creation time, older first

$latest_file = $ret[count($ret)-1];




echo 
'<nav>
      <a href="/index.php">Home</a>
      <a href="/pages/recipes/recipes.php">Food</a>
      <a href="/pages/movies/250.php">Movies</a>
      <a href="/pages/blog/' . $latest_file . '">Blog</a>
      <a href="/pages/portfolio/portfolio.php">Portfolio</a>
      <a href="/pages/portfolio/portfolio.php#container">Contact Me</a>
</nav>';

?>