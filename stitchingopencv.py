from pycromanager import Acquisition, multi_d_acquisition_events, Bridge, Dataset
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time, math
import os, sys
from PIL import Image
from math import sqrt

#data_path =r'C:\Users\gelfa\Desktop\saving_name_56'


def direct_stitch(data_path):
    dataset = Dataset(data_path)
    print(dataset.axes)
    dataset_metadata = dataset.read_metadata(channel = 0,position=0)
    print(dataset_metadata)
    pos=dataset_metadata["Axes"]["position"]
    print(pos)
    if(dataset):

        sizeimg = dataset.read_image(channel = 0,position=0)
        sizeimg = cv2.cvtColor(sizeimg,cv2.COLOR_GRAY2RGB)
        h,w,c = sizeimg.shape
    length=10 #size of the grid (row or column should be same technically)
    blank_image = np.ones((h*(length+1),w*(length+1),3), np.uint16)


    print("image size ",blank_image.shape)
    print(dataset_metadata)
    pixelsizeinum = dataset_metadata["PixelSizeUm"] #get size of pixel in um
    print(pixelsizeinum)

    """
    for datarow in range(10):
        for datacolumn in range(10):
            metadata = dataset.read_metadata(row=datarow, col=datacolumn)
            if(metadata["Axes"]["position"]>=0):
                pos=metadata["Axes"]["position"]
                #print(pos)
                img = dataset.read_image(position=pos)
            
    
                img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
                cv2.imshow("test",img)
    """
    xtotaloffset=0
    ytotaloffset=0
    for dataposition in range(70):
        print(dataposition)
        metadata = dataset.read_metadata(channel = 0,position=dataposition)
        img = dataset.read_image(channel = 0,position=dataposition)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        img = cv2.flip(img,1)
        xoffset_um=metadata["XPosition_um_Intended"]
        yoffset_um=metadata["YPosition_um_Intended"]

        print("Intended location is : ",xoffset_um,yoffset_um)
        # cv2.imshow("test",img)
        # cv2.waitKey(0)
        xoffset_px= (xoffset_um - dataset.read_metadata(channel = 0,position=0)['XPosition_um_Intended'] )/ pixelsizeinum
        yoffset_px= (yoffset_um - dataset.read_metadata(channel = 0,position=0)['YPosition_um_Intended'] )/ pixelsizeinum
        xoffset_px=int(xoffset_px)
        print("Xoffset ",xoffset_px)
        #print("img max X ",blank_image.shape[0])
        yoffset_px=int(yoffset_px)
        print("Yoffset ",yoffset_px)
        #print("img max Y ",blank_image.shape[1])


        blank_image[xoffset_px:xoffset_px+(img.shape[1]), yoffset_px:yoffset_px+(img.shape[0])] += img
        #blank_image[:yoffset_px+img.shape[0], :xoffset_px+img.shape[1]] = img
        #blank_image = cv2.addWeighted(blank_image[yoffset_px:yoffset_px+img.shape[0], xoffset_px:xoffset_px+img.shape[1]],img)


    ####################
    #printout only ignore
    ####################
    scale_percent = 5
    width = int(blank_image.shape[1] * scale_percent / 100)
    height = int(blank_image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(blank_image, dim, interpolation = cv2.INTER_AREA)
    winname = "test"
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 1000,1000)  # Move it to (40,30)
    cv2.imshow(winname, resized)
    cv2.waitKey(0)

    return blank_image

