import math
import numpy as np
import poi as poi
# enter poi coords
# facePOI
# go to POI
# danny.py
# record how far it went while avoiding obstacle, add/subtract it from poi coords
# facePOI
# loop again

def turnAfterAvoidance(x, counter):
    
    b = 0.25
    k = 0.75
    theta = 45
    print("x: ", x)
    if (counter == 3):              #4                 # face POI by turning right, one turn
        alpha = np.pi - (np.arctan((x + b) / k))
        alpha = alpha*(180/np.pi)*.7111
        xP = np.sqrt((x + b)**2 + k**2)
        poi.turn([0,2],alpha)
   
    elif (counter == 1):               #2              # face POI by turning left, one turn
        alpha = np.pi - (np.arctan((x + b) / k))
        alpha = alpha*(180/np.pi)*.8333
        xP = np.sqrt((x + b)**2 + k**2)
        poi.turn([0,-2],alpha)
    
    # elif (counter == 3):                             # face POI by turning right, two turns
    #     xP = np.sqrt((k**2) + ((x + b)**2) - (2 * k * (x + b) * np.cos(45)))
    #     alpha = np.pi - ((x + b) / (xP * np.sqrt(2)))
    #     alpha = alpha*(180/np.pi)
    #     poi.turn([0,2],alpha)

    # elif (counter == 1):                             # face POI by turning left, two turns
    #     xP = np.sqrt((k**2) + ((x + b)**2) - (2 * k * (x + b) * np.cos(45)))
    #     alpha = np.pi - ((x + b) / (xP * np.sqrt(2)))
    #     alpha = alpha*(180/np.pi)
    #     poi.turn([0,-2],alpha)
        
    print("Alpha: ", alpha)
    return xP
