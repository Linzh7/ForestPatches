from owslib.wms import WebMapService
import tqdm
import numpy as np
import io
from PIL import Image

INDEX = 0

wms_map_list = [
    'https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities',
    'https://kartta.luke.fi/geoserver/MVMI/wms?version=1.3.0',
    'https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS',
]

# NOTE: set different sources here
hel_map = WebMapService(wms_map_list[INDEX])


def layers_filter(hel_map, index):
    if index == 0:  # hel.fi
        return [
            name for name in hel_map.contents
            if ('rtoilmakuva' in name and ('19' in name or '20' in name))
        ]
    elif index == 1:  # luke.fi
        return [name for name in hel_map.contents if ('kuusi' in name)]
    elif index == 2:  # ymparisto.fi
        pass


def get_submap(points, step=0.001, precision=14):
    point1 = points[0]
    point2 = points[1]
    for i in range(int(abs((point2[0] - point1[0])) / step)):
        for j in range(int(abs((point2[1] - point1[1])) / step)):
            a = np.around(point1[0] + i * step, precision)
            b = np.around(point1[1] + j * step, precision)
            c = np.around(point1[0] + (i + 1) * step, precision)
            d = np.around(point1[1] + (j + 1) * step, precision)
            yield (a, b, c, d)


def is_image_useful(image_flow):
    memory_file = io.BytesIO()
    memory_file.write(image_flow.read())
    image = Image.open(memory_file)
    gray_image = np.array(image.convert('L'))
    if gray_image.mean() < 245:
        return True
    else:
        return False


print(
    f'Title: {hel_map.identification.title}\nVersion: {hel_map.identification.version}\nAbstract: {hel_map.identification.abstract}'
)

layer_list = layers_filter(hel_map, INDEX)

# get info we need
info_list = []
srs_amount = 27
for layer in layer_list:
    print(
        f' - Title: {hel_map[layer].title}\n - Range: {hel_map[layer].boundingBoxWGS84}\n - crsOptions: {hel_map[layer].crsOptions}\n - Styles: {hel_map[layer].styles}\n'
    )
    srs_amount = min(srs_amount, len(hel_map[layer].crsOptions))
    print(f' - srs amount: {srs_amount}\n')
    info_list.append({
        'layer': layer,
        'box': hel_map[layer].boundingBoxWGS84,
        'crs': hel_map[layer].crsOptions,
        'style': list(hel_map[layer].styles.keys())
    })

hel_range = ((24.461826, 59.965919), (25.518606, 60.444763))
reduced_hel_range = ((24.9, 60), (25.2, 60.3))

for info in tqdm.tqdm(info_list):
    for srs_index in range(srs_amount):
        for box in get_submap(reduced_hel_range, 0.1):
            img = hel_map.getmap(
                layers=[info['layer']],
                styles=[''],
                srs=info['crs'][srs_index],
                bbox=(24.9, 60.1, 25, 60.3),
                # size=(5120, 5120),
                size=(1024, 1024),
                format='image/png',
                transparent=False)
            if is_image_useful(img):
                print(
                    f'Image {info["layer"]}_{box}_{srs_index} is useful, saving...'
                )
                with open(f'./data/{info["layer"]}_{box}_{srs_index}.png',
                          'wb') as f:
                    f.write(img.read())
            else:
                print(f'Image {info["layer"]}_{box}_{srs_index} is useless')
        print(f'[info] Layer {info["layer"]} is done')
    print(f'[info] Info {info} is done')