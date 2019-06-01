
from __future__ import division

from UDPComms import Subscriber, timeout
from roboclaw_interface import RoboClaw
import math
import time


def find_serial_port():
    return '/dev/serial0'

class Arm:
    def __init__(self):
        self.target_vel = Subscriber(8410)

        self.motor_names = ["spinner"]
        self.pwm_names = ["led"]

        self.CPR = {'spinner':1294}
        self.oneShot = 0
        self.rc = RoboClaw(find_serial_port(), names = self.motor_names + self.pwm_names,\
                                                    addresses = [128])
	self.pos = 0
	self.offset = 0
       
        while 1:
            start_time = time.time()
            self.update()
            while (time.time() - start_time) < 0.1:
                pass


    def update(self):
        try:
            print()
            print("new iteration")
            target = self.target_vel.get()
            # TODO: This shouldn't be necessary, how to fix in UDPComms?
            target = {bytes(key): value for key, value in target.iteritems()}
            print(target)
            target_f = target

            if(target_f['grip'] == -1):
                self.rc.drive_duty("led", -30000)
            else:
                self.rc.drive_duty("led", 0)

            if math.fabs(target_f['yaw']) > 0.1:
                self.offset += 100*target_f['yaw']

            if(target_f['roll'] == 1 and self.oneShot == 0):
                self.pos = self.pos + 1
                self.oneShot = 1
            elif(target_f['roll'] == -1 and self.oneShot == 0):
                self.pos = self.pos - 1
                self.oneShot = 1
            if(target_f['roll'] == 0):
                self.oneShot = 0
	
            if target_f["reset"]:
                print ("RESETTING!!!")
                self.rc.set_encoder('spinner',0)
                self.pos = 0
                self.offset = 0

            self.rc.drive_position('spinner',int(self.pos*self.CPR['spinner'] + self.offset))
        except timeout:
            print ("No commands") 


if __name__ == "__main__":
    a = Arm()
