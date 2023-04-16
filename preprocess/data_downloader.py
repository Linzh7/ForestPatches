
from owslib.wms import WebMapService
import numpy as np

URL = {"luke": "https://kartta.luke.fi/geoserver/MVMI/wms?service=wms&version=1.3.0&request=GetCapabilities", 
       "helsinki": "https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities",
       "syke": "https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS"}

wms = WebMapService(URL["luke"], version='1.3.0')
#print(wms.getOperationByName('GetMap').formatOptions)

OUT_DIR = "../downloads/spruce2011/"
dataset = "kuusi_0711"

# boundary coordinates
x_min = 24.90
y_min = 60.19
x_max = 25.10
y_max = 60.29

no_tiles_x = 40 #number of pictures along x-axis
no_tiles_y = 20 #number of pictures along y-axis

# the boundaries for small pictures
xs = np.linspace(x_min, x_max, no_tiles_x + 1)
ys = np.linspace(y_min, y_max, no_tiles_y + 1) 
 
for i in range(4, no_tiles_x):
    print(f"processing column {i}")
    for j in range(no_tiles_y - 1, -1, -1):
        bbox = (xs[i], ys[j], xs[i+1], ys[j+1]) 
        img = wms.getmap(layers=[dataset], srs='CRS:84', bbox=bbox, size=(1024, 1024), format='image/geotiff')
        filename = f"{dataset}_{i}_{j}.tif" 
        out = open(OUT_DIR + filename, 'wb')
        out.write(img.read())
        out.close()