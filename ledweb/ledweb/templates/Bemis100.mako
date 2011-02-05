< %inherit file="/base.mako"/>

<div id='queue'>
	<h2>Queue</h2>
	<p id='controls'>
		<a>Play</a>
	</p>
	<ul>
		<li>Pattern 1</li>
  	<li>Pattern 2</li>
	</ul>
</div>

<div id='patterns'>
	<h2>Patterns</h2>
	% for p in c.patterns:
		<img class='pattern' alt='pattern' src='${c.pattern_dir}/${p}'>
	% endfor
</div>

