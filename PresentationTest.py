import detectionAlgo
import Circles
import cv2
import csv
import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

dataValuesSize = {}
dataValuesFlu = {}
dataValuesFluT = {}
dataValuesSizeT = {}
stitchedSavingFolder = 'C:/capstone'

# Images to use for demo
img_BF = cv2.imread(r"C:\capstone\testimage.tif", 0)  # BF image
# img_F = cv2.imread(r"C:\capstone\test1.png",0)        #FL image

# Locate Wells & isolate Brightfield
Circles.detectWells(img_BF, 80, 100, True, stitchedSavingFolder)  # detect wells in BF picture
Circles.isolateWells(img_BF)  # isolate wells in BF picture

# =======================================================================================================================
# ---------------------------------------BRIGHTFIELD--------------------------------------------------------------------
# =======================================================================================================================
# Cropping out wells
croppedImage = Circles.croppedImages[41]  # THE ARRAY OF ISOLATED WELL's first picture [39] has filament

# plt.imshow(croppedImage)
# plt.show()

# Detect filament

# FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
# print("Filament size : ",detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage))

# Locate droplets
CellsInsideCroppedImage, spores = detectionAlgo.detectDroplets(
    croppedImage.copy())  # the location of all cells inside the cropped image
trueDict = defaultdict(dict)
for x in range(len(Circles.croppedImages)):
    print("TOTAL NUMBER OF WELLS : ", len(Circles.croppedImages))
    print("WELL NUMBER (X) : ", str(x))
    dictionarykeyvalue = "NumPic" + str(0)

    croppedImage = Circles.croppedImages[x]

    CellsInsideCroppedImage, spores = detectionAlgo.detectDroplets(croppedImage.copy())
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
            if (cv2.contourArea(CellsInsideCroppedImage[0]) < 15):
                # if area of our individual droplet is less than 15 then remove them from array
                print("Droplet too small, do not analyze")

                trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {"Filament Radius ": "DROPLETTOOSMALL",
                                                                     "Droplet Radius ": "Nill",
                                                                     "# of spores ": "Nill"}
            else:
                # Record our data

                # end record

                # analyze filament

                FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
                print("Filament size(radius) : ", detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage))

                # cnt = max(contours_isolated, key=cv2.contourArea)
                (z, y), radius = cv2.minEnclosingCircle((CellsInsideCroppedImage[0]))
                print("radius of this droplet is = : ", radius)

                # storing data into dictionary

                dataValuesSize.setdefault("Image Number", {})[x] = detectionAlgo.maxThreshCalc(
                    FilamentsInsideCroppedImage)

                trueDict[dictionarykeyvalue]["WellNumb" + str(x)] = {
                    "Filament Radius ": detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage),
                    "Droplet Radius ": radius,
                    "# of spores ": len(spores)
                    #,"Fluorescence ": detectionAlgo.intensityFluores(croppedImage)
                    }

    # cv2.imshow("Cropped image",croppedImage)
    # cv2.waitKey(0)
'''
for i in range(len(Circles.croppedImages)):
    dataValuesSize.setdefault("Image Number", {})[i] = detectionAlgo.maxThreshCalc(Circles.croppedImages[i])
'''
print(trueDict)

print("Filament radius of well 42 is : ", trueDict['NumPic0']['WellNumb42']['Filament Radius '])

'''
listofwelldata = []
for i in range(len(Circles.croppedImages)):
    item1 = [trueDict['NumPic0']['WellNumb'+str(i)]['Filament Radius '],
             trueDict['NumPic0']['WellNumb'+str(i)]['Droplet Radius '],
             trueDict['NumPic0']['WellNumb'+str(i)]['# of spores ']
             ]
    listofwelldata.append(item1)
'''

with open(stitchedSavingFolder + '/Data/FluData.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow([str("Well# "), str("Filament-Radius"), str("Droplet-Radius"), ("#-of-Spores"), ("Fluorescence")])
    for welldata in range(len(Circles.croppedImages)):
        writer.writerow([
            str(welldata),
            str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Filament Radius ']),
            str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Droplet Radius ']),
            str(trueDict['NumPic0']['WellNumb' + str(welldata)]['# of spores '])
            # ,str(trueDict['NumPic0']['WellNumb' + str(welldata)]['Fluorescence '])
        ])

# =======================================================================================================================
# ---------------------------------------FLUORESCENCE--------------------------------------------------------------------
# =======================================================================================================================
'''

#Isolate Fluorescent
Circles.croppedImages.clear() #wipe the croppedimages
Circles.isolateWells(img_F)                #isolate wells in Fl picture



#Cropping out wells
croppedImage = Circles.croppedImages[39] #THE ARRAY OF ISOLATED WELL's first picture [39] has filament

#plt.imshow(croppedImage)
#plt.show()

FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
print("Filament size : ",detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage))
#Locate droplets
CellsInsideCroppedImage = detectionAlgo.detectDroplets(croppedImage.copy()) #the location of all cells inside the cropped image
print(len(CellsInsideCroppedImage))

#Drolet ruling out criteria
if len(CellsInsideCroppedImage) > 1:
    #do nothing because well is invalid due to having more than 1 droplet
    print("There is more than 1 droplet inside the well")

else:
    if len(CellsInsideCroppedImage) == 1 : #if we
        if (cv2.contourArea(CellsInsideCroppedImage[0]) < 15):
            #if area of our individual droplet is less than 15 then remove them from array
            print("Droplet too small, do not analyze")
        else:
            #Record our data

            cellFluorescence = detectionAlgo.intensityFluores(croppedImage)
            print("Cell fluorescence : ",cellFluorescence)
            #end record



            #analyze filament
            #cnt = max(contours_isolated, key=cv2.contourArea)
            print()



#Finish

#Filament growth level
#filament_level = detectionAlgo.intensityFluores(croppedImage)
#print("Filament growth level (pixels): ", filament_level)
#Fluorescence growth level
#fluorescence_level = detectionAlgo.sizeGrowth(croppedImage)
#print("Fluorescence growth level (pixels): ", fluorescence_level)


#Filament size max?
'''

cv2.waitKey(0)
