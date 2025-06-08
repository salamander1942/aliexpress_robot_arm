from math import *
import json

class Robot_arm():
    def __init__(self, a_length, b_length, gear_ratio):
        self.a_length = a_length
        self.b_length = b_length
        self.gear_ratio = gear_ratio
        try:
            with open('robot_arm_data.json', 'r') as file:
                self.Prev_angle = json.load(file)
                print('loadad data from the file')
        except:
            print('file failed to load data')
    # Put the explanation code here with the str or print thing

    
    def goto_XYZ(self,posX,posY,posZ):
        # make a variable to store the return angles
        return_angles = []
        # this block finds the first angle, angle C, diageram of arm is needed https://websitelink.com/diagrams/robotarm1
        c_square = (posX**2)+(posY**2)+(posZ**2)
        
        # check to see if valid arm position, if not terminate
        if sqrt(c_square) > (self.a_length+self.b_length):
            raise robo_arm_aint_long_enough
        
        # continue with calculations
        angle_C = acos(((self.a_length**2)+(self.b_length**2)-c_square)/(2*self.a_length*self.b_length))
        angle_B = asin((self.b_length*sin(angle_C))/sqrt(c_square))
        
        # find full z anglle
        angle_Z = asin(posZ/sqrt(c_square))
        angle_ZB = angle_B + angle_Z
        
        # print out angles to see if the math is mathing, its more difficult because i do not understand radians
        print('angle Z+B : ',degrees(angle_ZB))
        return_angles.append(degrees(angle_ZB)) 
        print('angle C : ',degrees(angle_C))
        return_angles.append(degrees(angle_C))
        
        # now find the rotation of the base
        try:
            angle_Y = asin(posY/sqrt((posX**2)+(posY**2)))
        except ZeroDivisionError:
            angle_Y = 0
        angle_Y = degrees(angle_Y)
        
        # acount for the 4 quadrents
        if (posX >= 0) and (posY >= 0):
            return_angles.append(angle_Y)
            print(f"1angle Y : {angle_Y}")
        elif (posX < 0) and (posY >= 0):
            print(f"2angle Y : {180-angle_Y}")
            return_angles.append(180-angle_Y)
        elif (posX >= 0) and (posY < 0):
            print(f"3angle Y : {360+angle_Y}")
            return_angles.append(360+angle_Y)
        else:
            print(f"4angle Y : {angle_Y+270}")
            return_angles.append(270+angle_Y)
        print()

        # do at end if movement is sucsesfull
        self.posX = posX
        self.posY= posY
        self.posZ = posZ
        
        # store previous angles
        self.Prev_angles = return_angles
        try:
            with open('robot_arm_data.json','w') as file:
                json.dump(self.Prev_angles, file)
                print('DATA HAS BEEN DUMPED')
        except:
            print('DATA FAILED TO DUMP')
        # return list
        return return_angles
    
    def position(self):
        try:
            return [self.posX,self.posY,self.posZ]
        except:
            return None
        
    def angles(self):
        try:
            return self.Prev_angles
        except:
            return None
        
        
if __name__=='__main__':
    '''
    Prev_angles = [90,90,90]
    with open('robot_arm_data.json', 'w') as file:
        json.dump(Prev_angles, file)
        print('did it')
    '''
    arm = Robot_arm(8,8,1)
    angles = arm.goto_XYZ(7.5,0,0)
    print(arm.position())
