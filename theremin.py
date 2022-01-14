import os
import sys
from datetime import datetime, timedelta
from os.path import dirname, join, abspath
from pysinewave import SineWave

import pdb

# leap lib
sys.path.append(join(dirname(__file__), './python-leap-ctypes/', 'src'))

# Set DLL path for leap libraries
os.environ['LEAP_DLL_PATH'] = abspath(join(dirname(__file__), './python-leap-ctypes/', 'dll'))

# Import leap
from cleap.leap import *

# setup leap controller
controller = leap_controller()
listener = leap_listener(500)
leap_add_listener(controller, listener)
leap_enable_background(controller)


try:
  # sinewave
  volume = -20
  pitch = 12
  sinewave = SineWave(pitch = pitch, decibels = volume, decibels_per_second = 20, pitch_per_second = 20)
  sinewave.play()

  print("move your hands around\n")

  counter = 0
  last_update = datetime.now()
  while counter < 3000:
    waiting = False
    while not waiting:
      event = leap_poll_listener(listener)
      if event:
        e = Event(event)
        counter += 1

        if any(e.frame.hands):
          last_update = datetime.now()

          volume = int(e.frame.hands[0].palm_position.points[1] / 10 * -1) # left hand, y coordinate
          sinewave.set_volume(volume)

          if len(e.frame.hands) > 1:
            pitch = e.frame.hands[1].palm_position.points[0] / 10 # right hand, x coordinate
            sinewave.set_pitch(pitch)
          print("\rvolume: %d, pitch: %d               " % (volume, pitch), end = '', flush = True)

          # points = e.frame.hands[0].palm_position.points
          # print("\rx: %d, y: %d, z: %d " % (points[0], points[1], points[2]), end = '', flush = True)
          # print(e.frame.hands[0].palm_position)


      else:
        waiting = True
        if datetime.now() > (last_update + timedelta(seconds = 2)):
          print("\r                                        ", end = '', flush = True)
finally:
  sinewave.stop()

print('')

leap_remove_listener(controller, listener)
leap_listener_dispose(listener)
leap_controller_dispose(controller)
