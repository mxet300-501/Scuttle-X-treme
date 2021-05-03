#This code was an attempt to correct the robot's heading through reactive means on a chassis level basis
#If the encoders read that the robot was veering right, it would actively turn left and vice versa

import L2_displacement as dis
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L1_encoder as enc                    # local library for encoders
import numpy as np                          # library for math operations
import time

encoders = enc.read()                       # grabs the current encoder readings before beginning
    
# initialize variables at zero
x = 0                                       # x
t = 0                                       # theta
encL1 = 0
encR1 = 0
res = (360/2**14)                           # resolution of the encoders

while True:
    encL0 = encL1                           # transfer previous reading.
    encR0 = encR1                           # transfer previous reading.
    encoders = enc.read()                   # grabs the current encoder readings, raw
    encL1 = round(encoders[0], 1)           # reading, raw.
    encR1 = round(encoders[1], 1)           # reading, raw.
    
    encoders = enc.read()                   # grabs the current encoder readings, raw
    encL1 = round(encoders[0], 1)           # reading, raw.
    encR1 = round(encoders[1], 1)           # reading, raw.
        
    # ---- movement calculations
    travL = dis.getTravel(encL0, encL1) * res   # grabs travel of left wheel, degrees
    travL = -1 * travL                      # this wheel is inverted from the right side
    travR = dis.getTravel(encR0, encR1) * res   # grabs travel of right wheel, degrees
        
    # build an array of wheel travels in rad/s
    travs = np.array([travL, travR])        # store wheels travel in degrees
    travs = travs * 0.5                     # pulley ratio = 0.5 wheel turns per pulley turn
    travs = travs * 3.14 / 180              # convert degrees to radians
    travs = np.round(travs, decimals=3)     # round the array
            
    chass = dis.getChassis(travs)               # convert the wheel travels to chassis travel
    x = x + chass[0]                        # add the latest advancement(m) to the total
    t = t + chass[1]
    print("x(m)", x)                        # print x in meters
    print("t(rad)", t)                        # print theta in radians
    time.sleep(.001)
        
    if(t>0):
        myVelocities = np.array([1.4, -8]) #input your first pair
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
        print("Turning right")
        time.sleep(0.001) # input your duration (s)
    elif(t<0):
        myVelocities = np.array([1.4, 8]) #input your first pair
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
        print("Turning left")
        time.sleep(0.001) # input your duration (s)
    else:
        myVelocities = np.array([1.4, 0]) #input your first pair
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
        print("Going straight")
        time.sleep(0.001) # input your duration (s)
