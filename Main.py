import math, time
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
#import PycroManagerCoreControl as pycrocontrol
import Circles as detection
import detectionAlgo as algo

def RunSetup(nb_pics, timeinterval, unit, max_size, min_size):
    start_time = datetime.now()
    end_time = 0
    end_time_unit = 0
    if unit == 's':
        end_time = start_time + timedelta(seconds=(nb_pics - 1) * timeinterval)
        end_time_unit = end_time.second - start_time.second
        print("time received:", end_time_unit, unit)
    if unit == 'min':
        end_time = start_time + timedelta(minutes=(nb_pics - 1) * timeinterval)
        end_time_unit = end_time.minute - start_time.minute
        print("time received:", end_time_unit, unit)
    if unit == 'hr':
        end_time = start_time + timedelta(hours=(nb_pics - 1) * timeinterval)
        end_time_unit = end_time.hour - start_time.hour
        print("time received:", end_time_unit, unit)
    timelast = start_time

    # ------
    # do our first image acquisition here
    #   image = pycrocontrol.acquireImage("ESP-XLED","BF") #acquire brightfield on the ESP-XLED channel group
    #   detection.detectWells(image,min_size,max_size,True) ## might need to be changed a bit
    #   detection.isolateWells(image) #creates array of isolated well images

    for i in range(0, len(detection.croppedImages)):  ##might need to loop through circles instead of croppedimages
        dropletsinside = algo.detectDroplets(detection.croppedImages[i])

        if len(dropletsinside) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            time.sleep(0)

        else:

            # detect filaments

            # get pixel count of filament

            # get total pixel count of well

            # Divide filametnpixel/wellpixel to get ratio aka how large it is in proportion to well
            time.sleep(0)

    # ------

    while datetime.now() < end_time:
        # do the rest of our image acquisitions here
        if unit == 's':
            if datetime.now().second - timelast.second >= timeinterval:
                # do stuff

                print("in time loop")
                timelast = datetime.now()
                time.sleep(1)
        if unit == 'min':
            if datetime.now().minute - timelast.minute >= timeinterval:
                # do stuff
                timelast = datetime.now()
                time.sleep(1)
        if unit == 'hrs':
            if datetime.now().hour - timelast.hour >= timeinterval:
                # do stuff
                timelast = datetime.now()
                time.sleep(1)
        if datetime.now() > end_time:
            print('finished')
            #FluorGraph(timeinterval, end_time_unit, unit)
            #FilGraph(timeinterval,end_time_unit,unit)

def FluorGraph(timeinterval, end_time, unit):
    # x-axis values
    print("end time: ", end_time)
    x = math.floor(end_time / timeinterval) + 1
    print('x: ', x)
    # corresponding y axis values
    xrow = []
    for i in range(0, x):
        xrow.append(i * timeinterval)
        print(i)
    y = [1, 4]  ### test value
    # plotting the points
    plt.plot(xrow, y, marker='o', markerfacecolor='blue', markersize=12)
    # naming the x-axis
    plt.xlabel('Time ' + '(' + unit + ')')
    # naming the y-axis
    plt.ylabel('Fluorescence Intensity (?)')
    # graph title
    plt.title('Fluorescence growth over incubation period')
    # showing the plot
    plt.show()
    print("done plotting")


def FilGraph(timeinterval, end_time, unit):
    # x-axis values
    x = math.floor(end_time / timeinterval) + 1
    # corresponding y axis values
    xrow = []
    for i in range(0, x):
        xrow.append(i * timeinterval)
        print(i)
    y = [2, 8]  ### test value
    # plotting the points
    plt.plot(xrow, y)
    # naming the x-axis
    plt.xlabel('Time ' + '(' + unit + ')')
    # naming the y-axis
    plt.ylabel('Filament Intensity (?)')
    # graph title
    plt.title('Filament growth over incubation period')
    # showing the plot
    plt.show()
    print("done plotting")
