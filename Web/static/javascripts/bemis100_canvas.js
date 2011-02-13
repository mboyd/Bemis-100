var canvas;
var ctx;
var ws;

$(document).ready(function() {
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  
  startSocketCheck();
});

function connect() {
  ws = new WebSocket("ws://localhost:9999");
  
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
    } else if (data['status'] == 'exiting') {
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
    setTimeout(startSocketCheck, 2000);
  }
}
