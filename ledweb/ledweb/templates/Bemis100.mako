<%inherit file="/base.mako"/>

<div id='queue'>
	<h2>Queue</h2>
	<ul>
	 <li><img src='patterns/cylon8x16.gif'></li>
   <li><img src='patterns/mandelbot.gif'></li>
	 <li><img src='patterns/mandelbrot2.png'></li>
	 <li><img src='patterns/mandelbrot3.png'></li>
	 <li><img src='patterns/rainbow.gif'></li>
	 <li><img src='patterns/rainbow166x1.gif'></li>
	 <li><img src='patterns/rainbow166x1center.gif'></li>
	</ul>
</div>

<div id='patterns'>
	<h2>Patterns</h2>
	% for p in c.patterns:
		<img class='pattern' alt='pattern' src='${c.pattern_dir}/${p}'>
	% endfor
</div>
