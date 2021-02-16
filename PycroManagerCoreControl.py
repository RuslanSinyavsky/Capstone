from pycromanager import Acquisition, multi_d_acquisition_events, Bridge, Dataset
from matplotlib import pyplot as plt
import numpy as np
import time
import os, sys
from PIL import Image

bridge = Bridge()
core = bridge.get_core()
mm = bridge.get_studio()
pm = mm.positions()
mmc = mm.core()
pos_list = pm.get_position_list()

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


with Acquisition(directory='E:\KENZA Folder\CapstoneTests', name='saving_name') as acq:
    x=np.hstack([x_array[:, None]])
    y=np.hstack([y_array[:, None]])
    z=np.hstack([z_array[:, None]])
    #Generate the events for a single z-stack
    xyz = np.hstack([x_array[:, None], y_array[:, None], z_array[:, None]])
    events = multi_d_acquisition_events(xyz_positions=xyz)
    acq.acquire(events)
    #acquire a 2 x 1 grid
    #acq.acquire({'row': 0, 'col': 0})
    #acq.acquire({'row': 1, 'col': 0})


#data_path ='E:\KENZA Folder\CapstoneTests\saving_name_18'
#dataset = Dataset(data_path)
dataset2 = acq.get_dataset()
#dataset = acq.get_dataset()

length=(len(xyz))

def merge_images(file1, file2):
    """Merge two images into one vertical image
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    image1 = file1
    image2 = file2

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    # result_width = width1 + width2
    result_width = width1
    # result_height = max(height1, height2)
    result_height = height1 + height2

    print (height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))
    return result

stitched_img = dataset2.read_image(position=0)
img_array=[]

for x_pos in range(length):
    print(x_pos)
    #for y_pos in range(length):
    #print(dataset2.has_image(row=x_pos, col=y_pos))
    img = dataset2.read_image(position=x_pos) # <---- read our z-stack index 0
    #plt.imshow(img)  # <---- convert numpy array into image
    #plt.show()  # <--- show us the image

    img_array.append(img)
    #stiched_img = merge_images(stitched_img, img)

# creates a new empty image, RGB mode, and size 444 by 95
new_im = Image.new('RGB', (444,95))

for elem in img_array:
    for i in xrange(0,444,95):
        im=Image.open(elem)
        new_im.paste(im, (i,0))
new_im.save('test.jpg')

plt.imshow(stitched_img)  # <---- convert numpy array into image
plt.show()  # <--- show us the image


#img = dataset2.read_image(row=0, col=0) # <---- read our z-stack index 0
#plt.imshow(img)  # <---- convert numpy array into image
#plt.show()  # <--- show us the image

