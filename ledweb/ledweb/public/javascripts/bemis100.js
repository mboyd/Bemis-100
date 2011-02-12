$(document).ready(function() {
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
      
      });
    }
  });
});