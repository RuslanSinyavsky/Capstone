import math, time
import sys
import csv
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
#import PycroManagerCoreControl as pycrocontrol
import Circles as detection
import detectionAlgo as algo
import cv2
import MiddleMan as middleman
#from GSOF_ArduBridge import UDP_Send

duration = 0
dataValuesSize = {}
dataValuesFlu = {}
dataValuesFluT = {}
dataValuesSizeT = {}
stitchedSavingFolder = 'E:/KENZA Folder/CapstoneTests'
'''
if UDP_Send in sys.modules:
    #setup UDP sending protocol for ArduBridge Shell.
    port=7010
    ip='127.0.0.1'
    print('UDP active on port %d')%(port)
    udpSend = False
    if port > 1:
        udpSend = UDP_Send.udpSend(nameID='', DesIP=ip, DesPort=port)
'''
#statusUpdate("Scanning image")
def RunSetup(nb_pics, timeinterval, unit, max_size, min_size):
    #Set T/F here
    ScanBool = True
    AnalysisBool = False
    TrigBool = False
    GraphBool = False
    '''
    if check == 1:  #Exlude empty droplets
        print("Exclude empty droplets")
    if check == 0:  #Include empty droplets
        print("Include empty droplets")
    '''
    if unit == 's':
        duration = timeinterval
        print("time received (s):", duration)
    if unit == 'min':
        duration = timeinterval * 60
        print("time received (s):", duration)
    if unit == 'hr':
        duration = timeinterval * 60 * 60
        print("time received (s):", duration)

    start_time = datetime.now()
    for n in range(nb_pics):  #OUR MAIN LOOP
        #SCANNING STAGE
        if ScanBool:
            print("Scanning image", n + 1)
            #gui.statusUpdate("Scanning image", n + 1)

            # ----
            # BRIGHT FIELD
            # ----
            #image_bf = pycrocontrol.acquireImage("ESP-XLED", "BF", pycrocontrol.hook_bf)  #acquire BF on the ESP-XLED channel group
            #BrightfieldStitchedPath = "{}\BF-{}.png".format(stitchedSavingFolder, n)
            #plt.imsave(BrightfieldStitchedPath, image_bf)
            # ----
            # FLUORESCENT
            # ----
            #image_fl = pycrocontrol.acquireImage("ESP-XLED", "Resorufin", pycrocontrol.hook_fl)  #acquire FL on the ESP-XLED channel group
            #FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            #plt.imsave(FluorescentStitchedPath, image_fl)
            '''
            # ----
            # BOTH
            # ----
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            image = pycrocontrol.acquireImage("ESP-XLED", "Resorufin", "BF", pycrocontrol.hook_fl)  #acquire BF and FL on the ESP-XLED channel group
            FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            plt.imsave(FluorescentStitchedPath, image)
            '''
        #IMAGE ANALYSIS STAGE
        if AnalysisBool:
            #if (n == 0):  # if it's our first loop we want to set up the wells area (fills circles array)
                #detection.detectWells(image_bf, min_size, max_size, True)  ## might need to be changed a bit

            #Begin BF Analysis:
            detection.croppedImages.clear()  #clear the cropped images to allow for the next
            #detection.isolateWells(image_bf)  #creates array of isolated well images (image with black border)[croppedImages]
            filamentSize, cellRadius =  analyzeBrightfield(min_size)

            #Begin FL Analysis:
            detection.croppedImages.clear()  #clear the cropped images to allow for the next
            #detection.isolateWells(image_fl)  # creates array of isolated well images (image with black border)[croppedImages]
            cellFluorescence = analyzeFluorescent(min_size)

            for i in range(len(detection.croppedImages)):
                dataValuesFlu.setdefault(n, {})[i] = algo.intensityFluores(detection.croppedImages[i])
                dataValuesSize.setdefault(n, {})[i] = algo.maxThreshCalc(detection.croppedImages[i])
        #HARDWARE TRIGGER
        #if TrigBool:
            #onTrigger(udpSend)
        else:
            time.sleep(duration)

    end_time = datetime.now()
    middleman.Holder("End of incubation")
    print('End of loop')
    print('Time elapsed:', end_time - start_time)

    for n in range(len(detection.croppedImages)):
        for i in range(nb_pics):
            dataValuesFluT.setdefault(n, {})[i] = dataValuesFlu[i][n]
            dataValuesSizeT.setdefault(n, {})[i] = dataValuesSize[i][n]

    with open(stitchedSavingFolder + '/Data/FluData.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dataValuesFluT.items():
            writer.writerow([key, value])

    with open(stitchedSavingFolder + '/Data/SizeData.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dataValuesSizeT.items():
            writer.writerow([key, value])
    #Plotting Graphs
    if GraphBool:
        FluorGraph(timeinterval, nb_pics, unit)
        FilGraph(timeinterval, nb_pics,unit)

def onTrigger(udp):
        print('Trigger received. Stopping incubation, starting sorting process.')
        s = 'setup.ImgTrigger()'
        if udp != False:
            udp.Send(s)

def FluorGraph(timeinterval, pics, unit):
    x = []
    y = []
    for i in range(pics):
        x.append(timeinterval + (timeinterval * i))
    print("x axis", x)
    for j in range(len(detection.croppedImages)):
        for i in range(pics):
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
        plt.savefig(stitchedSavingFolder + '/FluorGraphWell' + j + '.png')
        print("done plotting")

def FilGraph(timeinterval, pics, unit):
    x = []
    y = []
    for i in range(pics):
        x.append(timeinterval + (timeinterval * i))
    for j in range(len(detection.croppedImages)):
        for i in range(pics):
            y.append(dataValuesSize[i][j])
        # plotting the points
        plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12)
        # naming the x-axis
        plt.xlabel('Time ' + '(' + unit + ')')
        # naming the y-axis
        plt.ylabel('Filament Intensity (pixels)')
        # graph title
        plt.title('Filament growth over incubation period')
        # showing the plot
        plt.savefig(stitchedSavingFolder +'/FilGraph' + j + '.png')
        print("done plotting")

def analyzeBrightfield(min_size):
    for i in range(0, len(detection.croppedImages)):  #might need to loop through circles instead of croppedimages
        dropletsinside = algo.detectDroplets(detection.croppedImages[i])
        if len(dropletsinside) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            time.sleep(0)
        else:
            if (cv2.contourArea(dropletsinside[0]) < min_size):
                #if area of our individual droplet is less than min_size then remove them from array
                print("Droplet too small, do not analyze")
            else:
                #detect filaments size in BF
                FilamentsInsideCroppedImage = algo.detectFilament(detection.croppedImages[i].copy())
                filsize = algo.maxThreshCalc(FilamentsInsideCroppedImage)
                print("Filament size: ", algo.maxThreshCalc(FilamentsInsideCroppedImage))
                #RECORD DATA START

                #RECORD DATA END
                (x, y), radius = cv2.minEnclosingCircle((dropletsinside[0]))
                print("radius of this droplet is = : ", radius)
                # ^^^^ use this to detect abortion criteria ^^^^

    return filsize , radius

def analyzeFluorescent(min_size):
    for i in range(0, len(detection.croppedImages)):  # might need to loop through circles instead of croppedimages
        dropletsinside = algo.detectDroplets(detection.croppedImages[i])
        if len(dropletsinside) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            time.sleep(0)
        else:
            # detects fluorescence is FL picture
            # Droplet ruling out criteria
            if (cv2.contourArea(dropletsinside[0]) < min_size):
                # if area of our individual droplet is less than min_size then remove them from array
                print("Droplet too small, do not analyze")
            else:
                # Record our data
                cellFluorescence = algo.intensityFluores(detection.croppedImages[i].copy())
                print("Cell fluorescence: ", cellFluorescence)
    return cellFluorescence