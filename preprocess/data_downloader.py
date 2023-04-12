from owslib.wms import WebMapService
import numpy as np
import os
from tqdm import tqdm
import linzhutils as lu
import argparse

parser = argparse.ArgumentParser(prog='Geo Data Downloader',
                                 description='download dataset',
                                 epilog='Text at the bottom of help')
parser.add_argument(
    '-s',
    '--dataset',
    type=int,
    # default=1,
    help='0. luke (mask)\n1. helsinki (map)\n2. syke (mask)',
    # )
    required=True)
parser.add_argument('-d',
                    '--dir',
                    type=str,
                    default='hel2019',
                    help='the output dir, will be filled with ./data/{dir}')
parser.add_argument('-f',
                    '--format',
                    type=str,
                    default='png',
                    help='the filename extension of output files')
# parser.add_argument('-m',
#                     '--maxthreads',
#                     type=int,
#                     default=2,
#                     help='the max number of threads')
parser.add_argument('-z',
                    '--size',
                    type=int,
                    default=10,
                    help='unit in 100m, default 10 for 1x1km per tile')

# parser.add_argument('--', type=str, default='a12', help='dataset parameter')

args = parser.parse_args()

print(args)

URL = {
    "luke":
    "https://kartta.luke.fi/geoserver/MVMI/wms?service=wms&version=1.3.0&request=GetCapabilities",
    "helsinki":
    "https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities",
    "syke":
    "https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS"
}

# NEED TO EDIT FOR DIFFERENT DATA
## e.g., Image: ["avoindata:Ortoilmakuva_2019_20cm"], Mask(luke): ["kuusi_1519",xxxxx]
# ["kuusi_1519", 'manty_1519', 'koivu_1519', 'muulp_1519']
DATASET_LIST = [["kuusi_1519"],
                ["avoindata:Ortoilmakuva_2019_20cm"]]
DATASET = DATASET_LIST[args.dataset]
# server name, (helsinki, luke, syke)
WMS_SERVER_LIST = ["luke", "helsinki"]
WMS_SERVER = WMS_SERVER_LIST[args.dataset]
# make sure that the prefix are same in map and masks
DATA_NAME = args.dir
# image format， png is required for masks, otherwise jpg is fine.
FORMAT = args.format

# output dir
OUT_DIR = f"./data/{DATA_NAME}/"

# server
wms = WebMapService(URL[WMS_SERVER], version='1.3.0')

# boundary coordinates
# 100m in Helsinki area is about 0.0009 longitude, and 0.0012 latitude
TILE_SIZE = args.size  # 100m
SIZE = (int(512 * TILE_SIZE), int(512 * TILE_SIZE))
LONG_IN_M = 0.00090009001 * TILE_SIZE
LATI_IN_M = 0.00127279275 * TILE_SIZE

# Biggest size in 2019
# x_min = 24.819182
# y_min = 60.1212
# x_max = 25.2717
# y_max = 60.295403

# normal size
# x_min = 24.822
# y_min = 60.207
# x_max = 25.1816
# y_max = 60.295403

# Test train size, smaller
x_min = 24.8593
y_min = 60.2003
x_max = 24.9484
y_max = 60.2834

# no_tiles_x = 10  #number of pictures along x-axis
# no_tiles_y = 10  #number of pictures along y-axis

# the boundaries for small pictures
xs = np.arange(x_min, x_max, LONG_IN_M)
ys = np.arange(y_min, y_max, LATI_IN_M)

print(
    f"Tile size: {TILE_SIZE}, \ndataset size:{len(xs)}x{len(ys)} tiles,\nRange: ({x_min}, {y_min}), ({x_max}, {y_max})"
)

# NOTE: download images as PNG, not JPEG, to avoid compression artifacts. Especially for masks.
if __name__ == "__main__":
    lu.checkDir(OUT_DIR)
    for dataset in DATASET:
        with open(os.path.join(OUT_DIR, f'{dataset}_range_info.csv'), 'w') as f:
            print(f"Processing dataset {dataset}")
            DOWNLOAD_DIR = os.path.join(
                OUT_DIR,
                'images' if WMS_SERVER == 'helsinki' else 'color_masks',
                '' if WMS_SERVER == 'helsinki' else dataset.split('_')[0],
            )
            lu.checkDir(DOWNLOAD_DIR)
            for i in tqdm(range(len(xs) - 1)):
                for j in range(len(ys) - 1):
                    bbox = (xs[i], ys[j], xs[i + 1], ys[j + 1])
                    try:
                        img = wms.getmap(layers=[dataset],
                                         srs='CRS:84',
                                         bbox=bbox,
                                         size=SIZE,
                                         format=f'image/{FORMAT}')
                        filename = f"{DATA_NAME}_{i}_{j}.{FORMAT}"
                        out = open(os.path.join(DOWNLOAD_DIR, filename), 'wb')
                        out.write(img.read())
                        out.close()
                    except Exception as e:
                        print(f"Error: {e}, at {bbox}")
                        continue
                    f.write(
                        f"{os.path.join(DOWNLOAD_DIR,filename)},{xs[i]:.8f},{ys[j]:.8f},{xs[i + 1]:.8f},{ys[j + 1]:.8f}\n"
                    )
