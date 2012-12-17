'''
Grab XenApp server info
'''
import os, csv, random

APP_LIB_PATH = os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps','BD-Datagen-XENAPP')

class XAServers(object):
    
    def __init__(self, farmName):

	self.datadir = os.path.join(os.path.dirname(__file__), 'data')
	self.cache = list()
	f = open(os.path.join(APP_LIB_PATH,'bin','data','XenAppServers.csv'))
	c = csv.reader(f)
	
	for row in c:
	    
	    r = {
	    'FarmName' : row[0],
	    'ServerName' : row[1],
	    'ServerIP' : row[2],
	    }

	    if(r["FarmName"] == farmName):
		self.cache.append(r)
	    
	f.close()

    def getXAServer(self):
	return self.cache[random.randint(0, len(self.cache)-1)]
