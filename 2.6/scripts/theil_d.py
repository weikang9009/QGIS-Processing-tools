##Inequality=group
##input=vector 
##attribute=field input
##regime=field input

import pysal 
import numpy as np
import processing 

layer = processing.getObject(input)
data = processing.values(layer, regime, attribute)
y = np.array(data[attribute])
r = np.array(data[regime])
theil_d = pysal.TheilDSim(y, r, 99)

print "Theil Interregional Inequality Decomposition"
print "Attribute: ", attribute
print "Regime:  ", regime
print "Global inequality T: ", theil_d.T
print "Within regions: ", theil_d.wg[0][0]
print "Between regions: ", theil_d.bg[0][0]
print "p-value: ",theil_d.bg_pvalue[0]

