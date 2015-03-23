##Spatial statistics=group
##input=vector
##contiguity=selection ROOK; QUEEN
##n_neighbors=output vector

import pysal 
import numpy as np
import processing 
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *
from itertools import combinations

# np.random.seed(10)

#field = field[0:10] # try to handle Shapefile field length limit


layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
fields.append(QgsField('n_neighbors', QVariant.Double))
writer = VectorWriter(n_neighbors, None,fields, provider.geometryType(), layer.crs() )
print layer

def layerToW(layer, wType='ROOK'):
    # currently queen only to get this working with qgis
    polys = []
    ids = []
    i = 0
    v2p = {}
    iterator = layer.getFeatures()
    if wType == 'QUEEN':
        for feat in iterator:
            geom = feat.geometry()
            if geom.wkbType() == 6: #multipolygon
                polys = geom.asMultiPolygon()
                for poly in polys:
                    for part in poly:
                        for v in part:
                            if v not in v2p:
                                v2p[v] = []
                            v2p[v].append(i)
            else: # polygon
                poly = geom.asPolygon()
                for part in poly:
                    for v in part:
                        if v not in v2p:
                            v2p[v] = []
                        v2p[v].append(i)
            i+=1
    else: #Rook
        e2p = {}
        for feat in iterator:
            geom = feat.geometry()
            if geom.wkbType() == 6: #multipolygon
                polys = geom.asMultiPolygon()
                for poly in polys:
                    for part in poly:
                        lnv = len(part)
                        for oi in range(lnv-1):
                            o = part[oi]
                            d = part[oi+1]
                            od = (o,d)
                            do = (d,o)
                            if od not in e2p:
                                e2p[od] = []
                            if do not in e2p:
                                e2p[do] = []
                            e2p[od].append(i)
                            e2p[do].append(i)
            else: # polygon
                poly = geom.asPolygon()
                for part in poly:
                    for v in part:
                        lnv = len(part)
                        for oi in range(lnv-1):
                            o = part[oi]
                            d = part[oi+1]
                            od = (o,d)
                            do = (d,o)
                            if od not in e2p:
                                e2p[od] = []
                            if do not in e2p:
                                e2p[do] = []
                            e2p[od].append(i)
                            e2p[do].append(i)
            i+=1
        v2p = e2p
    n = i
    neighbors = dict([ (i,[]) for i in xrange(n)])
    for v in v2p:
        vn = list(set(v2p[v]))
        lvn = len(vn)
        if  lvn > 1:
            pairs = combinations(vn,2)
            for i,j in pairs:
                neighbors[i].append(j)
                neighbors[j].append(i)

    for i in neighbors:
        neighbors[i] = list(set(neighbors[i]))


    return pysal.W(neighbors)

contiguity = ["ROOK", "QUEEN"][contiguity]

if contiguity == 'QUEEN':
    print 'INFO:Queen contiguity'
    #w=pysal.queen_from_shapefile(input)
    w = layerToW(layer,'QUEEN')
else:
    print 'INFO: Rook contiguity'
    #w=pysal.rook_from_shapefile(input)
    w = layerToW(layer, 'ROOK')

n_neigh = w.cardinalities.values()
print n_neigh
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
