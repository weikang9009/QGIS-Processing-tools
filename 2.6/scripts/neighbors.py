##Spatial statistics=group
##input=vector
##contiguity=string queen
##n_neighbors=output vector

import pysal 
import numpy as np
import processing 
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *

# np.random.seed(10)

#field = field[0:10] # try to handle Shapefile field length limit

layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
fields.append(QgsField('n_neighbors', QVariant.Double))
writer = VectorWriter(n_neighbors, None,fields, provider.geometryType(), layer.crs() )

if contiguity == 'queen':
    print 'INFO:Queen contiguity'
    w=pysal.queen_from_shapefile(input)
else:
    print 'INFO: Rook contiguity'
    w=pysal.rook_from_shapefile(input)

n_neigh = w.cardinalities.values()
outFeat = QgsFeature()
i = 0
for inFeat in processing.features(layer):
    inGeom = inFeat.geometry()
    outFeat.setGeometry(inGeom)
    attrs = inFeat.attributes()
    attrs.append(float(n_neigh[i]))
    outFeat.setAttributes(attrs)
    writer.addFeature(outFeat)
    i+=1

del writer
