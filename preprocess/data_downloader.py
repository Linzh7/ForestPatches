from owslib.wms import WebMapService
import tqdm
import numpy as np
import time


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


if __name__ == '__main__':
    INDEX = 1

    wms_map_list = [
        'https://kartta.hel.fi/ws/geoserver/avoindata/wms?request=getCapabilities',
        'https://kartta.luke.fi/geoserver/MVMI/wms?version=1.3.0',
        'https://paikkatieto.ymparisto.fi/arcgis/services/INSPIRE/SYKE_Maanpeite/MapServer/WMSServer?request=GetCapabilities&service=WMS',
    ]

    # NOTE: set different sources here
    hel_map = WebMapService(wms_map_list[INDEX])

    # dataset info
    print(
        f'Title: {hel_map.identification.title}\nVersion: {hel_map.identification.version}\nAbstract: {hel_map.identification.abstract}'
    )

    # get layers we need
    layer_list = layers_filter(hel_map, INDEX)

    # get info we need
    info_list = []
    for layer in layer_list:
        print(
            f' - Title: {hel_map[layer].title}\n - Range: {hel_map[layer].boundingBoxWGS84}\n - crsOptions: {hel_map[layer].crsOptions}\n - Styles: {hel_map[layer].styles}\n'
        )
        info_list.append({
            'layer': layer,
            'box': hel_map[layer].boundingBoxWGS84,
            'crs': hel_map[layer].crsOptions,
            'style': list(hel_map[layer].styles.keys())
        })

    # (left-bottom, right-top)
    hel_range = ((24.461826, 59.965919), (25.518606, 60.444763))
    # fin_range = ((15.604854897351455, 59.35183067646301), (33.12630922296247,
    #                                                        70.07679148715648))
    # (15.49653323229236, 59.33036201524505, 33.127189374041905, 70.10340529761216)

    # download images
    # NOTE: i cannot download images in some situations, maybe they limit the number of requests
    for info in tqdm.tqdm(info_list):
        for box in get_submap(hel_range, 0.01):
            print(
                f'Laying {info["layer"]} on {box}, style: {info["style"][0]}, srs: {info["crs"][0]}'
            )
            img = hel_map.getmap(layers=[info['layer']],
                                 styles=[''],
                                 srs=info['crs'][0],
                                 bbox=box,
                                 size=(512, 512),
                                 format='image/png',
                                 transparent=False)
            with open(f'./data/{info["layer"]}_{box}.png', 'wb') as f:
                f.write(img.read())
            time.sleep(1)
            # break
        break