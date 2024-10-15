import time
import sys
import RPi.GPIO as GPIO

def main():
    PIN = 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN , GPIO.OUT)
    BZ = GPIO.PWM(PIN, 400)
    BZ.start(50)
    time.sleep(10)
    BZ.cleanup(PIN)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt :
        print("!!Exit!!")
        sys.exit()
