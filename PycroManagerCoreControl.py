from pycromanager import Acquisition, multi_d_acquisition_events, Bridge, Dataset
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time, math
import os, sys
from PIL import Image

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
        event_queue.put(None)
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






    # 
    # Turn this into a stitching function with argument the channel

    #stitched_img = dataset.read_image(position=0)
    #stitched_img2 = dataset.read_image(position=0)
    #globals()['string%s' % x] = 'Hello'

    #length=16
    posrange = int(math.sqrt(length))
    posincrement = posrange

    #Stitchedrow1=stitched_img
    #Stitchedrow2=stitched_img

    #Merged1=stitched_img
    #Merged2= stitched_img
    stitched_image=[]
    toggle=0
    index=0
    itteration=0
    while index<length:
        imgtable1 =[]
        imgtable2 =[]
        flippedimg=[]
        if toggle==0: #only do this one once

            for x_pos in range(index,posrange):
                if index<length-1:
                    print(index)

                    img = dataset.read_image(position=index , channel_name = channelName)
                    imgtable1.append(img)
                    index=index+1

            newimg=cv2.vconcat(imgtable1)
            flippedimg.append(newimg)
            toggle=1
            posrange=index+posincrement
            print("Finished0")

            for x_pos in range(index,posrange):
                if index<=length:
                    print(index)
                    index=index+1
                    img = dataset.read_image(position=x_pos, channel_name = channelName)
                    imgtable2.append(img)
            imgtable2=np.flipud(imgtable2)
            newimg=cv2.vconcat(imgtable2)
            flippedimg.append(newimg)
            toggle=1
            posrange=posrange+posincrement
            print("Finished1")
        if toggle==1:
            flippedimg=flippedimg[::-1]
            flippedimg=cv2.hconcat(flippedimg)
            stitched_image.insert(0,flippedimg) #modify this to add to bottom instead of top
            toggle=0
            itteration=itteration+1
            print("FinishedCombo")

    imgtoshow=cv2.hconcat(stitched_image)
    #plt.imshow(imgtoshow)
    #return stitched_image
    return imgtoshow
    #plt.savefig('foo.png')
    #plt.show()


