
from pycromanager import Acquisition, multi_d_acquisition_events
from matplotlib import pyplot as plt

# with Acquisition('/path/to/saving/dir', 'saving_name', tile_overlap=10) as acq:
# 10 pixel overlap between adjacent tiles
# acquire a 2 x 1 grid
# acq.acquire({'row': 0, 'col': 0})
# acq.acquire({'row': 1, 'col': 0})



acq = Acquisition(magellan_acq_index=0)  # <---- This should use the GUI configs from magellan (micromanager-gui)
acq.await_completion()  # <--- wait till acquisition is done
dataset = acq.get_dataset()  # <---- get our image data
img, img_metadata = dataset.read_image(z=0, read_metadata=True)  # <---- read our z-stack index 0
plt.imshow(img, interpolation='nearest')  # <---- convert numpy array into image
plt.show()  # <--- show us the image