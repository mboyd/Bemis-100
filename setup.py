from distutils.core import setup
import py2exe
setup(
    options = {'py2exe': {'bundle_files': 1}},
    windows = [{'script': "run.py"}]
)
# setup(console=['run.py -f 30 -g -n 25 -d COM5 new_wave'])

