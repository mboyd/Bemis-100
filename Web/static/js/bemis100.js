$(document).ready(function() {
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

    $.getJSON('/add', params, function(result) {
      updateQueue();
    });
  });

});


function updateDevices() {
  $.getJSON('/device_list', function(result) {
    var writers = result.writers;
    var ports = result.ports;
    var form_html = 'Type: <select name="writers">';
    for (var i=0; i<writers.length; i++) {
      form_html += '<option value="' + writers[i] + '">' + writers[i] + '</option>';
    }
    form_html += '</select> Port: <select name="ports">';
    for (i=0; i<ports.length; i++) {
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
    var writer_list = '';
    for (var i = 0; i < result.length; i++) {
      writer_list += '<li>' + result[i] + '</li>';
    }
    $('#writer_list ul').html(writer_list);
  });
}

function updateQueue() {
  $.getJSON('/queue', function(result) {
    var queue = result['queue'];
    var qh = '';
    var p;
    var n;

    if (queue.length === 0) {
      qh = '<li>empty</li>';
    }

    for (var i = 0; i < queue.length; i++) {
      p = queue[i].name;
      n = queue[i].reps;
      qh +=
        '<li><img src="/static/patterns/' + p + '">' +

        '</li>';
    }
    $('#queue ul').html(qh);
    var current = result['current'];
    p = current.name;
    n = current.reps;
    if (n !== 0) {
      $('#current ul').html('<li><img src="/static/patterns/' + p + '">' + '</li>');
    }
  setTimeout(updateQueue, 2000);
  });
}
