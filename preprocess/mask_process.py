import numpy as np
import cv2
import os
import linzhutils as lu


def bin_mask_process(mask, color_list):
    bin_mask = np.zeros(mask.shape[:2], dtype=np.uint8)
    for color in color_list:
        color_mask = np.all(mask == color, axis=-1)
        bin_mask = np.logical_or(bin_mask, color_mask)
    return bin_mask * 255


PATH = './data/'
BIN_MASK_PATH = './data/mask/'
COLOR_LIST = [(255, 255, 255), (254, 114, 0)]

file_list = lu.getFileList(PATH)

for file in file_list:
    file_path = os.path.join(PATH, file)
    if not file.endswith(('.jpg', '.png', '.jpeg')):
        continue
    print('Processing: {}'.format(file))
    mask = cv2.imread(file_path)
    bin_mask = bin_mask_process(mask, COLOR_LIST)
    cv2.imwrite(os.path.join(BIN_MASK_PATH, file), bin_mask)
