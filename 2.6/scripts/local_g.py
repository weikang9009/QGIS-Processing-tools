##Spatial statistics=group
##input=vector
##field=field input
##contiguity=string queen
##Local_G=output vector

import pysal 
import numpy as np
import processing 
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *

# np.random.seed(10)

field = field[0:10] # try to handle Shapefile field length limit

layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
fields.append(QgsField('L_G', QVariant.Double))
fields.append(QgsField('L_G_p', QVariant.Double))
fields.append(QgsField('L_G_S', QVariant.Double))
fields.append(QgsField('L_G_ll_hh', QVariant.Double))
writer = VectorWriter(Local_G, None,fields, provider.geometryType(), layer.crs() )

if contiguity == 'queen':
    print 'INFO: Local Getis-Ord G using queen contiguity'
    w=pysal.queen_from_shapefile(input)
else:
    print 'INFO: Local Getis-Ord using rook contiguity'
    w=pysal.rook_from_shapefile(input)

f = pysal.open(pysal.examples.get_path(input.replace('.shp','.dbf')))
y=np.array(f.by_col[str(field)])
lg = pysal.G_Local(y,w,transform = "b", permutations = 999)


sig_g =  1.0 * lg.p_sim <= 0.01 # could make significance level an option
ll_hh = 1.0 * (lg.Gs > lg.EGs) + 1
sig_ll_hh = sig_g * ll_hh
outFeat = QgsFeature()
i = 0
for inFeat in processing.features(layer):
    inGeom = inFeat.geometry()
    outFeat.setGeometry(inGeom)
    attrs = inFeat.attributes()
    attrs.append(float(lg.Gs[i]))
    attrs.append(float(lg.p_sim[i]))
    attrs.append(float(sig_g[i]))
    attrs.append(float(sig_ll_hh[i]))
    outFeat.setAttributes(attrs)
    writer.addFeature(outFeat)
    i+=1

del writer
