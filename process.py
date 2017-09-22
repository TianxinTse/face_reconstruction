import os
import sys


activate_this = 'E:/computer-vision/human-face/face-reconstruction/venv/Scripts/activate_this.py'

with open(activate_this, 'r') as f:
    exec(f.read(), dict(__file__=activate_this))

command = 'python E:/computer-vision/human-face/face-reconstruction/fr.py ' + sys.argv[1]
os.system(command)
