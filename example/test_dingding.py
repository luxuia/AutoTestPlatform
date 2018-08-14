
# We need the path to setup.py to be able to run
# the setup from a different folder
import os, sys
def setup_path(path = ""):
    # get the path to the setup file
    setup_path = os.path.abspath(os.path.split(__file__)[0])

    return os.path.join(setup_path, path)

sys.path.insert(0, setup_path('..'))

from source.core.api import *
from source.core.cv import *
from source.core.help import *
from source.core.win.win import Window

handle = sys.argv[1]
G.DEVICE = Window(handle=handle) 


while True:
	click(Template('__export_res__/9e791c6e-555a-4c18-b2ef-d51af36e08e6.png'))
	sleep(1)
