#import GUI as gui
import time
import datetime
from datetime import timedelta

start_time = datetime.datetime.now()
end_time = datetime

def IncubationTime(nb_pics, time) -> datetime:

    end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
    print(start_time)
    print("total time:", end_time)
    return end_time

def RunSetup(nb_pics, time, max_size):

    total_time = start_time + timedelta(seconds=(nb_pics-1) * time)
    while datetime.datetime.now() < total_time:
        print("test")
