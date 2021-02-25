import detectionAlgo
import Circles
import cv2
import numpy as np
from matplotlib import pyplot as plt

fil_test = cv2.imread(r"C:\Users\mperl\Desktop\test2.png")      #just to test filament pixel count

#Images to use for demo
img_BF = cv2.imread(r"C:\capstone\test3.tif", 0)       #BF image
img_F = cv2.imread(r"C:\capstone\test1.png", 0)        #FL image
#print(detectionAlgo.sizeGrowth(fil_test))

#Locate Wells
Circles.detectWells(img_BF,80,180,True)    #detect wells in BF picture
Circles.isolateWells(img_BF)               #isolate wells in BF picture
Circles.isolateWells(img_F)                #isolate wells in Fl picture
#Finish

#Cropping out wells
croppedImage = Circles.croppedImages[39] #THE ARRAY OF ISOLATED WELL's first picture [39] has filament

#plt.imshow(croppedImage)
#plt.show()

#Detect filament



#Locate droplets
CellsInsideCroppedImage = detectionAlgo.detectDroplets(croppedImage.copy()) #the location of all cells inside the cropped image
print(len(CellsInsideCroppedImage))

#Drolet ruling out criteria
if len(CellsInsideCroppedImage) > 1:
    #do nothing because well is invalid due to having more than 1 droplet
    print("There is more than 1 droplet inside the well")

else:
    if (cv2.contourArea(CellsInsideCroppedImage[0]) < 15):
        #if area of our individual droplet is less than 15 then remove them from array
        print("Droplet too small, do not analyze")
    else:
        #analyze filament
        FilamentsInsideCroppedImage = detectionAlgo.detectFilament(croppedImage.copy())
#Finish

#Filament growth level
#filament_level = detectionAlgo.intensityFluores(croppedImage)
#print("Filament growth level (pixels): ", filament_level)
#Fluorescence growth level
#fluorescence_level = detectionAlgo.sizeGrowth(croppedImage)
#print("Fluorescence growth level (pixels): ", fluorescence_level)


#Filament size max?


cv2.waitKey(0)