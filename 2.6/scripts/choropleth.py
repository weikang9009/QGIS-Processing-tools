##Spatial statistics=group
##input=vector
##field=field input
##classification=selection Quantile; Maximum Breaks; Fisher-Jenks
##classes=selection 3;4;5;6;7;8;9

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

colors = ["#eff3ff", "#bdd7e7", "#6baed6", "#2171b5"]
schemes = {}
schemes[3] = ['#e5f5f9', '#99d8c9', '#2ca25f']
schemes[4] = ['#edf8fb', '#b2e2e2', '#66c2a4', '#238b45']
schemes[5] = ['#edf8fb', '#b2e2e2', '#66c2a4', '#2ca25f', '#006d2c']
schemes[6] = ['#edf8fb', '#ccece6', '#99d8c9', '#66c2a4', '#2ca25f', '#006d2c']
schemes[7] = ['#edf8fb', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#005824']
schemes[8] = ['#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#005824']
schemes[9] = ['#f7fcfd', '#e5f5f9', '#ccece6', '#99d8c9', '#66c2a4', '#41ae76', '#238b45', '#006d2c', '#00441b']

colors = schemes[k]

lower = [min_y]
lower.extend(upper[:-1])
range_list = []
symbols = []
for i in range(k):
    print lower[i], upper[i]
    symbols.append(QgsSymbolV2.defaultSymbol(layer.geometryType()))
    symbols[i].setColor(QtGui.QColor(colors[i]))
    symbols[i].setAlpha(1) # change to option
    label = "%.1f-%.1f"%(lower[i],upper[i])
    range_list.append(QgsRendererRangeV2(lower[i],upper[i],symbols[i], label))

renderer = QgsGraduatedSymbolRendererV2('', range_list)
renderer.setMode(QgsGraduatedSymbolRendererV2.EqualInterval)
renderer.setClassAttribute(field)
layer.setRendererV2(renderer)

QgsMapLayerRegistry.instance().addMapLayer(layer)
iface.mapCanvas().refresh()
iface.legendInterface().refreshLayerSymbology(layer)
iface.mapCanvas().refresh()





