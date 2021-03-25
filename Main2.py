import math, time
import sys
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
#import PycroManagerCoreControl as pycrocontrol
import Circles as detection
#from GUI import statusUpdate
import detectionAlgo as algo
import cv2
#from GSOF_ArduBridge import UDP_Send

duration = 0
dataValuesSize = {}
dataValuesFlu = {}
stitchedSavingFolder = 'E:\KENZA Folder\CapstoneTests'
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

    if unit == 's':
        duration = timeinterval
        print("time received (s):", duration)
    if unit == 'min':
        duration = timeinterval * 60
        print("time received (s):", duration)
    if unit == 'hr':
        duration = timeinterval * 60 * 60
        print("time received (s):", duration)
    '''
    for i in range(0, len(detection.croppedImages)):  #might need to loop through circles instead of croppedimages
        dropletsinside = algo.detectDroplets(detection.croppedImages[i])

        if len(dropletsinside) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            time.sleep(0)

        else:
            # detect filaments

            # get pixel count of filament

            # get total pixel count of well

            # Divide filamentpixel/wellpixel to get ratio aka how large it is in proportion to well
            time.sleep(0)
    '''
    start_time = datetime.now()
    for n in range(nb_pics):  #OUR MAIN LOOP
        #SCANNING STAGE
        if ScanBool:
            print("Scanning image", n + 1)
            #gui.statusUpdate("Scanning image", n + 1)
            '''
            # ----
            # BRIGHT FIELD
            # ----
            detection.croppedImages.clear()  #clear the cropped images to allow for the next
            image1 = pycrocontrol.acquireImage("ESP-XLED", "BF", pycrocontrol.hook_bf)  #acquire BF on the ESP-XLED channel group
            BrightfieldStitchedPath = "{}\BF-{}.png".format(stitchedSavingFolder, n)
            plt.imsave(BrightfieldStitchedPath, image1)
            '''
            '''
            # ----
            # FLUORESCENT
            # ----
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            image2 = pycrocontrol.acquireImage("ESP-XLED", "Resorufin", pycrocontrol.hook_fl)  #acquire FL on the ESP-XLED channel group
            FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            plt.imsave(FluorescentStitchedPath, image2)
            '''
            '''
            # ----
            # BOTH
            # ----
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            image2 = pycrocontrol.acquireImage("ESP-XLED", "Resorufin", "BF", pycrocontrol.hook_fl)  #acquire BF and FL on the ESP-XLED channel group
            FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            plt.imsave(FluorescentStitchedPath, image)
            '''
        #IMAGE ANALYSIS STAGE
        #Turn this into two functions, 1 for BF specific and 1 for FL
        if AnalysisBool:
            '''
            if (n == 0):  # if it's our first loop we want to set up the wells area (fills circles array)
                detection.detectWells(image1, min_size, max_size, True)  ## might need to be changed a bit
            '''
            def BFAnalysis(image):
                detection.isolateWells(image)  #creates array of isolated well images (image with black border)
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
                            print("Filament size: ", algo.maxThreshCalc(FilamentsInsideCroppedImage))
                            #RECORD DATA START

                            #RECORD DATA END
                            (x, y), radius = cv2.minEnclosingCircle((dropletsinside[0]))
                            print("radius of this droplet is = : ", radius)
                            # ^^^^ use this to detect abortion criteria ^^^^
            '''
            detection.isolateWells(image2)  # creates array of isolated well images (image with black border)
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
                        # RECORD DATA START

                        # RECORD DATA END

            for i in range(len(detection.croppedImages)):
                dataValuesFlu[n] = {i: algo.detectFluores(detection.croppedImages[i])}
                dataValuesSize[n] = {i: algo.maxThreshCalc(detection.croppedImages[i])}
            '''
        #HARDWARE TRIGGER
        if TrigBool:
            onTrigger(udpSend)
        else:
            time.sleep(duration)
    end_time = datetime.now()
    print('End of loop')
    print('Time elapsed:', end_time - start_time)
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
        plt.savefig(stitchedSavingFolder + '\FluorGraphWell' + j + '.png')
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
        plt.savefig(stitchedSavingFolder +'\FilGraph' + j + '.png')
        print("done plotting")
