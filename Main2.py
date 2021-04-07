import math, time
import sys
import csv
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
import PycroManagerCoreControl as pycrocontrol
import Circles as detection
import detectionAlgo as algo
import cv2
import stitchingopencv
from collections import defaultdict

# import MiddleMan as middleman
# from GSOF_ArduBridge import UDP_Send

duration = 0
dataValuesSize = {}
dataValuesFlu = {}
dataValuesFluT = {}
dataValuesSizeT = {}
stitchedSavingFolder = 'E:/KENZA Folder/CapstoneTests'

trueDict = defaultdict(dict)

'''
#setup UDP sending protocol for ArduBridge Shell.
port=7010
ip='127.0.0.1'
print('UDP active on port '+str(port))
udpSend = False
if port > 1:
    udpSend = UDP_Send.udpSend(nameID='', DesIP=ip, DesPort=port)
'''


# statusUpdate("Scanning image")
def RunSetup(nb_pics, timeinterval, unit, max_size, min_size):
    # Set T/F here
    ScanBool = False
    AnalysisBool = False
    TrigBool = True
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
    for n in range(nb_pics):  # OUR MAIN LOOP
        # SCANNING STAGE
        if ScanBool:
            print("Scanning image", n + 1)
            # gui.statusUpdate("Scanning image", n + 1)

            # ----
            # BRIGHT FIELD
            # ----
            image_bf , pixelsizeinum = pycrocontrol.acquireImage("ESP-XLED", "BF",pycrocontrol.hook_bf)  # acquire BF on the ESP-XLED channel group
            BrightfieldStitchedPath = "{}\BF-{}.png".format(stitchedSavingFolder, n)
            cv2.imwrite(BrightfieldStitchedPath, image_bf)
            # ----
            # FLUORESCENT
            # ----
            image_fl,pixelsizeinum = pycrocontrol.acquireImage("ESP-XLED", "Resorufin",pycrocontrol.hook_fl)  # acquire FL on the ESP-XLED channel group
            FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            cv2.imwrite(FluorescentStitchedPath, image_fl)
            '''
            # ----
            # BOTH
            # ----
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            image = pycrocontrol.acquireImage("ESP-XLED", "Resorufin", "BF", pycrocontrol.hook_fl)  #acquire BF and FL on the ESP-XLED channel group
            FluorescentStitchedPath = "{}\Fluo-{}.png".format(stitchedSavingFolder, n)
            plt.imsave(FluorescentStitchedPath, image)
            '''
            #todo#######
            #todo#######
            #todo## FOR TESTING ONLY vvvvvv
       # image_bf = cv2.imread('E:\KENZA Folder\CapstoneTests\', 0)
        image_bf = stitchingopencv.direct_stitch('E:\KENZA Folder\CapstoneTests\saving_name_233')
            #todo### FOR TESTING ONLY ^^^^^^
            #todo#######
            #todo#######

        # IMAGE ANALYSIS STAGE
        if AnalysisBool:
            if (n == 0):  # if it's our first loop we want to set up the wells area (fills circles array)
                detection.detectWells(image_bf,  True)  ## might need to be changed a bit

            # Begin BF Analysis:
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            detection.isolateWells(image_bf)  # creates array of isolated well images (image with black border)[croppedImages]
            filamentSize , cellRadius  = analyzeBrightfield(min_size)

            #converting pixels into micro meters
            filamentSize = filamentSize*pixelsizeinum
            cellRadius = cellRadius*pixelsizeinum

            # Begin FL Analysis:
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            detection.isolateWells(image_fl)  # creates array of isolated well images (image with black border)[croppedImages]
            cellFluorescence = analyzeFluorescent(min_size)

            for i in range(len(detection.croppedImages)):
                dataValuesFlu.setdefault(n, {})[i] = cellFluorescence
                dataValuesSize.setdefault(n, {})[i] = filamentSize
        # HARDWARE TRIGGER
        if TrigBool:

           # if(((filamentSize/cellRadius)*100)>=(max_size)):

                # onTrigger(udpSend)
                print("TRIGGERED TO STOP/DUMP DROPLETS")

                break;
        else:
            time.sleep(duration)

        #WRITE OUR CSV FILE HERE AT THE END OF EACH PICTURE(2 channels in this case) TAKEN
        with open(stitchedSavingFolder + '/Data/FluData.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str("Well#"), str("Filament-Radius(um)"), str("Droplet-Radius(um)"), ("#-of-Spores"), ("Fluorescence(pxls)")])
            for welldata in range(len(detection.croppedImages)):
                writer.writerow([
                    str(welldata),
                    str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Filament Radius ']),
                    str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Droplet Radius ']),
                    str(trueDict['NumPic0']['WellNumb' + str(welldata)]['# of spores '])
                    # ,str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Fluorescence '])
                ])

    end_time = datetime.now()
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
    # Plotting Graphs
    if GraphBool:
        FluorGraph(timeinterval, nb_pics, unit)
        FilGraph(timeinterval, nb_pics, unit)


def onTrigger(udp):
    s = 'setup.ImgTrigger()'
    if udp != False:
        udp.Send(s)
    print('Trigger sent. Stopping incubation, starting sorting process.')


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
        plt.savefig(stitchedSavingFolder + '/FilGraph' + j + '.png')
        print("done plotting")


def analyzeBrightfield(min_size):
    for x in range(len(detection.croppedImages)):
        print("TOTAL NUMBER OF WELLS : ", len(detection.croppedImages))
        print("WELL NUMBER (X) : ", str(x))
        dictionarykeyvalue = "NumPic" + str(x)

        croppedImage = detection.croppedImages[x]

        CellsInsideCroppedImage, spores = algo.detectDroplets(croppedImage.copy())
        print("# spores ", len(spores))
        print("# droplets ", len(CellsInsideCroppedImage))

        # Drolet ruling out criteria
        if len(CellsInsideCroppedImage) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            print("There is more than 1 droplet inside the well")

            trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": "TOOMANYDROPLETS",
                                                                 "Droplet Radius ": "Nill",
                                                                 "# of spores ": "Nill"}

        if len(CellsInsideCroppedImage) < 1:
            trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": "NODROPLET",
                                                                 "Droplet Radius ": "Nill",
                                                                 "# of spores ": "Nill"}

        else:
            if len(CellsInsideCroppedImage) == 1:  # if we
                print("there is a droplet BUT")
                if (cv2.contourArea(CellsInsideCroppedImage[0]) < min_size):
                    # if area of our individual droplet is less than 15 then remove them from array
                    print("Droplet too small, do not analyze")

                    trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": "DROPLETTOOSMALL",
                                                                         "Droplet Radius ": "Nill",
                                                                         "# of spores ": "Nill"}
                else:
                    # Record our data

                    # end record

                    # analyze filament

                    FilamentsInsideCroppedImage = algo.detectFilament(croppedImage.copy())
                    filsize = algo.maxThreshCalc(FilamentsInsideCroppedImage)
                    print("Filament size(radius) : ", algo.maxThreshCalc(FilamentsInsideCroppedImage))

                    # cnt = max(contours_isolated, key=cv2.contourArea)
                    (z, y), radius = cv2.minEnclosingCircle((CellsInsideCroppedImage[0]))
                    print("radius of this droplet is = : ", radius)

                    # storing data into dictionary

                    dataValuesSize.setdefault("Image Number", {})[x] = algo.maxThreshCalc(
                        FilamentsInsideCroppedImage)

                    trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {
                        "Filament Radius ": algo.maxThreshCalc(FilamentsInsideCroppedImage),
                        "Droplet Radius ": radius,
                        "# of spores ": len(spores)
                        # ,"Fluorescence ": detectionAlgo.intensityFluores(croppedImage)
                    }

    return filsize, radius


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
