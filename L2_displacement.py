# This program takes the encoder values from encoders, computes wheel movement
# calculates the chassis displacement and continuously adds up the displacement
# to indicate how much the robot has advanced, in meters.
import L2_vector as vect
import L2_speed_control as sc
import L2_inverse_kinematics as inv
import L1_encoder as enc                    # local library for encoders
import numpy as np                          # library for math operations
import time                                 # library for time access

# define kinematics
R = 0.041                                   # radius in meters
L = 0.201                                   # half of wheelbase meters
res = (360/2**14)                           # resolution of the encoders
roll = int(360/res)                         # variable for rollover logic
gap = 0.5 * roll                            # degress specified as limit for rollover

A = np.array([[R/2, R/2], [-R/(2*L), R/(2*L)]])     # This matrix relates [PDL, PDR] to [XD,TD]
wait = 0.02                                 # wait time between encoder measurements (s)

def getTravel(deg0, deg1):                  # calculate the delta on Left wheel
    trav = deg1 - deg0                      # reset the travel reading
    if((-trav) >= gap):                     # if movement is large (has rollover)
        trav = (deg1 - deg0 + roll)         # forward rollover
    if(trav >= gap):
        trav = (deg1 - deg0 - roll)         # reverse rollover
    return(trav)

def getChassis(disp):                       # this function returns the chassis displacement
    B = disp                                # this array should store phi displacements (in radians)
    C = np.matmul(A, B)                     # perform matrix multiplication
    C = np.round(C, decimals=3)             # round the matrix
    return(C)                               # returns a matrix containing [dx, dTheta]

encoders = enc.read()                       # grabs the current encoder readings before beginning

# initialize variables at zero
x = 0                                       # x
t = 0                                       # theta
encL1 = 0
encR1 = 0

# this loop continuously adds up the x forward movement originating from the encoders.
def move(distance, speed):
    encoders = enc.read()                       # grabs the current encoder readings before beginning
    
    # initialize variables at zero
    x = 0                                       # x
    t = 0                                       # theta
    encL1 = 0
    encR1 = 0
    if(distance > 0):
        while (x < distance):
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
            x = x + chass[0]                        # add the latest advancement(m) to the total
            t = t + chass[1]
            print("x(m)", x)                        # print x in meters
            print("theta", t)                                # print theta in radians
            time.sleep(.0001)
        
            myVelocities = np.array([speed, 0]) #input your first pair
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
            time.sleep(0.00001) # input your duration (s)
            
    elif(distance < 0):
        while (x > distance):
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
            x = x + chass[0]                        # add the latest advancement(m) to the total
            t = t + chass[1]
            print("x(m)", x)                        # print x in meters
            print("theta", t)                                # print theta in radians
            time.sleep(.000001)
        
            myVelocities = np.array([-speed, 0]) #input your first pair
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
            time.sleep(0.0000001) # input your duration (s)



def move_detect(D):      #move forward while looking for object
    #x = 0                                       # x
    t = 0                                       # theta
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
    print("x(m)", D)                        # print x in meters
    print("theta", t)                                # print theta in radians
    time.sleep(.0001)
        
    myVelocities = np.array([1, 0]) #input your first pair
    myPhiDots = inv.convert(myVelocities)
    sc.driveOpenLoop(myPhiDots)
    time.sleep(0) # input your duration (s)
    return D


def forward_time(K):
    t1 = time.monotonic()
    x = 0                                       # x
    th = 0                                       # theta
    encL1 = 0
    encR1 = 0
    speed = 1
    while (x <= K):
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
        x = x + chass[0]                        # add the latest advancement(m) to the total
        th = th + chass[1]
        print("x(m)", x)                        # print x in meters
        print("theta", th)                                # print theta in radians
        time.sleep(.000001)
        
        myVelocities = np.array([speed, -3]) #input your first pair
        myPhiDots = inv.convert(myVelocities)
        sc.driveOpenLoop(myPhiDots)
        time.sleep(0.0000001) # input your duration (s)
        
        vector = vect.getNearest()
        distance = vector[0]
        angle = vector[1]
        if(distance < 0.17):
            t2 = time.monotonic()
            t = t2 - t1
            myVelocities = np.array([-speed, 3]) #input your first pair
            myPhiDots = inv.convert(myVelocities)
            sc.driveOpenLoop(myPhiDots)
            time.sleep(t) # input your duration (s)
            break


if __name__ == "__main__":
    move(1, 1.4)
    move(-1, 1.4)
    D = 0
    while(1):
        D += move_detect(D)
        print("D: ", D)
    K = 1
    forward_time(K)
