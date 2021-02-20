import math
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import detectionAlgo as fluor_detection

#iteration = 0 #nb of times a picture was taken
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

    start_time = datetime.now()
    end_time_unit=0
    if unit == 's':
        end_time = start_time + timedelta(seconds=(nb_pics-1) * time)
        end_time_unit = end_time.second - start_time.second
        print("unit received:", unit)
    if unit == 'min':
        end_time = start_time + timedelta(minutes=(nb_pics-1) * time)
        end_time_unit = end_time.minute - start_time.minute
        print("unit received:", unit)
    if unit == 'hrs':
        end_time = start_time + timedelta(hours=(nb_pics-1) * time)
        end_time_unit = end_time.hour - start_time.hour
        print("unit received:", unit)

    while datetime.now() < end_time:
        timelast =start_time
        print("in time loop")

        if unit == 's':
           if timelast.second - datetime.now().second >= time:
               #do stuff
               timelast = datetime.now()

        if unit == 'min':
            if timelast.minute - datetime.now().minute >= time:
                #do stuff
                timelast = datetime.now()

        if unit == 'hrs':
            if timelast.hour - datetime.now().hour >= time:
                #do stuff
                timelast = datetime.now()


        if datetime.now() > end_time:
            print('finished')
            FluorGraph(time,end_time_unit,unit)
            #FilGraph(time,end_time_unit,unit)

def FluorGraph(time,end_time,unit):
    #x-axis values
    x = math.floor(end_time/time) + 1
    print('x: ', x)
    #corresponding y axis values
    xrow=[]
    for i in range(0,x):
        xrow.append(i*time)
        print(i)
    y = [1,4] ### test value
    #plotting the points
    plt.plot(xrow, y, marker='o', markerfacecolor='blue', markersize=12)
    #naming the x-axis
    plt.xlabel('Time '+ '('+ unit +')')
    #naming the y-axis
    plt.ylabel('Fluorescence Intensity (?)')
    #graph title
    plt.title('Fluorescence growth over incubation period')
    #showing the plot
    plt.show()
    print("done plotting")

def FilGraph(time,end_time,unit):
    #x-axis values
    x = math.floor(end_time/time) + 1
    #corresponding y axis values
    xrow=[]
    for i in range(0,x):
        xrow.append(i*time)
        print(i)
    y = [2,8] ### test value
    #plotting the points
    plt.plot(xrow, y)
    #naming the x-axis
    plt.xlabel('Time '+ '('+ unit +')')
    #naming the y-axis
    plt.ylabel('Filament Intensity (?)')
    #graph title
    plt.title('Filament growth over incubation period')
    #showing the plot
    plt.show()
    print("done plotting")
