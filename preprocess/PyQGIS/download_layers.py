# must run in QGIS python console

# sources: https://github.com/soiqualang/test_pyQGIS/blob/master/t4_export_png_v2_final_qgis3.py
# with translation

from PyQt5.QtCore import QTimer

#Note that the exported image area is equal to the open map area on QGIS
#So adjust the map display area on QGIS accordingly and then export

#Configure the folder containing the images
filePath = './data/'

#prefixes = ['t_216_TVDI_200003.tif', 't_216_TVDI_200012.tif', 't_216_TVDI_200011.tif']
prefixes = []
count = 0

#scale = 640
layers = []
for layer in QgsProject.instance().mapLayers().values():
    #layers.append(layer)
    #print(layer.id());
    print(layer.name())
    prefixes.append(layer.name())

# print(layers[0].extent())
# map.setExtent(layers[0].extent())
# map.setRect(20, 20, 20, 20)


# Make a list of layers
def prepareMap():
    layers = []
    layers = QgsProject.instance().mapLayers()

    # Turn off all layers
    for layer in layers:
        QgsProject.instance().layerTreeRoot().findLayer(
            layer).setItemVisibilityChecked(False)

    # Select the layer to export
    exportLayers = []
    for layer in QgsProject.instance().mapLayers().values():
        if layer.name().startswith(prefixes[count]):
            QgsProject.instance().layerTreeRoot().findLayer(
                layer).setItemVisibilityChecked(True)
            # iface.actionZoomToSelected().trigger()
            # qgis.utils.iface.mapCanvas().zoomScale(scale)

    QTimer.singleShot(1000, exportMap)  # Chờ 1 giây đẻ export


def exportMap():  # Save as a PNG
    global count
    iface.mapCanvas().saveAsImage(filePath + prefixes[count] + ".png")
    print("Layer", prefixes[count], "Export")
    if count < len(prefixes) - 1:
        QTimer.singleShot(1000,
                          prepareMap)  # Wait 1 second to export the next layer
    count += 1


prepareMap()