import math, time
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
# import PycroManagerCoreControl as pycrocontrol
import Circles as detection
import detectionAlgo as algo

duration = 0
dataValuesSize = {}
dataValuesFlu = {}


def RunSetup(nb_pics, timeinterval, unit, max_size, min_size):
    if unit == 's':
        duration = timeinterval
        print("time received (s):", duration)
    if unit == 'min':
        duration = timeinterval * 60
        print("time received (s):", duration)
    if unit == 'hr':
        duration = timeinterval * 60 * 60
        print("time received (s):", duration)

    for i in range(0, len(detection.croppedImages)):  # might need to loop through circles instead of croppedimages
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
    start_time = datetime.now()
    for n in range(nb_pics):
        print("n:", n)

        # image = pycrocontrol.acquireImage("ESP-XLED","BF") #acquire brightfield on the ESP-XLED channel group

        # detection.detectWells(image,min_size,max_size,True) ## might need to be changed a bit

        # detection.isolateWells(image) #creates array of isolated well images

        # rest...

        for i in range(len(detection.croppedImages)):
            dataValuesFlu[n] = {i: algo.detectFluores(detection.croppedImages[i])}
            dataValuesSize[n] = {i: algo.maxThreshCalc(detection.croppedImages[i])}

        time.sleep(duration)
        end_time = datetime.now()
    print('loop finished')
    print('time elapsed:', end_time - start_time)
    # FluorGraph(timeinterval, nb_pics, unit)
    # FilGraph(timeinterval, nb_pics,unit)


def FluorGraph(timeinterval, pics, unit):
    x = []
    y = []
    for i in range(pics):
        x.append(timeinterval + (timeinterval * i))
    print("x axis", x)
    for j in range(len(detection.croppedImages)):
        for i in range(detection.croppedImages):
            y.append(dataValuesFlu[i][j])
            # plotting the points
            plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12)
            # naming the x-axis
            plt.xlabel('Time ' + '(' + unit + ')')
            # naming the y-axis
            plt.ylabel('Fluorescence Intensity (pixels)')
            # graph title
            plt.title('Fluorescence growth over incubation period')
            # showing the plot
            plt.savefig('FluorGraphWell' + i + '.png')
            print("done plotting")


def FilGraph(timeinterval, pics, unit):
    x = []
    y = []
    for i in range(pics):
        x.append(timeinterval + (timeinterval * i))
    for j in range(len(detection.croppedImages)):
        for i in range(detection.croppedImages):
            y.append(dataValuesSize[i][j])
            print("x axis", x)
            y = [2, 8]  # test values
            # plotting the points
            plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12)
            # naming the x-axis
            plt.xlabel('Time ' + '(' + unit + ')')
            # naming the y-axis
            plt.ylabel('Filament Intensity (pixels)')
            # graph title
            plt.title('Filament growth over incubation period')
            # showing the plot
            plt.savefig('FilGraph' + i + '.png')
            print("done plotting")
