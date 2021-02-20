import math
from datetime import timedelta, datetime
import matplotlib.pyplot as plt

iteration = 0 #nb of times a picture was taken

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
    #time_unit=unit
    start_time = datetime.now()
    if unit == 's':
        end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
        print('end time: ',end_time)
        end_time_unit=end_time.second
        print('end time unit: ',end_time_unit)
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
    print(datetime.now())
    #while datetime.datetime.now() < end_time:
    while datetime.now() < end_time:
        print("in time loop")
        if datetime.now() > end_time:
            print('finished')
            FluorGraph(time,end_time_unit,unit)
            FilGraph(time,end_time_unit,unit)

def FluorGraph(time,end_time,unit):
    #x-axis values
    x = math.floor(end_time/time)
    print(end_time)
    print(x)
    #corresponding y axis values
    y = [1,4]
    #plotting the points
    plt.plot(x, y)
    #naming the x-axis
    plt.xlabel('Time '+ '('+ unit +')')
    #naming the y-axis
    plt.ylabel('Fluorescence Intensity (?)')
    #graph title
    plt.title('Fluorescence growth over incubation period')
    #showing the plot
    plt.show()

def FilGraph(time,end_time,unit):
    #x-axis values
    x = math.floor(end_time/time)
    #corresponding y axis values
    y = [1,4]
    #plotting the points
    plt.plot(x, y)
    #naming the x-axis
    plt.xlabel('Time '+ '('+ unit +')')
    #naming the y-axis
    plt.ylabel('Filament growth level (?)')
    #graph title
    plt.title('Filament growth over incubation period')
    #showing the plot
    plt.show()
