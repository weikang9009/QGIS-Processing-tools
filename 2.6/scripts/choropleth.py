##Spatial statistics=group
##input=vector
##field=field input
##classification=selection Quantile; Maximum Breaks; Fisher-Jenks
##classes=selection 3;4;5;6;7;8;9
##colorMap=selection Blues; BuGn; BuPu; Greys; OrRd; YlGnBu; YlOrRd


import pysal 
import numpy as np
import processing 
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
from qgis.utils import iface
import sys
import json
from brewer2mpl import sequential

colorMaps = ['Blues', 'BuGn', 'BuPu', 'Greys', 'OrRd', 'YlGnBu', 'YlOrRd']
   
# np.random.seed(10)

field = field[0:10] # try to handle Shapefile field length limit
layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
f = pysal.open(pysal.examples.get_path(input.replace('.shp','.dbf')))

ps = pysal
print str(classification), str(field), int(classes), type(classification)

k = int(classes) + 3
y=np.array(f.by_col[str(field)])

#c = classifiers[str(classification)](y,k)
classifiers={}
classifiers[0] = ps.Quantiles
classifiers[1] = ps.Maximum_Breaks
classifiers[2] = ps.Fisher_Jenks
if classification in classifiers:
    #c=ps.Quantiles(y,k)
    c=classifiers[classification](y,k)

try:
    upper = c.bins.tolist() #for pysal 1.9dev +
except:
    upper = c.bins

min_y = y.min()

print upper,min_y


colors = eval('sequential.'+colorMaps[colorMap])[k].hex_colors

lower = [min_y]
lower.extend(upper[:-1])
range_list = []
symbols = []

for i in range(k):
    print lower[i], upper[i]
    symbols.append(QgsSymbolV2.defaultSymbol(layer.geometryType()))
    symbols[i].setColor(QtGui.QColor(colors[i]))
    symbols[i].setAlpha(1) # change to option
    label = "%#.3g-%#.3g"%(lower[i],upper[i])
    range_list.append(QgsRendererRangeV2(lower[i],upper[i],symbols[i], label))

renderer = QgsGraduatedSymbolRendererV2('', range_list)
renderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
renderer.setClassAttribute(field)
layer.setRendererV2(renderer)

QgsMapLayerRegistry.instance().addMapLayer(layer)
iface.mapCanvas().refresh()
iface.legendInterface().refreshLayerSymbology(layer)
iface.mapCanvas().refresh()
