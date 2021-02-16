#import GUI as gui
import time
import datetime
from datetime import timedelta

start_time = datetime.datetime.now()

def IncubationTime(nb_pics, time) -> datetime:

    total_time = start_time + timedelta(seconds=(nb_pics-1) * time)
    print(start_time)
    print("total time:", total_time)
    return total_time

def RunSetup(nb_pics, time, max_size):

    while datetime.datetime.now() < IncubationTime(nb_pics, time):
        print("test")
