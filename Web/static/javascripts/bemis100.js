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

  updateDevices();
  updateWriters();
  
  $('#play_controls a').click(function(evt) {
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
	  updateQueue();
    
    } else if ($(evt.target).hasClass('next')) { 
      $.getJSON('/next', function(result) {
        updateQueue();
      });
    }
  });

  $('#add_writer').click(function(evt) {
    evt.preventDefault();
    var selects = $('#writer_controls select');
    var writer_type = selects[0].options[selects[0].selectedIndex].text;
    var port = selects[1].options[selects[1].selectedIndex].text;
    $.getJSON('/add_writer', {'writer_type': writer_type, 'port': port}, function(result) {});
    updateWriters();
  });


  $('#patterns a').click(function(evt) {
    evt.preventDefault();
    
    var p = evt.target.getAttribute('data-pattern');
    
    var track_beat = $('#pattern_config input[name=beat_tracking]').is(':checked');
    
    params = {pattern: p};
    if (track_beat) {
      params.beat = true;
    }
    
    // $('#play_pause').removeClass('pause');
    // $('#play_pause').addClass('play');
    // $('#play_pause').html('Play');
    
    $.getJSON('/add', params, function(result) {
      updateQueue();
    });
  });
  
});

function connect() {
	//console.log('connecting')

  ws = io.connect('/');
  
  ws.on('connect', function() {
    $('#connection').html('Status: connected');
    updateQueue();
	// console.log('Opened WS connection')
  });
  
  ws.on('message', function(e) {
    var data = JSON.parse(e);
    
    if (data['status'] == 'ok') {
		// console.log(data['frame']);
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
      //ws.close();
    }
  });
  
  ws.on('disconnect', function() {
	  console.log('Closed WS connection')
    $('#connection').html('Status: disconnected');
    blank();
    setTimeout(connect, 2000);
  });
}

function updateDevices() {
  $.getJSON('/device_list', function(result) {
    var writers = result.writers;
    var ports = result.ports;
    var form_html = 'Type: <select name="writers">';
    for (var i=0; i<writers.length; i++) {
      form_html += '<option value="' + writers[i] + '">' + writers[i] + '</option>';
    }
    form_html += '</select> Port: <select name="ports">';
    for (var i=0; i<ports.length; i++) {
      form_html += '<option value="' + ports[i] + '">' + ports[i] + '</option>';
    }
    // form_html += '</select> <input type="submit" value="Add Writer"/>';
    form_html += '</select>';
    $('#writer_controls').html(form_html);
    console.log(writers);
    console.log(ports);
  });
}

function updateWriters() {
  $.getJSON('/get_writers', function(result) {
    console.log(result);
    var writer_list = ''
    for (var i = 0; i < result.length; i++) {
      writer_list += '<li>' + result[i] + '</li>'
    }
    $('#writer_list ul').html(writer_list);
  });
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
      qh = '<li>empty</li>';
    }
    
    for (var i = 0; i < queue.length; i++) {
      var p = queue[i][0];
      var n = queue[i][1];
      qh += 
        '<li><img src="/static/patterns/' + p + '">' + 
        
        '</li>';
    }
    $('#queue ul').html(qh);
	  var current_pattern = result['current'];
	  var p = current_pattern[0];
	  var n = current_pattern[1];
	  if (n != 0) {
		  $('#current ul').html('<li><img src="/static/patterns/' + p + '">' + '</li>');
	  }
	  setTimeout(updateQueue, 2000);
  });
}
