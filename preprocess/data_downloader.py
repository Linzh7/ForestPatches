
from owslib.wms import WebMapService
import numpy as np

URL = {"luke": "https://kartta.luke.fi/geoserver/MVMI/wms?service=wms&version=1.3.0&request=GetCapabilities", 
       "helsinki": "https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities",
       "syke": "https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS"}

wms = WebMapService(URL["helsinki"], version='1.3.0')

OUT_DIR = "../downloads/helsinki2019/"
dataset = "avoindata:Ortoilmakuva_2019_20cm"

# boundary coordinates
x_min = 24.90468
y_min = 60.18871
x_max = 24.94942
y_max = 60.22032

no_tiles_x = 10 #number of pictures along x-axis
no_tiles_y = 10 #number of pictures along y-axis

# the boundaries for small pictures
xs = np.linspace(x_min, x_max, no_tiles_x + 1)
ys = np.linspace(y_min, y_max, no_tiles_y + 1) 
 
for i in range(0, no_tiles_x):
    print(f"processing column {i}")
    for j in range(0, no_tiles_y):
        bbox = (xs[i], ys[j], xs[i+1], ys[j+1]) 
        img = wms.getmap(layers=[dataset], srs='CRS:84', bbox=bbox, size=(512, 512), format='image/jpeg')
        filename = f"{dataset}_{xs[i]}_{ys[j]}_{xs[i+1]}_{ys[j+1]}.jpg" 
        out = open(OUT_DIR + filename, 'wb')
        out.write(img.read())
        out.close()