import RPi.GPIO as GPIO
import time
from UDPComms import Subscriber, timeout

bucket_pin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(bucket_pin, GPIO.OUT)

bucket = GPIO.PWM(bucket_pin, 50)

bucket.start(0)

def clamp(x,ma,mi):
    if x > ma:
        return ma
    elif x < mi:
        return mi
    else:
        return x

def send(num):
    print "sending", num
    bucket.ChangeDutyCycle(num)
    time.sleep(0.5)
    bucket.ChangeDutyCycle(0)

send(4)
send(10)


bucket.stop()
GPIO.cleanup()

# while True:
#     time.sleep(0.1)
#     changed = False
#     try:
#         msg = sub.get()
#         bucket_angle = clamp(pan_angle + msg['pan'], 90, -90)

#         if (msg['pan'] != 0):
#             changed = True
#     except timeout:
#         pass

#     if changed:
#         bucket.ChangeDutyCycle(8.5 - bucket_angle*5.5/90)
#     else:
#         bucket.ChangeDutyCycle(0)

