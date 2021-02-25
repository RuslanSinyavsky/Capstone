from cv2 import cv2
import numpy as np
import math
from PIL import Image, ImageDraw
from Circles import croppedImages

def intensityFluores(image):

    #CV2 doesnt like some thing need to conver grey to 8UC1 format
    #grey = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #convert gray image to 8UC1 format
    gray8UC1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Output gray', gray8UC1)
    #cv2.waitKey(0)

    #extract binary
    ret, thresh1 = cv2.threshold(gray8UC1, 55, 255, cv2.THRESH_BINARY)
    #Calculate the colored pixels to find the flourecence
    #Todo might need to change as dan doesnt like
    pixelCountValue = cv2.countNonZero(thresh1)

    #print(pixelCountValue)
    #cv2.imshow('Output thresh', thresh1)
    #cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
    #cv2.imshow('Output', img)
    #cv2.waitKey(0)
    return pixelCountValue

def sizeGrowth(image):

    gray8UC1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray8UC1, 95, 30, cv2.THRESH_BINARY)
    pixelCountValue = cv2.countNonZero(thresh1)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
    gray8UC1_test = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, thresh12 = cv2.threshold(gray8UC1_test, 254, 255, cv2.THRESH_BINARY)
    pixelContourValue = cv2.countNonZero(thresh12)

    return pixelCountValue-pixelContourValue        #pixel value of filament

def detectDroplets(c_img):

# Otsu's thresholding
    blur = cv2.GaussianBlur(c_img,(5,5),0)
    ret,th = cv2.threshold(blur,30,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(th.copy(), cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)
    for i in range(0,len(contours)):
        area = cv2.contourArea(contours[i],False)
        arch = cv2.arcLength(contours[i],False)
        roundness = (4* math.pi * area)/math.pow(arch,2)
        if roundness <0.9 :
            #we are not sort of round
            print("not circle detected so removed")
            contours.remove(i)

    out = np.zeros_like(c_img)
    print(len(contours))
    print(len(hierarchy[0][1]))
    holes = [contours[i] for i in range(len(contours)) if hierarchy[0][i][2] >= 0]
    del holes[0]
    print(len(holes))
    cv2.drawContours(c_img, holes, -1, 255, 1)
    #img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    #cnt = contours[7]
   # (x,y),radius = cv2.minEnclosingCircle(cnt)
    #center = (int(x),int(y))
    #radius = int(radius)
    #cv2.circle(c_img,center,radius,(0,255,0),2)
    cv2.imshow('Output', c_img)
    cv2.waitKey(0)
   # center = (int(x),int(y))
    #radius = int(radius)
    #cv2.circle(c_img,center,radius,(0,255,0),2)
    return holes

