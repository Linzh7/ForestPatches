import numpy as np
import cv2
import os
import linzhutils as lu


# convert color mask to binary mask
def bin_mask_process(mask, color_list):
    bin_mask = np.zeros(mask.shape[:2], dtype=np.uint8)  # 0 for background
    for color in color_list:
        color_mask = np.all(mask == color,
                            axis=-1)  # for each color in color_list
        bin_mask = np.logical_or(bin_mask,
                                 color_mask)  # get the union of all colors
    bin_mask = np.logical_not(bin_mask)  # invert the mask
    return bin_mask * 255  # transform to 0, 255


INPUT_PATH = './data/helsinki2019/color_masks/'
OUTPUT_PATH = './data/helsinki2019/bin_masks/'
COLOR_LIST = [(255, 255, 255), (0, 114, 254)]

file_list = lu.getFileList(INPUT_PATH)

if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)
for file in file_list:
    file_path = os.path.join(INPUT_PATH, file)
    if not file.endswith(('.jpg', '.png', '.jpeg')):  # skip non-image files
        continue
    print('Processing: {}'.format(file))
    mask = cv2.imread(file_path)
    bin_mask = bin_mask_process(mask, COLOR_LIST)
    cv2.imwrite(os.path.join(OUTPUT_PATH, file), bin_mask)