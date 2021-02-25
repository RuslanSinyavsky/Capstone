import detectionAlgo
import Circles
import cv2

img_fluor = cv2.imread(r"C:\Users\mperl\Desktop\test1.png", 0)
img_fil = cv2.imread(r"C:\Users\mperl\Desktop\test3.png", 0)
fil_test = cv2.imread(r"C:\Users\mperl\Desktop\test2.png")

print(detectionAlgo.sizeGrowth(fil_test))

#Circles.detectWells(img,30,180,True)
#Circles.isolateWells(img)

cv2.waitKey(0)



