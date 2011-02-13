<%inherit file="/base.mako"/>

<div id='queue'>
	<h2>Queue</h2>
	<ul>
	</ul>
</div>

<div id='patterns'>
	<h2>Patterns</h2>
	% for p in c.patterns:
	  <a href='/play?pattern=${p}'>
		<img class='pattern' data-pattern='${p}' alt='pattern' src='${c.pattern_dir}/${p}'>
		</a>
	% endfor
</div>
