from pycromanager import Acquisition, multi_d_acquisition_events, Bridge, Dataset
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time, math
import os, sys
from PIL import Image
from math import sqrt

bridge = Bridge()

core = bridge.get_core()

mm = bridge.get_studio()
pm = mm.positions()
mmc = mm.core()
pos_list = pm.get_position_list()
#-------------------------------------------
directoryPATH = 'E:\KENZA Folder\CapstoneTests'
nameofSAVEDFILE = 'saving_name'
#--------------------------------------------
def merge_imagesVertical(file1, file2):
    """Merge two images into one vertical image
    :return: the merged Image object
    """
    image1 = file1
    image2 = file2
    vis=np.concatenate((image1,image2),axis=0)
    return vis

def merge_imagesHorizontal(file1, file2):
    """Merge two images into one Horizontal image
    :return: the merged Image object
    """
    image1 = file1
    image2 = file2
    vis=np.concatenate((image1,image2),axis=1)
    return vis

def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def hook_bf(event):
        time.sleep(1)
        return event

def hook_fn(event, bridge, event_queue):
        time.sleep(0.5)
        return event

def hook_fl(event):
        time.sleep(0)
        return event

def acquireImage(channelGroup,channelName, hook):

    x_array = []
    y_array = []
    z_array = []

    for idx in range(pos_list.get_number_of_positions()):
        pos = pos_list.get_position(idx)
        #pos.go_to_position(pos, mmc)

        x=pos_list.get_position(idx).get(0).x
        y=pos_list.get_position(idx).get(0).y
        z=pos_list.get_position(idx).get(1).x

        x_array.append(x)
        y_array.append(y)
        z_array.append(z)

    x_array = np.array(x_array)
    y_array = np.array(y_array)
    z_array = np.array(z_array)


    with Acquisition(directory=directoryPATH, name=nameofSAVEDFILE , pre_hardware_hook_fn=hook, post_camera_hook_fn=hook_fn) as acq:
        x=np.hstack([x_array[:, None]])
        y=np.hstack([y_array[:, None]])
        z=np.hstack([z_array[:, None]])
        #Generate the events for a single z-stack
        xyz = np.hstack([x_array[:, None], y_array[:, None], z_array[:, None]])
        events = multi_d_acquisition_events(xyz_positions=xyz, channel_group= channelGroup , channels= [channelName] )
        acq.acquire(events)
        #acquire a 2 x 1 grid
        #acq.acquire({'row': 0, 'col': 0})
        #acq.acquire({'row': 1, 'col': 0})


    #data_path ='E:\KENZA Folder\CapstoneTests\saving_name_18'
    #dataset = Dataset(data_path)
    dataset = acq.get_dataset()
    #dataset = acq.get_dataset()

    length=(len(xyz))

    dataset_metadata = dataset.read_metadata(position=10)
    pos=dataset_metadata["Axes"]["position"]
    print(pos)
    if(dataset):

        sizeimg = dataset.read_image(position=0)
        sizeimg = cv2.cvtColor(sizeimg,cv2.COLOR_GRAY2RGB)
        h,w,c = sizeimg.shape
    length=int((sqrt(length))) #size of the grid (row or column should be same technically)
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
    for dataposition in range(99):
        print(dataposition)
        metadata = dataset.read_metadata(position=dataposition)
        img = dataset.read_image(position=dataposition)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        img = cv2.flip(img,1)
        xoffset_um=metadata["XPosition_um_Intended"]
        yoffset_um=metadata["YPosition_um_Intended"]

        print("Intended location is : ",xoffset_um,yoffset_um)
        # cv2.imshow("test",img)
        # cv2.waitKey(0)
        xoffset_px= (xoffset_um - dataset.read_metadata(position=0)['XPosition_um_Intended'] )/ pixelsizeinum
        yoffset_px= (yoffset_um - dataset.read_metadata(position=0)['YPosition_um_Intended'] )/ pixelsizeinum
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
    #plt.savefig('foo.png')
    #plt.show()


