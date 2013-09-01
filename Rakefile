PATTERNS = FileList['Web/static/patterns/**/*']
PREVIEWS = []

PATTERNS.each do |pat|
	preview = pat.sub(/^Web\/static\/patterns/, 'Web/static/build/previews').sub(/\.[^.]*$/, '.gif')
	outFolder = preview.sub(/\/[^\/]*$/,'')
	mkdir_p outFolder
	file preview do
		sh "python Utilities/GIF_preview.py #{pat} #{preview}"
	end
	puts preview
	PREVIEWS.push(preview)
end

task :default => PREVIEWS

task :serve => PREVIEWS do
	Dir.chdir "Web"
	sh "python ledweb.py"
end