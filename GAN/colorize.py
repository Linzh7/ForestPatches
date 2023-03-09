from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
import warnings
import linzhutils as lu
device.set(device=DeviceId.GPU0)
torch.backends.cudnn.benchmark=True
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
colorizer = get_image_colorizer(artistic=True)

INPUT_DIR = './data/hel2019/images/'
OUTPUT_DIR = './data/hel2019/colored_images/'
INTENSITY = 100 # set above over 100 for better performance, however 110 might be the max value for A100

file_list = lu.getFileList(INPUT_DIR)

for file in file_list:
    colorizer.save_transformed_image(os.path.join(INPUT_DIR,file), os.path.join(OUTPUT_DIR,file), render_factor=INTENSITY)