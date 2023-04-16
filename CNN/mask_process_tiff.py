#this creates a binary mask from spruce volume data as GeoTIFF
import rasterio
import numpy as np
import os

PATH = ''
MASK_PATH = ''

def getFileList(path):
    for a, b, file in os.walk(path):
        return file

def bin_mask_process(mask, color_list):
    bin_mask = np.zeros(mask.shape[:2], dtype=np.uint8)
    for color in color_list:
        color_mask = np.all(mask == color, axis=-1)
        bin_mask = np.logical_or(bin_mask, color_mask)
    return bin_mask * 255

def get_mask(filename):
    with rasterio.open(filename, 'r') as src:
        arr = src.read()[0]
        mask = ((arr != 0) & (arr != 11)).astype(int)
        bin_mask_meta = src.meta.copy()
        bin_mask_meta.update({'count': 1})
        return mask, src.meta
    
def write_mask(filename, mask, meta):
    with rasterio.open(filename, 'w', **meta) as dst:
        dst.write(mask, 1)

file_list = getFileList(PATH)

for file in file_list:
    src_path = os.path.join(PATH, file)
    mask, meta = get_mask(src_path)
    dst_path = os.path.join(MASK_PATH, file)
    write_mask(dst_path, mask, meta)