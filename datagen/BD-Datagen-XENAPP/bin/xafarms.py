'''
Grab XenApp farm info
'''
import os, csv, random

APP_LIB_PATH = os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps','BD-Datagen-XENAPP')

class XAFarms(object):
    
    def __init__(self):

	self.datadir = os.path.join(os.path.dirname(__file__), 'data')
	self.cache = list()
	f = open(os.path.join(APP_LIB_PATH,'bin','data','XenAppFarms.csv'))
	c = csv.reader(f)
	
	for row in c:
	    
	    r = {
	    'FarmName' : row[0],
	    'ServerCount' : row[1],
	    'AppCount' : row[2]
	    }

	    self.cache.append(r)
	    
	f.close()

    def getXAFarm(self, farmName):
	return self.cache[farmName]