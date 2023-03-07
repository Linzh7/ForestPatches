from owslib.wms import WebMapService
import numpy as np
import os
import tqdm
import linzhutils as lu

URL = {
    "luke":
    "https://kartta.luke.fi/geoserver/MVMI/wms?service=wms&version=1.3.0&request=GetCapabilities",
    "helsinki":
    "https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities",
    "syke":
    "https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS"
}

# NEED TO EDIT FOR DIFFERENT DATA
## e.g., Image: "avoindata:Ortoilmakuva_2019_20cm", Mask(luke): "kuusi_1519"
DATASET = ["kuusi_1519", 'manty_1519', 'koivu_1519', 'muulp_1519']
# server name, (helsinki, luke, syke)
WMS_SERVER = "luke"
# make sure that the prefix are same in map and masks
DATA_NAME = 'hel2019'
# image format， png is required for masks, otherwise jpg is fine.
FORMAT = 'png'

# output dir
OUT_DIR = f"./data/{DATA_NAME}/"

# server
wms = WebMapService(URL[WMS_SERVER], version='1.3.0')

# boundary coordinates
x_min = 24.90468
y_min = 60.18871
x_max = 24.94942
y_max = 60.22032

no_tiles_x = 10  #number of pictures along x-axis
no_tiles_y = 10  #number of pictures along y-axis

# the boundaries for small pictures
xs = np.linspace(x_min, x_max, no_tiles_x + 1)
ys = np.linspace(y_min, y_max, no_tiles_y + 1)

# NOTE: download images as PNG, not JPEG, to avoid compression artifacts. Especially for masks.
if __name__ == "__main__":
    lu.checkDir(OUT_DIR)
    with open(os.path.join(OUT_DIR, 'range_info.csv'), 'w') as f:
        for dataset in DATASET:
            print(f"Processing dataset {dataset}")
            DOWNLOAD_DIR = os.path.join(
                OUT_DIR,
                'images' if WMS_SERVER == 'helsinki' else 'color_masks',
                dataset)
            lu.checkDir(DOWNLOAD_DIR)
            for i in tqdm.tqdm(range(0, no_tiles_x)):
                for j in range(0, no_tiles_y):
                    bbox = (xs[i], ys[j], xs[i + 1], ys[j + 1])
                    try:
                        img = wms.getmap(layers=[dataset],
                                         srs='CRS:84',
                                         bbox=bbox,
                                         size=(512, 512),
                                         format=f'image/{FORMAT}')
                        filename = f"{DATA_NAME}_{i}_{j}.{FORMAT}"
                        out = open(os.path.join(DOWNLOAD_DIR, filename), 'wb')
                        out.write(img.read())
                        out.close()
                    except Exception as e:
                        print(f"Error: {e}")
                        continue
                    f.write(
                        f"{os.path.join(DOWNLOAD_DIR,filename)},{xs[i]:.8f},{ys[j]:.8f},{xs[i + 1]:.8f},{ys[j + 1]:.8f}\n"
                    )
