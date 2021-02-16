import cv2
import numpy as np


def detectFluores(image):
    gray = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
#convert gray image to 8UC1 format
    gray8UC1 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Output gray', gray8UC1)
    # cv2.waitKey(0)

    #extract binary
    ret, thresh1 = cv2.threshold(gray8UC1, 55, 255, cv2.THRESH_BINARY)
    cv2.imshow('Output thresh', thresh1)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Output', img)
    cv2.waitKey(0)
    return img


img = cv2.imread(r"C:\Users\mperl\Desktop\test1.png", 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

detectFluores(img)
circles = cv2.HoughCircles(img
                           ,cv2.HOUGH_GRADIENT,1,300,
                          param1=20,param2=180,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
#draw the outer circle
   cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
#draw the center of the circle
   cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()


def addWells(index, y_pos, x_pos, radius, cropped_img):
    "adding a well to the wells array"
    wellArray = {}
    wellArray.insert(index, [cropped_img, y_pos, x_pos, radius])  # inserts well at a given index
    return
