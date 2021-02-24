from cv2 import cv2
import numpy as np
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

    gray = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    gray8UC1 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray8UC1, 55, 255, cv2.THRESH_BINARY)
    pixelCountValue = cv2.countNonZero(thresh1)

    return pixelCountValue

def detectDroplets(c_img):

    minimumradius = 130
    maximumradius = 180
    minimumdistance = 150 #minimum distance between any two cells

    circles = cv2.HoughCircles(c_img, cv2.HOUGH_GRADIENT, 1, minimumdistance,
                               param1=10, param2=70, minRadius=minimumradius, maxRadius=maximumradius)
    circles = np.uint16(np.around(circles))
    return circles