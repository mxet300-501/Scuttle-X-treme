import L2_log as log
import time
import numpy as np
import L1_encoder as enc
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L2_vector as vect
import L2_displacement as dis
import L2_heading as heading
import poi as poi

def turn(array, alpha):
    heading2 = heading.currentHeading()
    heading1 = heading.currentHeading()
    turn = 0
    while((-1*alpha) <= turn <= alpha):         # gonna turn 45 deg
        myVelocities = np.array(array) #turn right
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
        time.sleep(0) # input your duration (s)        k = 1                                   # evasive manuever executed
        heading2 = heading.currentHeading()     # keep updating new heading
        
        print("heading1: ",heading1,"heading2; ",heading2)
        
        if(-135 <= heading1 <= 135):            # math safe zone
            turn = (heading2 - heading1)
            print("safe left turn status: ",turn," heading: ",heading2)
                    
        elif( ((heading1 < 0) and (heading2 < 0)) or ((heading1 > 0) and (heading2 > 0))):
            turn = (heading2 - heading1)
            print("kinda dangerous turn status: ",turn," heading: ",heading2)  
            
        else:                                   # if it goes from neg to pos
            turn = 360 - ((heading2 - heading1))
            print("danger left turn status: ",turn," heading: ",heading2)
    poi.go([0,0],0.5)                                #pause for half a second
    print("turn done")

x = 0.17        # distance from robot to object


def forward_D2K(K):
    D = 0
    #K = 1
    i = 0
    global x
    while(D <= K):
        vector = vect.getNearest()
        distance = vector[0]
        angle = vector[1]
        D = dis.move_detect(D)
        print("D: ", D, "\n", "\r")
        if(distance < x):
            print("Object detected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            i = 1
            dis.move(-D, 1)
            # myVelocities = np.array([1, -3]) #input your first pair
            # myPhiDots = inv.convert(myVelocities)
            # sc.driveOpenLoop(myPhiDots)
            # time.sleep(0.000000) # input your duration (s)
            print("Done backing up")
            break
    return D, i
            



def forward_until_obj():     #goes forward until object is detected and turn reaction
    i = 0
    while (i == 0):
        vector = vect.getNearest()
        distance = vector[0]
        angle = vector[1]
        global x
        print (distance, angle)
        if(distance > x):
            myVelocities = np.array([1.4, 0])
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
        else:
            myVelocities = np.array([0, 0])
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
            i = 1
    if(distance < x):
        dis.move(-0.5, 1.8)
            
        if(angle > 0):  #object on right side
            heading1 = heading.currentHeading()
            turn([0,2], 45)        #turn left 45

                
        if(angle < 0):  #object on the left side
            heading1 = heading.currentHeading()
            turn([0,-2], 45)        #turn right 45

def forward_track(r):       #goes forward while tracking the distance is has moved until it hits an object
    D = 0                   #distance counter
    K = 0.5               #distance to go forward after correction
    B = 0.25                 #distance it backs up
    i = 0                   #condition counter
    heading1 = 0
    heading2 = 0
    global x
    while(D <= r):
        vector = vect.getNearest()
        distance = vector[0]
        angle = vector[1]
        D = dis.move_detect(D)
        Xprime_remaining = r - D            #the distance nedded to travel of X_prime
        #r = r - D
        print("Xprime_remaining: ", r)
        print("D: ", D, "\n", "\r")
        if(distance < x):
            print("Object detected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            dis.move(-B, 1)
            # myVelocities = np.array([1, -3]) #input your first pair
            # myPhiDots = inv.convert(myVelocities)
            # sc.driveOpenLoop(myPhiDots)
            # time.sleep(0.000000) # input your duration (s)
            print("Done backing up")
            print("Angle: ", angle)
            if(angle > 0):  #object on right side
                print("Turn Left")
                i = 1
                heading1 = heading.currentHeading()
                turn([0,2], 75)        #turn left 45
                I = forward_D2K(K)
                print("I: ", I)
                # if(I[1] == 1):
                #     print("Turn Left Again")
                #     i = 2
                #     heading1 = heading.currentHeading()
                #     turn([0,2], 45)        #turn left 45
                #     I = forward_D2K(K)

            if(angle < 0):  #object on the left side
                print("Turn Right")
                i = 3
                heading1 = heading.currentHeading()
                turn([0,-2], 64)        #turn right 45
                I = forward_D2K(K)
                print("I: ", I)
                # if(I[1] == 1):
                #     print("Turn Right Again")
                #     i = 4
                #     heading1 = heading.currentHeading()
                #     turn([0,-2], 45)        #turn right 45
                #     I = forward_D2K(K)
            return Xprime_remaining, i
            break


if __name__ == "__main__":
    #turn([0,2],70)
    dis.move(1.5, 1)
