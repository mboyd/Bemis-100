<!DOCTYPE html>
<html>
<head>
  <title>LEDWeb Alpha</title>
  ${h.stylesheet_link('/stylesheets/bemis100.css')}
  <link href='http://fonts.googleapis.com/css?family=Droid+Sans' rel='stylesheet' type='text/css'>
  <script src='/javascripts/bemis100_canvas.js'></script>
</head>

<body>
  <div id='header'>
    <h1>Bemis 100</h1>
  </div>
  
  <div id='liveview'>
    <canvas id='canvas' width='830' height='50'></canvas>
    <div id='controls'>
      <a class='pause' href='#'>Pause</a> &nbsp;&nbsp;|&nbsp;&nbsp;
      <a class='next' href='#'>Next</a>
    </div>
  </div>
  
  <div id='content'>
    ${self.body()}
  </div>

</body>
</html>