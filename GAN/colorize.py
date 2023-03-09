from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
device.set(device=DeviceId.GPU0)
torch.backends.cudnn.benchmark=True
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
colorizer = get_image_colorizer(artistic=True)

file_list = []

for file in file_list:
    colorizer.plot_transformed_image('test_images/image.jpg', render_factor=i, display_render_factor=True)