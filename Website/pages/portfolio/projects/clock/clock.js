var noon = 12;

// Function to set current time to webpage
var showCurrentTime = function() {
  var clock = document.getElementById('clock');
  
  var currentTime = new Date();
  var hours = currentTime.getHours();
  var mins = currentTime.getMinutes();
  var secs = currentTime.getSeconds();
  
  var AMToggle = "AM";
  
  // Sets hour
  if (hours >=  noon) {
    AMToggle = "PM";
  }
  
  if (hours > noon) {
    hours -= 12;
  }
  
  if (mins < 10) {
    mins = '0' + mins;
  }
  
  if (secs < 10) {
    secs = '0' + secs;
  }
  
  var clockTime = hours + ':' + mins + ':' + secs + AMToggle;
  
  clock.innerText = clockTime;
  
};


// Updates clock.
var updateClock = function() {
  var time = new Date().getHours();
  
  showCurrentTime();
};

updateClock();

var oneSecond = 1000;
setInterval( updateClock, oneSecond);
