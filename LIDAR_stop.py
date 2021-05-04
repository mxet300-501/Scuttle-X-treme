# This progam makes scuttle drive forwards until object is detected, then back up and turn left or right if an object is detected.
# It then repeats this process in an infinite loop, avoiding objects and driving forwards.
# Mainly, this code represented a checkpoint in the programming of the final project; we could run this code to make sure
# that the LIDAR, motors, and encoders were working as expected.


# Import Internal Programs
import L2_vector as vect
import L2_speed_control as sc
import L2_inverse_kinematics as inv

# Import External programs
import numpy as np
import time

while (1):
    vector = vect.getNearest()
    distance = vector[0]
    angle = vector[1]
    x = 0.16    # distance form robot to object 
    print (distance, angle)
    if(distance > x):
        myVelocities = np.array([1, -3])
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
    else:
        myVelocities = np.array([0, 0])
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)

    if(distance < x):
            myVelocities = np.array([-1, 3]) #input your first pair
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
            time.sleep(1.5) # input your duration (s)
            
            if(angle > 0):  #object on right side
                myVelocities = np.array([0, 1.57]) #turn left
                myPhiDots = inv.convert(myVelocities)
                sc.driveOpenLoop(myPhiDots)
                time.sleep(1) # input your duration (s)
                
            if(angle < 0):  #object on the left side
                myVelocities = np.array([0, -1.57]) #turn right
                myPhiDots = inv.convert(myVelocities)
                sc.driveOpenLoop(myPhiDots)
                time.sleep(1) # input your duration (s)
