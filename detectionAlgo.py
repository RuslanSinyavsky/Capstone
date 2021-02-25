from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw
from Circles import croppedImages
import math

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

    # gray = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    gray8UC1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray8UC1, 95, 30, cv2.THRESH_BINARY)
    pixelCountValue = cv2.countNonZero(thresh1)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(image, contours, -1, (255, 255, 255), 2)
    gray8UC1_test = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, thresh12 = cv2.threshold(gray8UC1_test, 254, 255, cv2.THRESH_BINARY)
    pixelContourValue = cv2.countNonZero(thresh12)


    return pixelCountValue-pixelContourValue

def detectDroplets(c_img):

    minimumradius = 130
    maximumradius = 180
    minimumdistance = 150 #minimum distance between any two cells

    circles = cv2.HoughCircles(c_img, cv2.HOUGH_GRADIENT, 1, minimumdistance,
                               param1=10, param2=70, minRadius=minimumradius, maxRadius=maximumradius)
    circles = np.uint16(np.around(circles))
    return circles

def radiusCalc(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # For testing------------------------------------------#
    # img = cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
    area = cv2.contourArea(contours[0],False)
    radius = int(math.sqrt(area/3.14))
    return radius