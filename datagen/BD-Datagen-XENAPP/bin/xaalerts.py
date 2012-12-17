'''
Grab XenApp Alert info
'''
import os, csv, random

APP_LIB_PATH = os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps','BD-Datagen-XENAPP')

class XAAlerts(object):
    
    def __init__(self):

	self.datadir = os.path.join(os.path.dirname(__file__), 'data')
	self.cache = list()
	f = open(os.path.join(APP_LIB_PATH,'bin','data','XenAppAlerts.csv'), "rU")
	c = csv.reader(f)
	
	for row in c:
	    
	    r = {
	    'source' : row[0],
	    'Value' : row[1],
	    'alert_name' : row[2],
	    'usrexp' : row[3]
	    }

	    self.cache.append(r)
	    
	f.close()

    def getXAAlert(self):
	return self.cache[random.randint(0, len(self.cache)-1)]