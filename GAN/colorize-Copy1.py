from deoldify import device
from deoldify.device_id import DeviceId
from deoldify.visualize import *
import warnings
import linzhutils as lu
from tqdm import tqdm

import torch

if not torch.cuda.is_available():
    print('GPU not available.')
else:
    print('GPU is available.')
torch.backends.cudnn.benchmark=True

warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")

colorizer = get_image_colorizer(artistic=True)

YEAR='2006'

INPUT_DIR = f'/scratch/project_2007251/hel{YEAR}/images'
OUTPUT_DIR = f'/scratch/project_2007251/hel{YEAR}/colored_images'

lu.checkDir(OUTPUT_DIR)
INTENSITY = 100 # set above over 100 for better performance, however 110 might be the max value for A100

print(INPUT_DIR)

file_list = sorted(lu.getFileList(INPUT_DIR))
target_file_list = sorted(lu.getFileList(OUTPUT_DIR))

for file in tqdm(file_list):
    if file in target_file_list:
        print(f'{file} existed')
        continue
    colorizer.save_transformed_image(os.path.join(INPUT_DIR,file), os.path.join(OUTPUT_DIR,file), render_factor=INTENSITY)
