var canvas;
var ctx;
var ws;

var frameCount;
var lastTime;

$(document).ready(function() {
  
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  blank();
  
  frameCount = 0;
  lastTime = (new Date).getTime();
  
  connect();
  
  $('#controls a').click(function(evt) {
    evt.preventDefault();
    
    if ($(evt.target).hasClass('pause')) {  
      $.getJSON('/pause', function(result) {
      
      });
    
      $(evt.target).removeClass('pause');
      $(evt.target).addClass('play');
      $(evt.target).html('Play');
    
    } else if ($(evt.target).hasClass('play')) { 
      $.getJSON('/play', function(result) {
      
      });
      $(evt.target).removeClass('play');
      $(evt.target).addClass('pause');
      $(evt.target).html('Pause');
    
    } else if ($(evt.target).hasClass('next')) { 
      $.getJSON('/next', function(result) {
        updateQueue();
      });
    }
  });
  
  $('#patterns a').click(function(evt) {
    evt.preventDefault();
    
    var p = evt.target.getAttribute('data-pattern');
    
    var track_beat = $('#pattern_config input[name=beat_tracking]').is(':checked');
    
    params = {pattern: p};
    if (track_beat) {
      params.beat = true;
    }
    
    $('#play_pause').removeClass('pause');
    $('#play_pause').addClass('play');
    $('#play_pause').html('Play');
    
    $.getJSON('/play', params, function(result) {
      updateQueue();
    });
  });
  
});

function connect() {
  ws = new WebSocket("ws://localhost:9999");
  
  ws.onopen = function() {
    $('#connection').html('Status: connected');
    updateQueue();
  }
  
  ws.onmessage = function(e) {
    var data = JSON.parse(e.data);
    
    if (data['status'] == 'ok') {
      var frame = data['frame'];
      var pixelWidth = canvas.width / frame.length;
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
    $('#connection').html('Status: disconnected');
    blank();
    setTimeout(connect, 2000);
  }
}

function blank() {
  ctx.fillStyle = 'rgb(0,0,0)';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function updateQueue() {
  $.getJSON('/queue', function(result) {
    var queue = result['queue'];
    var qh = '';
    
    if (queue.length == 0) {
      qh = '<li>Queue empty</li>';
    }
    
    for (var i = 0; i < queue.length; i++) {
      var p = queue[i][0];
      var n = queue[i][1];
      qh += 
        '<li><img src="/static/patterns/' + p + '">' + 
        
        '</li>';
    }
    $('#queue ul').html(qh);
  })
}