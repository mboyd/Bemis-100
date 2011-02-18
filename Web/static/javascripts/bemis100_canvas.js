var canvas;
var ctx;
var ws;

var frameCount;
var lastTime;

$(document).ready(function() {
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  
  frameCount = 0;
  lastTime = (new Date).getTime();
  
  startSocketCheck();
});

function connect() {
  ws = new WebSocket("ws://localhost:9999");
  
  $('#connection').html('Status: connected')
  
  ws.onmessage = function(e) {
    var data = JSON.parse(e.data);
    
    if (data['status'] == 'ok') {
      var frame = data['frame'];
      var pixelWidth = canvas.width / (83 * 2);
      var height = canvas.height;
      
      for (var i = 0; i < frame.length; i++) {
        ctx.fillStyle = frame[i];
        ctx.fillRect(i*pixelWidth, 0, pixelWidth, height);
      }
      
      if (frameCount == 30) {
        frameCount = 0;
        var t = (new Date).getTime();
        var dt = t - lastTime;
        var fr = 30 / (dt / 1000.0);
        $('#framerate').html('Framerate: ' + fr.toFixed(2) + ' fps');
      
        lastTime = t;
      }
      
      frameCount += 1;
      
    } else if (data['status'] == 'exiting') {
      $('#framerate').html('');
      ws.close();
    }
  };
  
  ws.onclose = function() {
    setTimeout(startSocketCheck, 1000);
  }
}

function startSocketCheck() {
  try {
    connect();
  } catch (err) {
    $('#connection').html('Status: disconnected');
    setTimeout(startSocketCheck, 2000);
  }
}
