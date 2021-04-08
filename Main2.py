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
######################################################
######KENZA'S PATHS###################################
######################################################
######################################################
stitchedSavingFolder = 'E:/KENZA Folder/CapstoneTests'
graphPath = 'E:/KENZA Folder/CapstoneTests/Graph'

######################################################
######Capstone team'S PATHS###################################
######################################################
######################################################
#stitchedSavingFolder = 'C:/capstone'
#graphPath = 'C:/capstone/Graph'

#image_bf = cv2.imread(r"C:\capstone\test3.tif", 0)  # BF image for use when testing without acquiring image
#image_fl = cv2.imread(r"C:\capstone\test1.png", 0)  # fl image
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
ScanBool = False
AnalysisBool = True
TrigBool = False
GraphBool = True

triggered=False

# statusUpdate("Scanning image")
def RunSetup(nb_pics, timeinterval, unit, max_size, min_size):
    # Set T/F here

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
            image_bf, pixelsizeinum = pycrocontrol.acquireImage("ESP-XLED", "BF",pycrocontrol.hook_bf)  # acquire BF on the ESP-XLED channel group
            BrightfieldStitchedPath = "{}\BF-{}.png".format(stitchedSavingFolder, n)
            cv2.imwrite(BrightfieldStitchedPath, image_bf)
            # ----
            # FLUORESCENT
            # ----
            image_fl, pixelsizeinum = pycrocontrol.acquireImage("ESP-XLED", "Resorufin",pycrocontrol.hook_fl)  # acquire FL on the ESP-XLED channel group
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
        # todo#######
        # todo#######
        # todo## FOR TESTING ONLY vvvvvv
        # image_bf = stitchingopencv.direct_stitch('E:\KENZA Folder\CapstoneTests\saving_name_233')
        # BrightfieldStitchedPath = "{}\BF-{}.png".format(stitchedSavingFolder, n)
        # cv2.imwrite(BrightfieldStitchedPath, image_bf)
        # todo### FOR TESTING ONLY (STICHES WITHOUT ACQUIRING)^^^^^^
        # todo#######
        # todo#######

        # IMAGE ANALYSIS STAGE
        if AnalysisBool:
            if (n == 0):  # if it's our first loop we want to set up the wells area (fills circles array)
                detection.detectWells(image_bf, True, stitchedSavingFolder)


            # Begin BF Analysis:
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            detection.isolateWells(image_bf)  # creates array of isolated well images (image with black border)[croppedImages]
            analyzeBrightfield(min_size, n,max_size)
            # Begin FL Analysis:
            detection.croppedImages.clear()  # clear the cropped images to allow for the next
            detection.isolateWells(image_fl)  # creates array of isolated well images (image with black border)[croppedImages]
            analyzeFluorescent(min_size, n)






        # HARDWARE TRIGGER
        if TrigBool:

            if(triggered):

                #onTrigger(udpSend)
                print("TRIGGERED TO STOP/DUMP DROPLETS")

                break;
        else:
            time.sleep(duration)

        # WRITE OUR CSV FILE HERE AT THE END OF EACH PICTURE(2 channels in this case) TAKEN
        with open(stitchedSavingFolder + '/Data/ImageData' +str("-")+str(n)+str("-")+ str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '.csv',
                  'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str("Well#"), str("Filament-Radius(um)"), str("Droplet-Radius(um)"), ("#-of-Spores"), ("Fluorescence(pxls)"), ("Status")])
            for welldata in range(len(detection.croppedImages)):
                writer.writerow([
                    str(welldata),
                    str(trueDict['NumPic' + str(n)]['WellNumb' + str(welldata)]['Filament Radius ']),
                    str(trueDict['NumPic' + str(n)]['WellNumb' + str(welldata)]['Droplet Radius ']),
                    str(trueDict['NumPic' + str(n)]['WellNumb' + str(welldata)]['# of spores ']),
                    str(trueDict['NumPic' + str(n)]['WellNumb' + str(welldata)]['Fluorescence ']),
                    str(trueDict['NumPic' + str(n)]['WellNumb' + str(welldata)]['Status '])
                ])

    end_time = datetime.now()
    print('End of loop')
    print('Time elapsed:', end_time - start_time)

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

    for wellNumber in range(len(detection.croppedImages)):
        for pictureNumber in range(pics):
            y.append(trueDict["NumPic"+str(pictureNumber)]["WellNumb"+str(wellNumber)]["Fluorescence "])
        for i in range(pics):
            x.append(timeinterval + (timeinterval * i))
        plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12)
        # naming the x-axis
        plt.xlabel('Time ' + '(' + unit + ')')
        # naming the y-axis
        plt.ylabel('Fluorescence Intensity (pixels)')
        # graph title
        plt.title('Fluorescence growth over incubation period')
        # showing the plot
        plt.savefig(graphPath + '/FluorGraphWell_' + str(wellNumber) + '_' + str(
            datetime.now().strftime("%Y%m%d-%H%M%S")) + '.png')
        plt.close()
        y.clear()
        x.clear()
        print("Fluorescent Graph generated")


def FilGraph(timeinterval, pics, unit):
    x = []
    y = []

    for wellNumber in range(len(detection.croppedImages)):
        for pictureNumber in range(pics):
            y.append(trueDict["NumPic"+str(pictureNumber)]["WellNumb"+str(wellNumber)]["Filament Radius "])
        for k in range(pics):
            x.append(timeinterval + (timeinterval * k))

        # plotting the points
        plt.plot(x, y, marker='o', markerfacecolor='blue', markersize=12)
        # naming the x-axis
        plt.xlabel('Time ' + '(' + unit + ')')
        # naming the y-axis
        plt.ylabel('Filament size (µm)')
        # graph title
        plt.title('Filament growth over incubation period')
        # showing the plot
        plt.savefig(graphPath + '/FilGraphWell_' + str(wellNumber) + '_' + str(
            datetime.now().strftime("%Y%m%d-%H%M%S")) + '.png')
        plt.close()
        y.clear()
        x.clear()
        print("Fillament Graph generated")

def analyzeBrightfield(min_size, n,max_size):
    for x in range(len(detection.croppedImages)):
        brightfieldData=[]
        print("TOTAL NUMBER OF WELLS : ", len(detection.croppedImages))
        print("WELL NUMBER (X) : ", str(x))
        dictionarykeyvalue = "NumPic" + str(n)

        croppedImage = detection.croppedImages[x]

        CellsInsideCroppedImage, spores = algo.detectDroplets(croppedImage.copy())
        print("# spores ", len(spores))
        print("# droplets ", len(CellsInsideCroppedImage))

        # Drolet ruling out criteria
        if len(CellsInsideCroppedImage) > 1:
            # do nothing because well is invalid due to having more than 1 droplet
            print("There is more than 1 droplet inside the well")
            FilamentsInsideCroppedImage = algo.detectFilament(croppedImage.copy())
            filsize = algo.maxThreshCalc(FilamentsInsideCroppedImage)
            trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": filsize,
                                                                 "Droplet Radius ": "Nill",
                                                                 "# of spores ": "Nill",
                                                                 "Status " : "TOOMANYDROPLETS"}

        if len(CellsInsideCroppedImage) < 1:
            FilamentsInsideCroppedImage = algo.detectFilament(croppedImage.copy())
            filsize = algo.maxThreshCalc(FilamentsInsideCroppedImage)
            trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": filsize,
                                                                 "Droplet Radius ": "Nill",
                                                                 "# of spores ": "Nill",
                                                                 "Status " : "NODROPLET"}

        else:
            if len(CellsInsideCroppedImage) == 1:  # if we
                print("there is a droplet BUT")
                if (cv2.contourArea(CellsInsideCroppedImage[0]) < min_size):
                    FilamentsInsideCroppedImage = algo.detectFilament(croppedImage.copy())
                    filsize = algo.maxThreshCalc(FilamentsInsideCroppedImage)
                    # if area of our individual droplet is less than 15 then remove them from array
                    print("Droplet too small, do not analyze")

                    trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": filsize,
                                                                         "Droplet Radius ": "Nill",
                                                                         "# of spores ": "Nill",
                                                                         "Status " : "DROPLETTOOSMALL"}

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

                    #dataValuesSize.setdefault("Image Number"+str(n), {})[x] = algo.maxThreshCalc(FilamentsInsideCroppedImage)

                    trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {
                        "Filament Radius ": algo.maxThreshCalc(FilamentsInsideCroppedImage),
                        "Droplet Radius ": radius,
                        "# of spores ": len(spores),
                        "Status " : "OK"
                        # ,"Fluorescence ": detectionAlgo.intensityFluores(croppedImage)
                    }
                    print("we got here")
                    pixelsizeinum = 0.3243
                    print(filsize)
                    print(radius)
                # converting pixels into micro meters
                    if(filsize):
                        filamentSize = filsize * pixelsizeinum
                        dropletRadius = radius * pixelsizeinum
                        if(((filamentSize/dropletRadius)*100)>=(max_size)):
                            global triggered
                            triggered=True






def analyzeFluorescent(min_size, n):
    for i in range(len(detection.croppedImages)):  # might need to loop through circles instead of croppedimages
        dropletsinside = algo.detectDroplets(detection.croppedImages[i])
        dictionarykeyvalue = "NumPic" + str(n)

        cellFluorescence = algo.intensityFluores(detection.croppedImages[i].copy())
        print("Cell fluorescence: ", cellFluorescence)
        trueDict[dictionarykeyvalue]["WellNumb" + str(i)]["Fluorescence "] = cellFluorescence



