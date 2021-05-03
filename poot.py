# this program will turn the robot 45° left or right depending on where the object it detected was
# and go straight if nothing is detected
# since we are using the compass to calculate changes, the math can get janky if it is turning from -175 to +160 for example

# Import Internal Programs
import L2_vector as vect
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L2_heading as heading
# Import External programs
import numpy as np
import time


def go(array, delay):
    myVelocities = np.array(array) #turn right
    myPhiDots = inv.convert(myVelocities)
    sc.driveOpenLoop(myPhiDots)
    time.sleep(delay) # input your duration (s)


k = 0   # evasive manuever variable

print("hiiiii :3")

while (1):
     
    vector = vect.getNearest()
    distance = vector[0]
    angle = vector[1]
    x = 0.17    # distance form robot to object 
   
    print ("                             ",distance,"m", angle,"deg?")
    
    if(distance > x):
        go([1.4,0], 0)                                      # go forwards
        print("im going forwards :)")
  
    else:
        go([0,0], 0)                                        # pause
        print("object detected")
   
    if(distance < x):
            go([-1.4,0], 1)                                 # go backwards
            print("backing up for 1 second")
            
            if(angle > 0):                                  # object on right side
                
                print("object on right side, turn LEFT")
                turn = 0
                heading1 = heading.currentHeading()         # get heading before turn
                
                while(turn <= 45):                          # gonna turn 45 deg
                    go([0,1.57], 0)                         # start turning left
                    k = 1                                   # evasive manuever executed
                    heading2 = heading.currentHeading()     # keep updating new heading
                    print("heading1: ",heading1,"heading2; ",heading2)
                    if(-135 <= heading1 <= 135):            # math safe zone
                        turn = abs(heading1 - heading2)
                        print("safe left turn status: ",turn," heading: ",heading2)
                        
                    elif( ((heading1 < 0) and (heading2 < 0)) or ((heading1 > 0) and (heading2 > 0))):
                        turn = abs(heading1 - heading2)
                        print("kinda dangerous turn status: ",turn," heading: ",heading2)                        
                    else:                                   # if it goes from neg to pos
                        turn = 360 - (abs(heading1 - heading2))
                        ("danger left turn status: ",turn," heading: ",heading2)

                k = 1                                       # evasive manuever variable
                    
                    

            if(angle < 0):  #object on the left side
                
                print("object on left side, turning RIGHT")
                turn = 0
                heading1 = heading.currentHeading()         # get heading before turn
                
                while(turn <= 45):                          # gonna turn 45 deg
                    go([0,-1.57], 0)                        # start turning right
                    k = 1                                   # evasive manuever executed
                    heading2 = heading.currentHeading()     # keep updating new heading
                    print("heading1: ",heading1,"heading2; ",heading2)

                    if(-135 <= heading1 <= 135):            # math safe zone
                        turn = abs(heading1 - heading2)
                        print("safe right turn status: ",turn," heading: ",heading2)

                    elif( ((heading1 < 0) and (heading2 < 0)) or ((heading1 > 0) and (heading2 > 0))):
                        turn = abs(heading1 - heading2)
                        print("kinda dangerous turn status: ",turn," heading: ",heading2)

                    else:                                   # if it goes from neg to pos
                        turn = 360 - (abs(heading1 - heading2))                           # evasive manuever executed
                        print("danger right turn status: ",turn," heading: ",heading2)

                k = 1                                       # evasive manuever variable



