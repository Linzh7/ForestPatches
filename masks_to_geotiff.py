import numpy as np
import pandas as pd
import rasterio
from rasterio import CRS
import torch
import glob
import os
#import gdal

PATH_TO_MASKS = '../../../scratch/project_2007251/2019/results'
PATH_TO_CSV = '../../../scratch/project_2007251/2019/hel2019'
PATH_TO_INTERMEDIATE_RES = '/../../../scratch/project_2007251/2019/intermediate'
PATH_FINAL_OUTPUT = '/../../../scratch/project_2007251/2019/'

file_list = np.load(os.path.join(PATH_TO_MASKS,'file_list.npy'))
coordinate_index = pd.read_csv(os.path.join(PATH_TO_CSV,'csv_output.csv'), names=['filename', 'x_min', 'y_min', 'x_max', 'y_max'])

file_index = 0
mask_index = 0

mask_file = np.load(os.path.join(PATH_TO_MASKS,'result_masks_0.npy'))
concatenated = np.concatenate(mask_file, axis=0)
masks = concatenated.reshape(-1, 512, 512)

for i, filepath in enumerate(file_list):
    if mask_index >= masks.shape[0]:
        mask_index = 0
        file_index += 1
        try:
            mask_file = np.load(f'result_masks_{file_index}.npy')
            concatenated = np.concatenate(mask_file, axis=0)
            masks = concatenated.reshape(-1, 512, 512)
        except:
            print(f'file with index {file_index} not found')
            break
    mask = torch.tensor(masks[mask_index] * 255).type(torch.uint8)
    filename = filepath.split('/')[-1]
    coordinates = coordinate_index[coordinate_index['filename'] == filename]
    transform = rasterio.transform.from_bounds(coordinates['x_min'].values[0], coordinates['y_min'].values[0], coordinates['x_max'].values[0], coordinates['y_max'].values[0], width=512, height=512)
    meta = {'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 255.0, 'width': 512, 'height': 512, 'count': 1, 'crs': CRS.from_epsg(4326), 'transform': transform}
    with rasterio.open(os.path.join(PATH_TO_INTERMEDIATE_RES, f'mask_{i}.tif'), 'w', **meta) as dst:
        dst.write(mask, indexes=1) 
    mask_index += 1
    
file_list2 = glob.glob(os.path.join(PATH_TO_INTERMEDIATE_RES, '*'))

vrt = gdal.BuildVRT("", file_list2, separate=False)
g = gdal.Translate(os.path.join(PATH_FINAL_OUTPUT,"helsinki2019.tif"), vrt, format="GTiff")
