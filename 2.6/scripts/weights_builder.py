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
from collections import defaultdict


layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
fields.append(QgsField('n_neighbors', QVariant.Double))
writer = VectorWriter(n_neighbors, None,fields, provider.geometryType(), layer.crs() )
print layer

def layerToW(layer, wType='ROOK'):

    polys = []
    ids = []
    v2p = defaultdict(set)
    iterator = layer.getFeatures()
    if wType == 'QUEEN':
        i = 0
        for feat in iterator:
            geom = feat.geometry()
            if geom.wkbType() == 6: #multipolygon
                polys = geom.asMultiPolygon()
            else:
                polys = [geom.asPolygon()] # polygon

            for poly in polys:
                for ring in poly:
                    for v in ring:
                        v2p[v].add(i)

            i += 1
    else: #Rook
        e2p = defaultdict(set)

        i = 0
        for feat in iterator:
            geom = feat.geometry()
            if geom.wkbType() == 6: #multipolygon
                polys = geom.asMultiPolygon()
            else:
                polys = [geom.asPolygon()] #polygon

            for poly in polys:
                for ring in poly:
                    nv = len(ring)
                    for o,d in zip( ring[:-1], ring[1:] ):
                        key = tuple(sorted([o,d], key=lambda e: (e[0], e[1])))
                        e2p[key].add(i)
                        #e2p[d,o].add(i)
            i += 1
        v2p = e2p

    n = i
    neighbors = defaultdict(set)
    for v in v2p:
        vn = v2p[v]
        if  len(vn) > 1:
            for i,j in combinations(vn,2):
                neighbors[i].add(j)
                neighbors[j].add(i)

    return pysal.W(neighbors)

contiguity = ["ROOK", "QUEEN"][contiguity]

if contiguity == 'QUEEN':
    print 'INFO:Queen contiguity'
    w = layerToW(layer,'QUEEN')
else:
    print 'INFO: Rook contiguity'
    w = layerToW(layer, 'ROOK')

n_neigh = w.cardinalities.values()
print 'cardinalities: ', n_neigh
outFeat = QgsFeature()

i = 0
for inFeat in processing.features(layer):
    inGeom = inFeat.geometry()
    outFeat.setGeometry(inGeom)
    attrs = inFeat.attributes()
    attrs.append(float(n_neigh[i]))
    outFeat.setAttributes(attrs)
    writer.addFeature(outFeat)
    i += 1

del writer
