from pycromanager import Acquisition, multi_d_acquisition_events, Bridge, Dataset
from matplotlib import pyplot as plt
import numpy as np
import cv2
import time, math
import os, sys, re
from PIL import Image
from math import sqrt
from pathlib import Path


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

#runnumber = 0
def hook_bf(event):
        time.sleep(1)
        return event

def hook_fn(event, bridge, event_queue):
        time.sleep(0)
        #global runnumber
        #if runnumber == 0:
        #    print("in runnumber")
        #    time.sleep(3)
        #runnumber=runnumber+1
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


    with Acquisition(directory=directoryPATH, name=nameofSAVEDFILE , post_hardware_hook_fn=hook, post_camera_hook_fn=hook_fn) as acq:
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
    
    stackfolder = "**/*"
    folder = Path(directoryPATH)
    foldernames = []
    for name in folder.glob('saving_name_*'):
        print (name.stem)
        foldernames.append(name.stem)
    maximum =1
    for file in foldernames:
        number = int(re.search(nameofSAVEDFILE+"_"+'(\d*)', file).group(1))  # assuming filename is "filexxx.txt"
        # compare num to previous max, e.g.
        maximum= number if number > maximum else maximum  # set max = 0 before for-loop
        print(number)

    highest = nameofSAVEDFILE + "_" + str(maximum)


    data_path = os.path.join(folder, highest)

    dataset = Dataset(data_path)
    #dataset = acq.get_dataset()
    #dataset = acq.get_dataset()
    #print(dataset)
    #data_path=str(directoryPATH/saving_name)
    dataset = Dataset(data_path)
    print(dataset.axes)
    print("data_path", data_path)

    length=(len(xyz))

    dataset_metadata = dataset.read_metadata(channel = 0 ,position=1)
    print(dataset_metadata)
    pos=dataset_metadata["Axes"]["position"]
    print(pos)
    if(dataset):

        sizeimg = dataset.read_image(channel = 0, position=0)
        sizeimg = cv2.cvtColor(sizeimg,cv2.COLOR_GRAY2RGB)
        h,w,c = sizeimg.shape
    length=int((sqrt(length))) #size of the grid (row or column should be same technically)
    blank_image = np.zeros((h*(math.ceil(math.sqrt(length))+2),w*(math.ceil(math.sqrt(length))+2),3), np.uint16)


    print("image size ",blank_image.shape)

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
    for dataposition in range(len(xyz)): #do range for all positions in micromanager
        print(dataposition)
        metadata = dataset.read_metadata(channel = 0,position=dataposition)
        img = dataset.read_image(channel = 0, position=dataposition)
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
        img = cv2.flip(img,1)
        xoffset_um=metadata["XPosition_um_Intended"]
        yoffset_um=metadata["YPosition_um_Intended"]

        print("Intended location is : ",xoffset_um,yoffset_um)
        # cv2.imshow("test",img)
        # cv2.waitKey(0)
        xoffset_px= (xoffset_um - dataset.read_metadata(channel = 0, position=0)['XPosition_um_Intended'] )/ pixelsizeinum
        yoffset_px= (yoffset_um - dataset.read_metadata(channel = 0,position=0)['YPosition_um_Intended'] )/ pixelsizeinum
        xoffset_px=int(xoffset_px)
        print("Xoffset ",xoffset_px)
        #print("img max X ",blank_image.shape[0])
        yoffset_px=int(yoffset_px)
        print("Yoffset ",yoffset_px)
        #print("img max Y ",blank_image.shape[1])

        alpha=0
        blank_image[xoffset_px:xoffset_px+(img.shape[1]), yoffset_px:yoffset_px+(img.shape[0])] = cv2.addWeighted(blank_image[xoffset_px:xoffset_px+(img.shape[1]), yoffset_px:yoffset_px+(img.shape[0])],alpha,img,1-alpha,0)
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

    '''
    #show image
    winname = "test"
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 1000,1000)  # Move it to (40,30)

    cv2.imshow(winname, resized)
    cv2.waitKey(0)
    '''
    blank_image = cv2.cvtColor(blank_image,cv2.COLOR_BGR2GRAY)
    return blank_image , pixelsizeinum
    #plt.savefig('foo.png')
    #plt.show()


