$(document).ready(function() {
  $('#patterns h2 a').click(function(evt) {
    $(document.body).append('<iframe id="muro" src="http://muro.deviantart.com"' + 
                ' style="z-index: 2; position: absolute; top: 5%; left: 5%;' + 
                ' width: 90%; height: 90%; margin: auto;"></iframe>');
                
    var muro = $('iframe#muro').contents().get(0);
    $(muro).ready(function() {
      $('div.submitButton', muro).click(function(evt) {
        evt.preventDefault();
        alert('Click!');
      });
    });
  });
  

  
});