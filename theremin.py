import os
import sys
from datetime import datetime, timedelta
from os.path import dirname, join, abspath
from pysinewave import SineWave

# leap lib
sys.path.append(join(dirname(__file__), './lib/'))

# Set DLL path for leap libraries
os.environ['LEAP_DLL_PATH'] = abspath(join(dirname(__file__), './lib/', 'dll'))

# Import leap
import Leap


# globals
volume = -100
pitch = 0
tone = SineWave(pitch = pitch, decibels = volume, decibels_per_second = 50, pitch_per_second = 40)


class SampleListener(Leap.Listener):
    # def on_init(self, controller):
    #     print("Initialized")

    # def on_connect(self, controller):
    #     print("Connected")

    #     Enable gestures
    #     controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
    #     controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
    #     controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
    #     controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        global volume
        global pitch
        frame = controller.frame()

        if frame.hands.is_empty:
            print("\r                                        ", end = '', flush = True)
            update_tone(-100, 0)
        else:
            for hand in frame.hands:
                # left hand volume
                if hand.is_left:
                    volume = int(hand.palm_position[1] / 5 ) - 100 # y coordinate, with an offset

                # right hand pitch
                else:
                    pitch = (hand.palm_position[0] / 5) - 5 # x coordinate, with an offset

            print("\rvolume: %d, pitch: %d               " % (volume, pitch), end = '', flush = True)
            update_tone(volume, pitch)


def update_tone(volume, pitch):
    tone.set_volume(volume)
    tone.set_pitch(pitch)


def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("This is a Theremin!")
    print("Use your left hand to control volume and your right hand to control pitch")

    # start the silent tone
    tone.play()

    print("\nPress Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        tone.stop()
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
