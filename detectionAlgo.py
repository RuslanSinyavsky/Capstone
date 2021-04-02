from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw
from Circles import croppedImages
import math

def intensityFluores(image):

    #CV2 doesnt like some thing need to conver grey to 8UC1 format
    grey = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #convert gray image to 8UC1 format
    gray8UC1 = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('Output gray', gray8UC1)
    #cv2.waitKey(0)

    #extract binary
    ret, thresh1 = cv2.threshold(gray8UC1, 30, 255, cv2.THRESH_BINARY)
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
    img = cv2.drawContours(image, contours, -1, (255, 255, 255), 1)
    gray8UC1_test = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, thresh12 = cv2.threshold(gray8UC1_test, 254, 255, cv2.THRESH_BINARY)
    pixelContourValue = cv2.countNonZero(thresh12)

    return pixelCountValue-pixelContourValue        #pixel value of filament

def detectDroplets(c_img):

    # Otsu's thresholding

    blur = cv2.GaussianBlur(c_img,(5,5),0)
    ret,th = cv2.threshold(blur,15,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(th.copy(), cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)

   # print("contours[0] ",contours[0])


    contours2=[]
    for i in range(0,len(contours)):

        area = cv2.contourArea(contours[i],False)
        arch = cv2.arcLength(contours[i],False)
        if arch >0:
            roundness = (4* math.pi * area)/math.pow(arch,2)
        else:
            roundness = 0
        #print("roundness is: ",roundness)
        #print("Roundness : ",roundness)
        if roundness <0.5 :
            #we are not sort of round
            print()
           # print("not circle detected so removed")
           # print("contours : ",len(contours))
            #contours.remove(i)
        else:
            contours2.append(contours[i])

    #image_test = c_img.copy()
    #cv2.drawContours(image_test, contours2, -1, 255, 1) # TEST TO SEE ALL CONTOURS
    #cv2.imshow('Output', image_test)
    #cv2.waitKey(0)

    out = np.zeros_like(c_img)
    #print(len(contours))
   # print(len(hierarchy[0][1]))
    holes = [contours2[i] for i in range(len(contours2)) if (hierarchy[0][i][2] >= 0 )]

    if len(holes)>0:
        del holes[0]



    holes2 = [contours2[i] for i in range(len(contours2)) if hierarchy[0][i][0] >= 0]
    holes3= holes+holes2

    spores = [contours2[i] for i in range(len(contours2)) if hierarchy[0][i][2] != -1] #if there is a child add it to spores list


   # print("holes length =",len(holes3))
    cv2.drawContours(c_img, holes3, -1, 255, 1)
   # print(hierarchy[0][2][2]) #the "child" of the specified contour is in position hierarchy[Next, Previous, First_Child, Parent]

    #img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    #cnt = contours[7]
   # (x,y),radius = cv2.minEnclosingCircle(cnt)
    #center = (int(x),int(y))
    #radius = int(radius)
    #cv2.circle(c_img,center,radius,(0,255,0),2)

    cv2.imshow('Output holes', c_img)     #SHOW THE OUTLINE
    cv2.waitKey(0)

   # center = (int(x),int(y))
    #radius = int(radius)
    #cv2.circle(c_img,center,radius,(0,255,0),2)
    return holes3 , spores


def detectFilament(c_img):



   # contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    ret,th = cv2.threshold(c_img,5,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    contours_thresh, hierarchy_tresh = cv2.findContours(th.copy(), cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)

    mask = np.zeros_like(c_img)
    cv2.drawContours(mask, contours_thresh, -1, 255, -1) #black out the cell
    c_img_masked = cv2.bitwise_and(c_img, c_img, mask=mask)
    c_img_masked_not = cv2.bitwise_not(c_img_masked.copy(),c_img_masked.copy())

    cv2.imshow('Output', c_img) #SHOW THE RAW PICTURE
    cv2.waitKey(0)
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    c_img_masked_dilate = cv2.dilate(c_img_masked_not, np.ones((11, 11)),2)
    c_img_masked_dilate_not = cv2.bitwise_not(c_img_masked_dilate.copy(),c_img_masked_dilate.copy())
    #dilate = cv2.dilate(c_img_masked, kernel, iterations=5)
    #blur_mask = cv2.GaussianBlur(c_img_masked,(5,5),0)

    edges = cv2.Canny(c_img_masked,40,200)
    c_img_masked = cv2.bitwise_and( edges,c_img_masked_dilate_not.copy())

    ret2,th2 = cv2.threshold(c_img_masked,30,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(th2.copy(), cv2.RETR_TREE , cv2.CHAIN_APPROX_NONE)

    for c in contours:
        area = cv2.contourArea(c)

    # Fill very small contours with zero (erase small contours).
        if area < 10:
           cv2.fillPoly(th2, pts=[c], color=0)
           continue
    #th2 = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))); #this one actually closes the filaments individually
    th2 = cv2.morphologyEx(th2, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))); ##close the filaments to get an area
    contours_isolated, hierarchy_isolated = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if(len(contours_isolated)) >0:

        cnt = max(contours_isolated, key=cv2.contourArea)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(th2,center,radius,255,2)
     #   print("we have: ",len(contours))
        cv2.drawContours(c_img_masked, contours_isolated, -1, 255, 3) #contour our actual filament
        cv2.imshow('Output', c_img_masked)
        cv2.waitKey(0)

    return contours_isolated #returns the contour of the actual filament


def maxThreshCalc(img):

    if len(img) > 0:
        c = max(img, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

        return radius