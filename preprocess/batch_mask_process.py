import argparse
import cv2
import json
import numpy as np
import os
from collections import defaultdict
from functools import partial
from tqdm import tqdm
import linzhutils as lu

def get_images(file_name, folder_list, input_path):
    image_dict = defaultdict(lambda: None)
    for folder in folder_list:
        file_path = os.path.join(input_path, folder, file_name)
        # check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError('File not found.')
        # check if the file is an image
        if not file_name.endswith(('.jpg', '.png', '.jpeg')):
            raise ValueError('File is not an image.')
        image_dict[folder.split('_')[0]] = cv2.imread(file_path)
    # check if all 4 images are found
    assert len(image_dict) == len(folder_list), "We need 4 masks."
    return image_dict

def get_mask_and_write(file_name, default_shape, folder_list, color_map, input_path, output_path):
    bin_mask = bin_mask_process(file_name, default_shape, folder_list, color_map, input_path)
    cv2.imwrite(os.path.join(output_path, file_name), bin_mask)
    return bin_mask

def process_files(file_list, default_shape, folder_list, color_map, input_path, output_path, threshold_memory):
    binary_masks = []
    current_memory = 0
    get_mask_partial = partial(get_mask_and_write, default_shape=default_shape, folder_list=folder_list, color_map=color_map, input_path=input_path, output_path=output_path)
    for file_name in tqdm(file_list):
        bin_mask = get_mask_partial(file_name)
        binary_masks.append(bin_mask)
        current_memory += bin_mask.nbytes
        if current_memory > threshold_memory:
            binary_masks = np.array(binary_masks)
            for idx, bin_mask in enumerate(binary_masks):
                cv2.imwrite(os.path.join(output_path, file_list[idx]), bin_mask)
            binary_masks = []
            current_memory = 0
    if binary_masks:
        binary_masks = np.array(binary_masks)
        for idx, bin_mask in enumerate(binary_masks):
            cv2.imwrite(os.path.join(output_path, file_list[idx]), bin_mask)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='path of the configuration file',
        default='./preprocess/mask_conf_all_tree.json',
    )
    # required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    input_path = config["input_path"]
    output_path = config["output_path"]
    default_shape = tuple(config["default_shape"])
    color_map = config["color_map"]
    threshold_memory = config["threshold_memory"]

    folder_list = lu.getFolderList(input_path)
    lu.checkDir(output_path)

    file_count = []
    for folder in folder_list:
        file_count.append(len(lu.getFileList(os.path.join(input_path, folder))))
    assert len(set(file_count)) == 1, f"We need the same number of files in each folder. However, we have {file_count}"

    file_list = lu.getFileList(os.path.join(input_path, folder_list[0]))
    process_files(file_list, default_shape, folder_list, color_map, input_path, output_path, threshold_memory)
