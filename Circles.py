import cv2
import numpy as np

# GLOBAL VARIABLES
wellArray = {}  # array to store our

vCircles = 0;  # Storing all our wells locations for re-use later, should only find this value once technically.     **set in detectWells**
croppedImages = []  # List to store our cropped (blacked out edges) well images individually.                       **filled in isolateWells**


def detectFluores(image):
    # CV2 doesnt like some thing
    #gray = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    # convert gray image to 8UC1 format
    gray8UC1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Output gray', gray8UC1)
    cv2.waitKey(0)

    # extract binary
    ret, thresh1 = cv2.threshold(gray8UC1, 25, 255, cv2.THRESH_BINARY)
    pixelCountValue = cv2.countNonZero(thresh1)
    print(pixelCountValue)
    cv2.imshow('Output thresh', thresh1)
    cv2.waitKey(0)

    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img = cv2.drawContours(image, contours, -1, (255, 255, 255), 2)
    cv2.imshow('Output', img)
    cv2.waitKey(0)
    gray8UC1_test = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1, thresh12 = cv2.threshold(gray8UC1_test, 254, 255, cv2.THRESH_BINARY)
    pixelContourValue = cv2.countNonZero(thresh12)
    cv2.imshow('Output thresh', thresh12)
    cv2.waitKey(0)

    return pixelCountValue-pixelContourValue

#img = cv2.imread(r"C:\Users\Ruslan\Desktop\test2.png")
# # # img = cv2.medianBlur(img,5)
#print(detectFluores(img))

def detectWells(img, minimumradius, maximumradius, debugbool,path):
    # minimumradius default : 130
    # maximumradius default : 180
    minimumdistance = 150  # minimum distance between any two cells default 150

    #img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # detectFluores(img)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, minimumdistance,
                               param1=30, param2=20, minRadius=minimumradius, maxRadius=maximumradius)

    circles = np.uint16(np.around(circles))
    if debugbool == True:
        pos=0 #used to number the wells
        # if we're debugging print out the circles over the image
        for i in circles[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
            cv2.putText(cimg, str(pos), (i[0],i[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA) #REMOVED FOR CONFLICT WITH CONTOUR LOWER DOWN
            pos=pos+1

    if debugbool == True:
        #debug ######
        scale_percent = 30 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(cimg, dim, interpolation = cv2.INTER_AREA)
        winname = "Debug detectwells"
        cv2.namedWindow(winname)        # Create a named window
        cv2.moveWindow(winname, 1000,1000)  # Move it to (40,30)
        cv2.imshow(winname, resized)
        cv2.imwrite(path + '/Data/DetectedWells.tiff',cimg)
        cv2.waitKey(0)



        #############



        # # percent of original size
       # width = int(img.shape[1] * scale_percent / 100)
       # height = int(img.shape[0] * scale_percent / 100)
       # dim = (width, height)
        # dim = (200, 200)
       # resized = cv2.resize(cimg, dim, interpolation = cv2.INTER_AREA)
      #  winname = "Debug detectwells"
      #  cv2.namedWindow(winname)        # Create a named window
       # cv2.moveWindow(winname, 1000,1000)  # Move it to (40,30)
       # cv2.imshow(winname, resized)
        ##cv2.imshow("Debug detectwells",resized)
       # cv2.waitKey(0)
        #debug ######


    global vCircles
    vCircles = circles  # add our Circle locations into global circles variable


def isolateWells(img):
    global vCircles
    circles = vCircles
    img = cv2.medianBlur(img, 5)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    pos=0

    global croppedImages
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 3)
        # i[0] & i[1] are x,Y coords of center point
        # i[2] is radius

        # Arrayofwells = DefineArray[ArrayOfWells,i[0],i[1],i[2]]

        # draw the center of the circle
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
        # Draw index #
        # cv2.putText(cimg, '{}'.format(pos), (i[0],i[1]), font, 1, (0, 255, 0), 2, cv2.LINE_AA) #REMOVED FOR CONFLICT WITH CONTOUR LOWER DOWN
        # Crop image
        centerx = int(i[0])
        centery = int(i[1])
        radius = int(i[2])

        lowery = centery + radius
        uppery = centery - radius
        lowerx = centerx + radius
        upperx = centerx - radius
        if lowery < 0:
            lowery = 0
        if lowerx < 0:
            lowerx = 0
        if uppery < 0:
            uppery = 0
        if upperx < 0:
            upperx = 0

        croppedImage_numbered = cimg[uppery:lowery, upperx:lowerx].copy()
        croppedImage_raw = img[uppery:lowery, upperx:lowerx].copy()
        gray8UC1 = cv2.cvtColor(croppedImage_numbered, cv2.COLOR_BGR2GRAY)

      #  ret, thresh1 = cv2.threshold(gray8UC1, 30, 255, cv2.THRESH_BINARY)
       # contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
       # img2 = cv2.drawContours(croppedImage_raw, contours, -1, (0, 255, 0), 0)  # outer edge

       # contours, hierarchy = cv2.findContours(gray8UC1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #img3 = cv2.drawContours(croppedImage_numbered, contours, -1, (0, 255, 0), 3)

       # gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
       # ret, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        #cnts = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cnts[0] if len(cnts) == 2 else cnts[1]

#        cv2.drawContours(thresh2, cnts, 4, (255, 255, 255), cv2.FILLED)  # our MASK

        # Generate mask

        mask = np.zeros_like(img)
        mask = cv2.circle(mask, (i[0], i[1]), i[2]-10, (255, 255, 255), -1)
        croppedmask = mask[uppery:lowery, upperx:lowerx].copy()
        maskedImage = cv2.bitwise_and(croppedImage_raw, croppedmask)  ### THE FINAL CROPPED IMAGE WITH BLACK BACKGROUND
        croppedImages.append(maskedImage)
        pos = pos + 1
        print("Done isolatewells # " ,pos, " out of ", len(circles))
        ##DEBUG PRINTOUT
        #dim = (200, 200)
        #resized = cv2.resize(maskedImage, dim, interpolation = cv2.INTER_AREA)
        #winname = "Debug isolatewells"
        #cv2.namedWindow(winname)        # Create a named window
        #cv2.moveWindow(winname, 1000,1000)  # Move it to (40,30)
        #cv2.imshow(winname, resized)
        #cv2.waitKey(0)

        #cv2.imshow("Debug isolatewells",maskedImage)
        #cv2.waitKey(0)
        ##DEBUG END

def addWells(index, y_pos, x_pos, radius, cropped_img):
    "adding a well to the wells array"
    wellArray.insert(index, [cropped_img, y_pos, x_pos, radius])  # inserts well at a given index
    return
