$(document).ready(function() {
  updateQueue();
  
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
    $.getJSON('/play', {pattern: p}, function(result) {
      updateQueue();
    });
  });
  
});

function updateQueue() {
  $.getJSON('/queue', function(result) {
    var queue = result['queue'];
    var qh = ''
    for (var i = 0; i < queue.length; i++) {
      var p = queue[i][0];
      var n = queue[i][1];
      qh += 
        '<li><img src="/static/patterns/' + p + '"></li>';
    }
    $('#queue ul').html(qh);
  })
}