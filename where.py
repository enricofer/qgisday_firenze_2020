#from qgis.core import QgsPointXY,QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsMapRendererCustomPainterJob
#from Qt5.QtGui import QImage, QPainter
from PIL import Image

import tempfile
import os

location = QgsPointXY(11.87617,45.41712)
crsSrc = QgsCoordinateReferenceSystem(4326)
crsDest = QgsCoordinateReferenceSystem(3857)
trasformed_location = QgsCoordinateTransform(crsSrc, crsDest, QgsProject.instance()).transform(location)
iface.mapCanvas().setCenter(trasformed_location)
scale = 50
base_dir = os.getcwd()
images = []

def save_image():
    # https://gis.stackexchange.com/questions/245840/wait-for-canvas-to-finish-rendering-before-saving-image?rq=1
    size = iface.mapCanvas().size()
    image = QImage(size, QImage.Format_RGB32)
    painter = QPainter(image)
    settings = iface.mapCanvas().mapSettings()
    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.renderSynchronously()
    painter.end()
    file_name = os.path.join(tempfile.mkdtemp(), 'where.png')
    print (file_name)
    image.save(file_name)
    return file_name

for scale_factor in range (1,22):
    scale = scale * 2
    iface.mapCanvas().zoomScale(scale)
    images.append(Image.open(save_image()))

#https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
loop_images = images + images[::-1]
images[0].save(os.path.join(base_dir, "out.gif"), save_all=True, append_images=loop_images, duration=200, loop=0)
print ( "result:",os.path.join(base_dir, "out.gif"))

    