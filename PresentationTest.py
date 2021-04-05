import detectionAlgo
import Circles
import cv2
import numpy as np
from matplotlib import pyplot as plt

dataValuesSize = {}
dataValuesFlu = {}
dataValuesFluT = {}
dataValuesSizeT = {}

#Images to use for demo
img_BF = cv2.imread(r"C:\capstone\testimage.tif", 0)       #BF image
#img_F = cv2.imread(r"C:\capstone\test1.png",0)        #FL image

#Locate Wells & isolate Brightfield
Circles.detectWells(img_BF,80,100,True)    #detect wells in BF picture
Circles.isolateWells(img_BF)               #isolate wells in BF picture



#=======================================================================================================================
#---------------------------------------BRIGHTFIELD--------------------------------------------------------------------
#=======================================================================================================================
#Cropping out wells
croppedImage = Circles.croppedImages[41] #THE ARRAY OF ISOLATED WELL's first picture [39] has filament

#plt.imshow(croppedImage)
#plt.show()

#Detect filament

    #FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
    #print("Filament size : ",detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage))

#Locate droplets
CellsInsideCroppedImage , spores = detectionAlgo.detectDroplets(croppedImage.copy()) #the location of all cells inside the cropped image

for x in range(len(Circles.croppedImages)):

    croppedImage = Circles.croppedImages[x]

    for i in range(len(Circles.croppedImages)):
        dataValuesFlu.setdefault(n, {})[i] = algo.intensityFluores(detection.croppedImages[i])
        dataValuesSize.setdefault(n, {})[i] = algo.maxThreshCalc(detection.croppedImages[i])

    CellsInsideCroppedImage , spores = detectionAlgo.detectDroplets(croppedImage.copy())
    print("# spores ",len(spores))
    print("# droplets ",len(CellsInsideCroppedImage))

    #Drolet ruling out criteria
    if len(CellsInsideCroppedImage) > 1:
        #do nothing because well is invalid due to having more than 1 droplet
        print("There is more than 1 droplet inside the well")

    else:
        if len(CellsInsideCroppedImage) == 1 : #if we
            print("there is a droplet BUT")
            if (cv2.contourArea(CellsInsideCroppedImage[0]) < 15):
                #if area of our individual droplet is less than 15 then remove them from array
                print("Droplet too small, do not analyze")
            else:
                #Record our data


                #end record



                #analyze filament

                FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
                print("Filament size : ",detectionAlgo.maxThreshCalc(FilamentsInsideCroppedImage))

                #cnt = max(contours_isolated, key=cv2.contourArea)
                (x,y),radius = cv2.minEnclosingCircle((CellsInsideCroppedImage[0]))
                print("radius of this droplet is = : ",radius)


    #cv2.imshow("Cropped image",croppedImage)
    #cv2.waitKey(0)

for i in range(len(Circles.croppedImages)):
    dataValuesFlu.setdefault("Image Number", {})[i] = detectionAlgo.intensityFluores(Circles.croppedImages[i])


#=======================================================================================================================
#---------------------------------------FLUORESCENCE--------------------------------------------------------------------
#=======================================================================================================================
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