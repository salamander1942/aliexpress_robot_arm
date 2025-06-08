import robot_arm
import machine
import time

class Robot_arm_servo(robot_arm.Robot_arm):
    def __init__(self, length_A, length_B, gear_ratio, ZB_pin, C_pin, Y_pin, claw):
        # initilize super class of robot arm
        
        super().__init__(length_A, length_B, gear_ratio)
        
        # initalize servo pins
        
        self.servoZB = machine.PWM(machine.Pin(ZB_pin, machine.Pin.OUT))
        self.servoC = machine.PWM(machine.Pin(C_pin, machine.Pin.OUT))
        self.servoY = machine.PWM(machine.Pin(Y_pin, machine.Pin.OUT))
        self.servoClaw = machine.PWM(machine.Pin(claw, machine.Pin.OUT))
        
        # Initialize duty cycles
        
        self.servoZB.freq(50)
        self.servoC.freq(50)
        self.servoY.freq(50)
        self.servoClaw.freq(50)
        
        # place items into list for convinient use
        # sory claw is excluded, but here it is just in case self.servoClaw

        self.servos = [self.servoZB, self.servoC, self.servoY]

        # servo tunes, for some reason the servos im useing are garbage

        self.servoZB_tune = [130, 60]
        self.servoC_tune = [21, 125]
        self.servoY_tune = [33, 130]
        
        # put servo tunes into convient list
        # again claw is excluded, cuz i hate the claw
        
        self.servo_tunes = [self.servoZB_tune, self.servoC_tune, self.servoY_tune]
        
    def __str__(self):
        return 'Servo library for the AliExpress robotic arm'
    
    def map(self,x, in_min, in_max, out_min, out_max):
        return round(((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min),2)
    
    def arm_servo_goto(self, angles_list, old_list):
        
        #account for arm geometry in calc
        old_list[1] = (old_list[0] + old_list[1])
        angles_list[1] = (angles_list[0] + angles_list[1])
        
        # first calculate how many pwm diff there is, then find the longest one for time ref
        servo_duty_angles = [self.map(angles_list[i], 0, 180, self.servo_tunes[i][0], self.servo_tunes[i][1]) for i in range(0,3)]
        
        # now with duties, use same method to find old servo duty cycles

        old_servo_duty_angles = [self.map(old_list[i], 0, 180, self.servo_tunes[i][0], self.servo_tunes[i][1]) for i in range(0,3)]
                    
        # Find the difference in duty cycles with a while loop
        
        servoAngleDiff = [ servo_duty_angles[x] - old_servo_duty_angles[x] for x in range(0,len(servo_duty_angles))]
        
        largest_value = abs(max(servoAngleDiff))

        for x in range(1,largest_value):
            for servo in range(0,len(servoAngleDiff)):
                q = (servoAngleDiff[servo]*x)/largest_value
                print(int(q),end=' ')
                self.servos[servo].duty(int(old_servo_duty_angles[servo]+q))
                print(int(q),end=' ')
            time.sleep(1)
            # usually .04
            print()


    def tune_servos(self, servo_number):
        servos = {
            "SERVO_ZB": self.servoZB,
            "SERVO_C": self.servoC,
            "SERVO_Y": self.servoY,
            # Add more servos as needed
        }

        if servo_number in servos:
            servo = servos[servo_number]
            tune_values = {
                "180": None,
                "0": None,
            }

            for position in ["180", "90"]:
                repeat = True
                while repeat:
                    servo_pos = input(f'Input a PWM around 20 - 180 for {position} degrees, then input "done" when reached: ')
                    if servo_pos.lower() == "done":
                        try:
                            tune_values[position] = prev_input
                        finally:
                            repeat = False
                    else:
                        servo.duty(int(servo_pos))
                        prev_input = servo_pos

            # Store the tune values
            if servo_number == "SERVO_ZB":
                self.servoZB_tune = tune_values
            elif servo_number == "SERVO_C":
                self.servoC_tune = tune_values
            elif servo_number == "SERVO_Y":
                self.servoY_tune = tune_values

            print('Done!')
        else:
            print("Invalid servo number")

    def goto_pos(self, quardX, quardY, quardZ):
        
        # first i want to account for prev position, if none is returned, asume defult positon of 0,8,8
        
        if self.angles() == None:
            self.goto_XYZ(0,8,8)
        old_list = self.angles()
        servo_angles = self.goto_XYZ(quardX, quardY, quardZ)
        self.arm_servo_goto(servo_angles, old_list)
            
        

if __name__=='__main__':
        length_A = 8
        length_B = 8
        gear_ratio = 1
        ZB_pin = 15
        C_pin = 19
        Y_pin = 18
        claw = 33
        arm = Robot_arm_servo(length_A, length_B, gear_ratio, ZB_pin, C_pin, Y_pin, claw)
        
        for x in range(-8,8):
            for y in range(5,8):
                arm.goto_pos(x,y,1)
            time.sleep(1)
            arm.goto_pos(x,5,1)
            
        for y in range(5,8):
            for x in range(-8,8):
                arm.goto_pos(x,y,1)
            time.sleep(1)
            arm.goto_pos(-8,y,1)
        
        




        

    
    
    


        



