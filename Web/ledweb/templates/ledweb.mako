<%inherit file="/base.mako"/>
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

<div id='queue'>
	<h2>Queue</h2>
	<ul>
	</ul>
</div>

<div id='patterns'>
	<h2>Patterns</h2>
	${h.show_patterns(c.patterns) | n}
</div>

<div id='upload'>
  <form action='/upload' method='post' enctype="multipart/form-data">
    <label for='pattern'>Upload a pattern</label>
    <input type='file' name='pattern'>
    <input type='submit' value='Upload'>
  </form>
</div>
