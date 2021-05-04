# This code is used as a test to determine whter the robot is capable of turning 
# through the use of its compass, rather than the encoders.

# import L2_log as log
# import time
import numpy as np
# import L1_encoder as enc
# import L2_kinematics as kin
# import L2_speed_control as sc
# import L2_inverse_kinematics as inv
# import L2_vector as vect
import L2_heading as head
import time



C = 0

# def drive(xd,td, t):           #drive toward POI unless object detected
#     myVelocities = np.array([xd, td]) #input your first pair
#     myPhiDots = inv.convert(myVelocities)
#     sc.driveOpenLoop(myPhiDots)
#     time.sleep(t) # input your duration (s)
    
def turn(A):
    axes = head.getXY()  
    axesScaled = head.scale(axes) 
    h1 = head.getHeading(axesScaled)                  # compute the heading
    headingDegrees1 = round(h1*180/np.pi, 2)
    print("h1: ", headingDegrees1)
    if (A<0):
        i = -1
        j = 360
        headingDegrees2 = 360
        while((headingDegrees2 - headingDegrees1) > A):
            #drive(0,i*2,0.001)
            axes = head.getXY()  
            axesScaled = head.scale(axes) 
            h2 = head.getHeading(axesScaled)                  # compute the heading
            headingDegrees2 = round(h2*180/np.pi, 2)
            print("h2: ", headingDegrees2)
            print("theta: ", headingDegrees2 - headingDegrees1)
            time.sleep(0.01) 
    elif(A>0):
        i = 1
        j = 0
        headingDegrees2 = -360
        while((headingDegrees2 - headingDegrees1) < A):
            #drive(0,i*2,0.001)
            axes = head.getXY()  
            axesScaled = head.scale(axes) 
            h2 = head.getHeading(axesScaled)                  # compute the heading
            headingDegrees2 = round(h2*180/np.pi, 2)
            print("h2: ", headingDegrees2)
            print("theta: ", headingDegrees2 - headingDegrees1)
            time.sleep(0.01) 
    
turn(-45)
print("CLICK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
turn(45)
