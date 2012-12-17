'''
Grab Citrix Receiver info
'''
import os, csv, random

APP_LIB_PATH = os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps','BD-Datagen-XENAPP')

class CtxReceiverClients(object):
    
    def __init__(self):

	self.datadir = os.path.join(os.path.dirname(__file__), 'data')
	self.cache = list()
	f = open(os.path.join(APP_LIB_PATH,'bin','data','ctxReceiverClients.csv'))
	c = csv.reader(f)
	
	for row in c:
	    
	    r = {
	    'ClientVersion' : row[0],
	    'ClientProductID' : row[1],
	    'ClientBuildNumber' : row[2]
	    }

	    self.cache.append(r)
	    
	f.close()

    def getCtxReceiverClient(self):

	return self.cache[random.randint(0, len(self.cache)-1)]