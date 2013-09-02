PATTERNS = FileList['Web/static/patterns/**/*.*']
PREVIEWS = []

PATTERNS.each do |pat|
	preview = pat.sub(/^Web\/static\/patterns/, 'Web/static/build/previews').sub(/\.[^.]*$/, '.gif')
	puts preview
	file preview do
		outFolder = preview.sub(/\/[^\/]*$/,'')
		mkdir_p outFolder
		sh "python Utilities/GIF_preview.py #{pat} #{preview}"
	end
	PREVIEWS.push(preview)
	thumb = pat.sub(/^Web\/static\/patterns/, 'Web/static/build/thumbs')
	file thumb do
		outFolder = thumb.sub(/\/[^\/]*$/,'')
		mkdir_p outFolder
		sh "python Utilities/pattern_thumb.py #{pat} #{thumb}"
	end
	PREVIEWS.push(thumb)
end

task :default => PREVIEWS

task :serve => PREVIEWS do
	Dir.chdir "Web"
	sh "python ledweb.py"
end