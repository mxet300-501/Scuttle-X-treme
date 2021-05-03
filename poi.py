import L2_log as log
import time
import numpy as np
import L1_encoder as enc
import L2_kinematics as kin
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L2_vector as vect
import L2_speed_control as sc
import L2_heading as heading
# Import External programs
import numpy as np
import time

def go(array,delay):
    myVelocities = np.array(array) #input your first pair
    myPhiDots = inv.convert(myVelocities)
    sc.driveOpenLoop(myPhiDots)
    time.sleep(delay) # input your duration (s)

def turn(array, alpha):                                 #turn based off heading angle
    turn = 0
    heading2 = heading.currentHeading()
    heading1 = heading.currentHeading()
    while((-1*alpha) <= turn <= alpha):                          # gonna turn 45 deg
        go(array, 0)                          # start turning
        k = 1                                   # evasive manuever executed
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
    go([0,0],0.1)                                #pause for half a second
    print("turn done")
    


def facePOI():
    heading1 = 0
    heading2 = 0
    print("X: ")
    x = float(input())
    print("Y: ")
    y = float(input())
    
    r = np.sqrt(x**2 + y**2)                # distance to POI
    alpha = np.arctan(y/x) * 180/np.pi      #  to degrees 
    alpha = round(np.absolute(alpha),2)
    
    
    print("r: ",r)
    print("alpha: ",alpha)
    
    while(1):
    
        print("inside while loop")
        
        if((x > 0) and (y > 0)):         #1st quad, turn left alpha
                
            print("1st quad")
            heading1 = heading.currentHeading()
            turn([0,2], alpha)        #turn left alpha
            
            
        elif((x < 0) and (y > 0)):       #2nd quad, turn left 90 + (90 - alpha)
    
            print("2nd quad")
            heading1 = heading.currentHeading()
            moreAlpha = 90 - alpha
            turn([0,2], 90)        #turn left ninety
            heading1 = heading.currentHeading()
            turn([0,2],moreAlpha)        #turn left 90 - alpha
        
        elif((x < 0) and (y < 0)):       #3rd quad, turn right 90 + (90 - alpha)
            
            print("3rd quad")
            heading1 = heading.currentHeading()
            moreAlpha = 90 - alpha
            turn([0,-2], 90)        #turn right ninety
            heading1 = heading.currentHeading()
            turn([0,-2],moreAlpha)        #turn right 90 - alpha
        
        elif((x > 0) and (y < 0)):       #4th quad, turn right alpha
            
            print("4th quad")
            heading1 = heading.currentHeading()
            turn([0,-2], alpha)        #turn left alpha
            
            
        elif((x == 0) and (y > 0)):      #90 deg to the left 
    
            print("90 left")
            heading1 = heading.currentHeading()
            turn([0,2], 90)        #turn left alpha
        
        elif((x == 0) and (y < 0)):      #90 deg to the right           
            
            print("90 right")
            heading1 = heading.currentHeading()
            turn([0,-2], 90)        #turn right alpha
            
        elif((x < 0) and (y == 0)):      #directly behind
    
            print("behind")
            heading1 = heading.currentHeading()
            turn([0,-2], 90)        #turn right 90
            print("turned 90 once")
            turn([0,-2], 90)        #turn right 90
            print("turned 90 twice")
    
        else:                            #forwards!!
            print("else")
        
        return r
