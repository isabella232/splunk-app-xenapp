'''
Grab XenApp app info
'''
import os, csv, random

APP_LIB_PATH = os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps','BD-Datagen-XENAPP')

class XAApps(object):
    
    def __init__(self):

	self.datadir = os.path.join(os.path.dirname(__file__), 'data')
	self.cache = list()
	f = open(os.path.join(APP_LIB_PATH,'bin','data','XenAppApps.csv'), "rU")
	c = csv.reader(f)
	
	for row in c:
	    
	    r = {
	    'AccessSessionConditions' : row[0],
	    'AccessSessionConditionsEnabled' : row[1],
	    'AddToClientDesktop' : row[2],
	    'AddToClientStartMenu' : row[3],
	    'AlternateProfiles' : row[4],
	    'AnonymousConnectionsAllowed' : row[5],
	    'ApplicationId' : row[6],
	    'ApplicationType' : row[7],
	    'AudioRequired' : row[8],
	    'AudioType' : row[9],
	    'BrowserName' : row[10],
	    'CachingOption' : row[11],
	    'ClientFolder' : row[12],
	    'ColorDepth' : row[13],
	    'CommandLineExecutable' : row[14],
	    'ConnectionsThroughAccessGatewayAllowed' : row[15],
	    'ContentAddress' : row[16],
	    'CpuPriorityLevel' : row[17],
	    'Description' : row[18],
	    'DisplayName' : row[19],
	    'Enabled' : row[20],
	    'EncryptionLevel' : row[21],
	    'EncryptionRequired' : row[22],
	    'FolderPath' : row[23],
	    'HideWhenDisabled' : row[24],
	    'InstanceLimit' : row[25],
	    'LoadBalancingApplicationCheckEnabled' : row[26],
	    'MaximizedOnStartup' : row[27],
	    'MultipleInstancesPerUserAllowed' : row[28],
	    'OfflineAccessAllowed' : row[29],
	    'OtherConnectionsAllowed' : row[30],
	    'PreLaunch' : row[31],
	    'ProfileLocation' : row[32],
	    'ProfileProgramArguments' : row[33],
	    'ProfileProgramName' : row[34],
	    'RunAsLeastPrivilegedUser' : row[35],
	    'SslConnectionEnabled' : row[36],
	    'StartMenuFolder' : row[37],
	    'TitleBarHidden' : row[38],
	    'WaitOnPrinterCreation' : row[39],
	    'WindowType' : row[40],
	    'WorkingDirectory' : row[41]
	    }

	    self.cache.append(r)
	    
	f.close()

    def getXAApp(self):
	return self.cache[random.randint(0, len(self.cache)-1)]