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
import danny as dan
import poi as poi
import trash as trash





origin = 0              #Location of the robot
Xp = poi.facePOI()       #turn and face POI and return the distance to it
while(Xp > 0):
#if(True):
    Data = dan.forward_track(Xp)    #goes forward while tracking the distance is has moved until it hits an object
    print("Data: ", Data)
    #Xp = Xp - Data[0]
    Xp = trash.turnAfterAvoidance(Data[0], Data[1])
    #print("X_Prime: ", Xp)
    
    
print("POI FOUND!!!!!!!!!")
