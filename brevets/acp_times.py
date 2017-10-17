"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow, math

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

CUTOFF =  [0, 200, 400, 600, 1000, 1300]     #cutoff distance brackets for each speed bracket (km)
MAXSPD =  [0, 34 , 32 , 30 , 28, 26]         #maximum speed for each time bracket (km/h)
MINSPD =  [0, 15 , 15 , 15 , 11.428, 13.333] #minimum speed for eachg time bracket (km/h)


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    assert brevet_dist_km >= 0 and brevet_dist_km <= 1000
    if control_dist_km > brevet_dist_km: raise ValueError("Provided control distance is greater than provided Brevet distance")
    if control_dist_km < 0:              raise ValueError("Provided control distance is less than 0")

    if control_dist_km == 0: time = 0
    else:                    time = find_time_using(MAXSPD, control_dist_km)
    
    start = arrow.get(brevet_start_time)
    hrs, mins = convert_hrs_mins(time)
    shifted = start.shift(hours=+hrs)
    shifted = shifted.shift(minutes=+mins)
    #print("the open time is: "+str(hrs)+":"+str(mins))
    return shifted.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    assert brevet_dist_km >= 0 and brevet_dist_km <= 1000
    if control_dist_km > brevet_dist_km*1.1: raise ValueError("The provided control distance is greater than 110% of provided Brevet distance")
    if control_dist_km < 0:                  raise ValueError("The provided control distance is less than 0")

    if control_dist_km == 0: time = 1
    else:                    time = find_time_using(MINSPD, control_dist_km)
    
    start = arrow.get(brevet_start_time)
    hrs, mins = convert_hrs_mins(time)
    shifted = start.shift(hours=+hrs)
    shifted = shifted.shift(minutes=+mins)
    #print("the open time is: "+str(hrs)+":"+str(mins))
    return shifted.isoformat()

def find_time_using(spd, control_dist_km):
    """
    Calculates the time to travel the control distance given by the speeds in the spd variable. It iterates
    through the distance cutoff array, then increments the time appropriately if control > CUTOFF[i]. Once the 
    control distance is within its appropriate bracket, the time is incremented from the remaining distance.
    Args:
    	spd: list of numbers, of appropriate speeds (should either be the constant arrays MAXSPD or MINSPD)
    	control_dist_km: number, the control distance in kilometers
    Returns:
    	The time it takes to travel the control distance, calculated from the speed brackets given
    """
    time = 0
    rem = control_dist_km
    for i in range(1, len(CUTOFF)):
        if control_dist_km > CUTOFF[i]:
            delta = CUTOFF[i] - CUTOFF[i-1];
            time += delta/spd[i]
            rem -= delta
        else:
            time += rem/spd[i]
            break
    return time

def convert_hrs_mins(f):
    """
    Converts a time expressed as a decimal into time expressed as hours and minutes.
    Args:
    	Time expressed in a floating point number
    Returns: 
    	Time expressed in an list of [hours, minutes]
    """
    mins, hrs = math.modf(f)
    hrs = int(hrs)
    mins = int(mins*60)
    return [hrs, mins]