import detectionAlgo
import Circles
import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread(r"C:\capstone\test3.tif", 0)
img2 = cv2.imread(r"C:\capstone\test1.png", 0)

#DETECT AND ISOLATE THE WELLS
Circles.detectWells(img,80,180,True)
Circles.isolateWells(img)
Circles.isolateWells(img2)
##Finish detect and isolate wells




croppedimage = Circles.croppedImages[1] #THE ARRAY OF ISOLATED WELL's first picture

plt.imshow(croppedimage)
plt.show()
CellsInsideCroppedImage = detectionAlgo.detectDroplets(croppedimage) #the location of all cells inside the cropped image
print(CellsInsideCroppedImage)
if len(CellsInsideCroppedImage) > 1:
    ## do nothing because well is invalid due to having more than 1 droplet
    print("we have more than 1 cell inside our image")





cv2.waitKey(0)



