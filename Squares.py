import numpy
from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw

# Hi
# Test

img = cv2.imread(r"C:\Users\gelfa\Desktop\test2.tif", 0)
img = cv2.medianBlur(img, 5)
cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

font = cv2.FONT_HERSHEY_SIMPLEX
distance = 10
pos = 0;
# ArrayOfWells[index,xpos,ypos,radius,..]

circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 150,
                           param1=10, param2=70, minRadius=130, maxRadius=180)

circles = np.uint16(np.around(circles))
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 1)
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

    ret, thresh1 = cv2.threshold(gray8UC1, 30, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img2 = cv2.drawContours(croppedImage_raw, contours, -1, (0, 255, 0), 3) #outer edge


    contours, hierarchy = cv2.findContours(gray8UC1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    img3 = cv2.drawContours(croppedImage_numbered, contours, -1, (0, 255, 0), 1)

    gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    ret, thresh2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    cv2.drawContours(thresh2,cnts,4,(255,255,255),cv2.FILLED) #our MASK

    # Generate mask


    maskedImage = cv2.bitwise_and(croppedImage_raw, thresh2) ### THE FINAL CROPPED IMAGE WITH BLACK BACKGROUND

    #cv2.imshow('cropped',cont_img)

    # cv2.waitKey()
    # print("X: %s    Y: %s  " %(i[0], i[1]))
    pos = pos + 1
cv2.imshow('maskedped', maskedImage)
resized_cimg = cv2.resize(cimg, (0, 0), fx=0.4, fy=0.4)
cv2.imshow('detected circles', resized_cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
msg = "hi again"
# wtf is this shit???
