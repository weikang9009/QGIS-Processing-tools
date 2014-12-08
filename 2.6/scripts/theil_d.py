##Inequality=group
##input=vector
##attribute=field input
##regime=field input

import pysal 
import numpy as np
import processing 
from processing.tools.vector import VectorWriter
from qgis.core import *
from PyQt4.QtCore import *


layer = processing.getObject(input)
provider = layer.dataProvider()
fields = provider.fields()
f = pysal.open(pysal.examples.get_path(input.replace('.shp','.dbf')))

y = np.array(f.by_col[str(attribute)])
r = np.array(f.by_col[str(regime)])
theil_d = pysal.TheilDSim(y,r,99)

print "Theil Inequality Decomposition"
print "Attribute: ", attribute
print "Regime:  ", regime
print "Global inequality T: ", theil_d.T
print "Within regions: ", theil_d.wg[0][0]
print "Between regions: ", theil_d.bg[0][0]
print "p-value: ",theil_d.bg_pvalue[0]
