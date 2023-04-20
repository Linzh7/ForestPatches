import argparse
import numpy as np
import cv2
import os
import linzhutils as lu
from tqdm import tqdm
import json


def bin_mask_process(mask, color_list):
    """
    Convert color mask to binary mask
    """
    bin_mask = np.zeros(mask.shape[:2], dtype=np.uint8)  # 0 for background
    for color in color_list:
        color_mask = np.all(mask == color,
                            axis=-1)  # for each color in color_list
        bin_mask = np.logical_or(bin_mask,
                                 color_mask)  # get the union of all colors
    bin_mask = np.logical_not(bin_mask)  # invert the mask
    return bin_mask * 1  # transform to 0, 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--config',
                        help='path to config file',
                        default='./preprocess/mask_conf_kussi.json',
                       )
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = json.load(f)

    input_path = config['input_path']
    output_path = config['output_path']
    color_list = config['color_list']

    file_list = lu.getFileList(input_path)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in tqdm(file_list):
        file_path = os.path.join(input_path, file)
        if not file.endswith(
            ('.jpg', '.png', '.jpeg')):  # skip non-image files
            continue
        mask = cv2.imread(file_path)
        bin_mask = bin_mask_process(mask, color_list)
        cv2.imwrite(os.path.join(output_path, file), bin_mask)
