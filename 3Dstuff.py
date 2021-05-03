import L2_displacement as dis
import numpy as np
import time
import L1_encoder as enc
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L1_mpu as mpu

c = 0

def detect(D):      #move forward while looking for object
    t = 0                                   # theta
    encL1 = 0
    encR1 = 0
    encL0 = encL1                           # transfer previous reading.
    encR0 = encR1                           # transfer previous reading.
    encoders = enc.read()                   # grabs the current encoder readings, raw
    encL1 = round(encoders[0], 1)           # reading, raw.
    encR1 = round(encoders[1], 1)           # reading, raw.
        
    # ---- movement calculations
    travL = getTravel(encL0, encL1) * res   # grabs travel of left wheel, degrees
    travL = -1 * travL                      # this wheel is inverted from the right side
    travR = getTravel(encR0, encR1) * res   # grabs travel of right wheel, degrees
    
    # build an array of wheel travels in rad/s
    travs = np.array([travL, travR])        # store wheels travel in degrees
    travs = travs * 0.5                     # pulley ratio = 0.5 wheel turns per pulley turn
    travs = travs * 3.14 / 180              # convert degrees to radians
    travs = np.round(travs, decimals=3)     # round the array
        
    chass = getChassis(travs)               # convert the wheel travels to chassis travel
    D = D + np.absolute(chass[0])                    # add the latest advancement(m) to the total
    t = t + chass[1]
    #print("x(m)", D)                        # print x in meters
    #print("theta", t)                       # print theta in radians
    return D

while True:
    axes = mpu.getAccel()
    #print("accel(m/s^2):", axes)
    x = axes[0]
    y = axes[1]
    z = axes[2]
    
    alpha = np.arctan(x/z) * 180 / np.pi
    beta = np.arctan(y/z) * 180 / np.pi
    gamma = np.arctan(x/y) * 180 / np.pi
    #print("alpha:",alpha," beta:",beta," gamma:",gamma)
    
        
    c = dis.move_detect(c)
    a = 0
    
    if(beta > 7):
        print("up")
        a += c * np.cos(beta)
    elif(beta < -7):
        print("down")
        a += c * np.cos(-1 * beta)
    else:
        print("level")
        a += c
    print("a:",a)
    time.sleep(0.25)
