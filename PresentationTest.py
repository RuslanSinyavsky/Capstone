import detectionAlgo
import Circles
import cv2



img = cv2.imread(r"C:\capstone\filament.tif", 0)


Circles.detectWells(img,30,180,True)
Circles.isolateWells(img)


cv2.waitKey(0)



