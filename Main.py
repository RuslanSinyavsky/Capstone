import time
import datetime
from datetime import timedelta

#end_time = datetime

#def IncubationTime(nb_pics, time, unit) -> datetime:

#start_time = datetime.datetime.now()

#    if unit == 's':
#        end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
#        print("unit received:", unit)
#    if unit == 'min':
#        end_time = start_time + timedelta(minutes=(nb_pics-1) * time)
#        print("unit received:", unit)
#    if unit == 'hrs':
#        end_time = start_time + timedelta(hours=(nb_pics-1) * time)
#        print("unit received:", unit)

#    print("start time:", start_time)
#    print("total time:", end_time)
    #return end_time

def RunSetup(nb_pics, time, unit, max_size, min_size):

    start_time = datetime.datetime.now()
    if unit == 's':
        end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
        print("unit received:", unit)
    if unit == 'min':
        end_time = start_time + timedelta(minutes=(nb_pics-1) * time)
        print("unit received:", unit)
    if unit == 'hrs':
        end_time = start_time + timedelta(hours=(nb_pics-1) * time)
        print("unit received:", unit)

    print("start time:", start_time)
    print("end time:", end_time)

    #end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
    print(datetime.datetime.now())
    while datetime.datetime.now() < end_time:
        print("in time loop")


