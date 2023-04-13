import argparse
import cv2
import json
import numpy as np
import os
from collections import defaultdict
from tqdm import tqdm
<<<<<<< HEAD
import linzhutils as lu
=======

TEN_COLORS = [(0, 114, 254), (70, 152, 254), (165, 205, 154), (195, 255, 195),
              (115, 243, 131), (22, 231, 24), (0, 205, 2), (0, 130, 1),
              (220, 0, 23), (149, 31, 40)]

SIX_COLORS = [TEN_COLORS[0], TEN_COLORS[2], TEN_COLORS[4]] + TEN_COLORS[6:]

DEFAULT_SHAPE = (512, 512)

COLOR_NUMBER_MAP = {
    'koivu': {
        'number':
        [0, (1 + 4) / 2, (5 + 12) / 2, (13 + 27) / 2, (28 + 54) / 2, 55 * 1.1],
        'color':
        SIX_COLORS,
    },
    'muulp': {
        'number': [0, 1, 2, (3 + 4) / 2, (5 + 16) / 2, 17 * 1.1],
        'color': SIX_COLORS,
    },
    'manty': {
        'number': [
            0,
            (1 + 9) / 2,
            (10 + 20) / 2,
            (21 + 35) / 2,
            (36 + 51) / 2,
            (52 + 68) / 2,
            (69 + 87) / 2,
            (88 + 108) / 2,
            (109 + 144) / 2,
            160 * 1.1,
        ],
        'color':
        TEN_COLORS,
    },
    'kuusi': {
        'number': [
            0, 1, (2 + 3) / 2, (4 + 7) / 2, (8 + 15) / 2, (16 + 29) / 2,
            (30 + 52) / 2, (53 + 95) / 2, (96 + 184) / 2, 200 * 1.1
        ],
        'color':
        TEN_COLORS,
    },
}

INPUT_PATH = './data/hel2019/color_masks/'
OUTPUT_PATH = './data/hel2019/bin_masks/'
# COLOR_LIST = [(255, 255, 255), (0, 114, 254)]
LABEL_LIST = ['koivu', 'muulp', 'manty', 'kuusi']

folder_list = lu.getFolderList(INPUT_PATH)
>>>>>>> 06ce86bf243d6246e80521bd53770ec57ca8597a


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


# convert 4 color masks to 1 binary mask
def bin_mask_process(file_name, shape, folder_list, color_map, input_path):
    other_tree_count = np.zeros(shape, dtype=np.float64)  # other trees
    kuusi_tree_count = np.zeros(shape, dtype=np.float64)  # kuusi trees
    images_dict = get_images(file_name, folder_list,
                             input_path)  # get 4 color masks
    for label, image in images_dict.items():  # for each color mask and image
        if label not in color_map:  # check if the label is in color map
            raise KeyError('Label not found in color map.')
        # get the target count matrix
        target_count = kuusi_tree_count if label == 'kuusi' else other_tree_count
        # for each color in color_list, add the number of trees to the matrix
        for i in range(len(color_map[label]['number'])):
            # get the mask for each color in color_list
            mask = np.all(image == color_map[label]['color'][i], axis=-1)
            # add the amounts of trees to the matrix
            target_count[mask] += color_map[label]['number'][i]
    # get the binary mask
    bin_mask = kuusi_tree_count > other_tree_count
    # return bin_mask * 255  # return the binary mask as black-white images (0-255)
    return bin_mask * 1  # for 0 - background, 1 - target class values


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='path of the configuration file',
        default='./preprocess/1.json',
    )
    # required=True)
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    input_path = config["input_path"]
    output_path = config["output_path"]
    default_shape = tuple(config["default_shape"])
    color_map = config["color_map"]

    folder_list = lu.getFolderList(input_path)
    lu.checkDir(output_path)

    file_count = []
    for folder in folder_list:
        file_count.append(len(lu.getFileList(os.path.join(input_path,
                                                          folder))))
    assert len(
        set(file_count)
    ) == 1, f"We need the same number of files in each folder. However, we have {file_count}"

    file_list = lu.getFileList(os.path.join(input_path, folder_list[0]))
    for file_name in tqdm(file_list):
<<<<<<< HEAD
        bin_mask = bin_mask_process(file_name, default_shape, folder_list,
                                    color_map, input_path)
        cv2.imwrite(os.path.join(output_path, file_name), bin_mask)
=======
        bin_mask = bin_mask_process(file_name)
        cv2.imwrite(os.path.join(OUTPUT_PATH, file_name), bin_mask)
>>>>>>> 06ce86bf243d6246e80521bd53770ec57ca8597a
