#Bemis 100
Firmware, software and web interface for the 1E Bemis100 lighting system.

##Dependencies
- Python 2.6 (2.7 should work, 3.x won't)
- PIL
- numpy
- pyaudio
- tornado
- TornadIO2 (use the development version from https://github.com/MrJoes/tornadio2)

##Usage
Command line: `python run.py [-d device] [-f framerate] (pattern | pattern_dir) ...`

Web interface: `cd Web; python ledweb.py`
