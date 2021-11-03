import RPi.GPIO as GPIO
import time
GPIO.cleanup()
ang = 0
dc = 0.
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(8) # Initialization
try:
  while True:
    ang = int(input('Enter angle in degrees'))
    print('Angle - '+str(ang))
    dc = ang/18.+3.
    print('Duty Cycle - '+str(dc))
    p.ChangeDutyCycle(dc)
    time.sleep(0.5)
    #p.ChangeDutyCycle(2.5)
    #time.sleep(3)
    #p.ChangeDutyCycle(12.5)
    #time.sleep(3)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
