# # # # # # # # # # # # # # # # # # # # # # #

#	Data Generator for a XA Deployment 

#	- XenApp Sessions
#	- XenApp ICA Session
#	- Windows Perfmon Counters
#	- WinEvent Errors

# # # # # # # # # # # # # # # # # # # # # # #

import time,sys,os,traceback,random,datetime

# # # # # # # # # # # # # # # # # # # # # # #

#
#	Set the START and END fields in DAYS to populate
#	e.g to fill the index 4 days in the past and 2 in the future:
#	_START = -4 
#	_END = 2
#

# # # # # # # # # # # # # # # # # ## # # ## # # #

_START = -2
_END = 2

APP_NAME = 'BD-Datagen-XENAPP'
## Define output log
xa_server_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_server.log'),'w')
xa_farm_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_farm.log'),'w')
xa_serverload_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_serverload.log'),'w')
xa_serverhotfix_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_serverhotfix.log'),'w')
xa_application_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_applications.log'),'w')
xa_sessions_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_sessions.log'),'w')
xa_sessionprocess_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_sessionprocess.log'),'w')
xa_icasession_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_icasessions.log'),'w')
xa_alerts_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xa_alerts.log'),'w')

def logger(string):
	BD_DATAGEN_LOG.write(time.asctime() + ' - ' + string + "\n")
	BD_DATAGEN_LOG.flush()
#	print time.asctime() + ' - ' + string
	return 0

##############################################
#
#    Farm
#
##############################################	
def writeFarmRecord(eventTime, farm):
	
	server = xaServers.getXAServer()
	
	log_line = """***SPLUNK*** host={host}  {time} - FarmName={farmName} SessionCount={sessionCount} Users={userCount} Servers={serverCount} Applications={applicationCount}
""".format(
        time = eventTime,
        farmName = farm["FarmName"],
	sessionCount = str(random.randint(5, int(farm["SessionCount"]))),
	userCount = str(random.randint(5, int(farm["SessionCount"]))),
	serverCount = farm["ServerCount"],
	applicationCount = farm["AppCount"],
	host = server["ServerName"]
	)

	xa_farm_out.writelines(log_line)
	xa_farm_out.flush()


##############################################
#
#    Server
#
##############################################
def writeServerRecord(eventTime, farm):
	
	server = xaServers.getXAServer()
	
	log_line = """***SPLUNK*** host={host} {time} - CitrixEdition="Platinum" CitrixEditionString="PLT" CitrixInstallDate="02/10/2012 06:41:00" CitrixInstallPath="C:\Program Files (x86)\Citrix\" CitrixProductName="Citrix Presentation Server" CitrixServicePack="0" CitrixVersion="6.5.6682" ElectionPreference="MostPreferred"
FolderPath="Servers" IcaPortNumber="1494" IPAddresses="{serverIP}" Is64Bit="True" IsSpoolerHealthy="True" LicenseServerName="lic-01.domain.com" LicenseServerPortNumber="27000" LogOnMode="AllowLogOns" LogOnsEnabled="True"
MachineName="{serverName}" OSServicePack="Service Pack 1" OSVersion="6.1.7601" PcmMode="Normal" RdpPortNumber="3389"
ServerFqdn="{serverName}.domain.com" ServerId="0673-000C-000000BE" ServerName="{serverName}"
SessionCount="{sessionCount}" ZoneName="SFO-1" FarmName="{farmName}" ScriptRunTime="{time}"
""".format(
		time = eventTime,
		serverIP = server["ServerIP"],
		serverName = server["ServerName"],
		sessionCount = str(random.randint(5, int(farm["SessionCount"]))),
		farmName = farm["FarmName"],
		host = server["ServerName"]
	)

	xa_server_out.writelines(log_line)
	xa_server_out.flush()
	
	ServerLoads = ["100","10000","1200","2000","1800"]
	ServerLoad = ServerLoads[random.randint(0,len(ServerLoads)-1)]
	
	log_line = """***SPLUNK*** host={host} {time} - Load="{load}" MachineName="{serverName}" ServerName="{serverName}" FarmName="{farmName}" ScriptRunTime="129816577132435248"
""".format(
		time = eventTime,
		load = ServerLoad,
		serverName = server["ServerName"],
		farmName = server["FarmName"],
		host = server["ServerName"]
	)
	
	xa_serverload_out.writelines(log_line)
	xa_serverload_out.flush()
	
	log_line = """***SPLUNK*** host={host} {time} - HotfixesReplaced="XA600W2K8R2X64001;XA600W2K8R2X64002;XA600W2K8R2X64003;XA600W2K8R2X64004;XA600W2K8R2X64005;XA600W2K8R2X64006;XA600W2K8R2X64007;XA600W2K8R2X64008;XA600W2K8R2X64009;XA600W2K8R2X64010;XA600W2K8R2X64011;XA600W2K8R2X64012;XA600W2K8R2X64013;XA600W2K8R2X64014;XA600W2K8R2X64015;XA600W2K8R2X64016;XA600W2K8R2X64017;XA600W2K8R2X64018;XA600W2K8R2X64019;XA600W2K8R2X64020;XA600W2K8R2X64021;XA600W2K8R2X64022;XA600W2K8R2X64023;XA600W2K8R2X64024;XA600W2K8R2X64025;XA600W2K8R2X64026;XA600W2K8R2X64027;XA600W2K8R2X64028;XA600W2K8R2X64029;XA600W2K8R2X64030;XA600W2K8R2X64031;XA600W2K8R2X64032;XA600W2K8R2X64033;XA600W2K8R2X64034;XA600W2K8R2X64035;XA600W2K8R2X64036;XA600W2K8R2X64037;XA600W2K8R2X64038;XA600W2K8R2X64039;XA600W2K8R2X64040;XA600W2K8R2X64041;XA600W2K8R2X64042;XA600W2K8R2X64043;XA600W2K8R2X64044;XA600W2K8R2X64045;XA600W2K8R2X64046;XA600W2K8R2X64047;XA600W2K8R2X64048;XA600W2K8R2X64049;XA600W2K8R2X64050;XA600W2K8R2X64051;XA600W2K8R2X64052;XA600W2K8R2X64053;XA600W2K8R2X64054;XA600W2K8R2X64055;XA600W2K8R2X64056;XA600W2K8R2X64057;XA600W2K8R2X64058;XA600W2K8R2X64059;XA600W2K8R2X64060;XA600W2K8R2X64061;XA600W2K8R2X64062;XA600W2K8R2X64063;XA600W2K8R2X64064;XA600W2K8R2X64065;XA600W2K8R2X64066;XA600W2K8R2X64067;XA600W2K8R2X64068;XA600W2K8R2X64069;XA600W2K8R2X64070;XA600W2K8R2X64071;XA600W2K8R2X64072;XA600W2K8R2X64073;XA600W2K8R2X64074;XA600W2K8R2X64075;XA600W2K8R2X64076;XA600W2K8R2X64077;XA600W2K8R2X64078;XA600W2K8R2X64079;XA600W2K8R2X64080;XA600W2K8R2X64081;XA600W2K8R2X64082;XA600W2K8R2X64083;XA600W2K8R2X64084;XA600W2K8R2X64085;XA600W2K8R2X64086;XA600W2K8R2X64087;XA600W2K8R2X64088;XA600W2K8R2X64089;XA600W2K8R2X64090;XA600W2K8R2X64091;XA600W2K8R2X64092;XA600W2K8R2X64093;XA600W2K8R2X64094;XA600W2K8R2X64095;XA600W2K8R2X64096;XA600W2K8R2X64097;XA600W2K8R2X64098;XA600W2K8R2X64099;XA600W2K8R2X64100;XA600W2K8R2X64101;XA600W2K8R2X64102;XA600W2K8R2X64103;XA600W2K8R2X64104;XA600W2K8R2X64105;XA600W2K8R2X64106"
HotfixName="XA600W2K8R2X64R01" HotfixType="HRP" InstalledBy="{userName}" InstalledOn="04/23/2012 13:26:07" LanguageId="1033" MoreInformationAt="http://support.citrix.com/article/CTX130473" ServerName="{serverName}" TargetProduct="Citrix XenApp 6.0" Valid="True" FarmName="{farmName}" ScriptRunTime="129816576498909534"
""".format(
	time = eventTime,
	userName = "Administrator",
	serverName = server["ServerName"],
	farmName = server["FarmName"],
	host = server["ServerName"]
	)

	xa_serverhotfix_out.writelines(log_line)
	xa_serverhotfix_out.flush()
	
	writePerfMon(server["ServerName"], eventTime)


##############################################
#
#    Session
#
##############################################	
def writeSessionRecord(eventTime, farm):
	
	user = localUsers.getUser()
	server = xaServers.getXAServer()
	app = xaApps.getXAApp()
	client = clients.getCtxReceiverClient()
	username = user["loginid"][user["loginid"].find('\\')+1:]
	
	log_line = """***SPLUNK*** host={host} {time} - AccessSessionGuid="" AccountName="{accountName}" ApplicationState="NotApplicable" BrowserName="{browserName}" ClientAddress="{clientIP}" ClientBuffers="0 x 0" ClientBuildNumber="{clientBuildNumber}" ClientCacheDisk="0" ClientCacheLow="3145728" ClientCacheMinBitmapSize="0" ClientCacheSize="0" ClientCacheTiny="32768" ClientCacheXms="0" ClientDirectory="" ClientId="{clientId}" ClientIPV4="{clientIP}" ClientName="" ClientProductId="{clientProductId}" ClientType="WI" ClientVersion="{clientVersion}" ColorDepth="Colors32Bit" ConnectTime="{connectTime}" CurrentTime="{currentTime}" DirectXEnabled="True" DisconnectTime="{disconnectTime}" EncryptionLevel="Basic" FlashEnabled="True" HorizontalResolution="0" LastInputTime="{lastInputTime}" LogOnTime="{loginTime}" MachineName="{machineName}" Protocol="Ica" ServerBuffers="0 x 0" ServerName="{serverName}" SessionId="{sessionId}" SessionName="" SmartAccessFilters="" State="Active" UsbEnabled="False" VerticalResolution="0" VirtualIP="" WmpEnabled="True" UserName="{userName}" FarmName="{farmName}" SessionUID="{sessionUID}"
""".format(
	time = eventTime,
	accountName = username,
	browserName = app["BrowserName"],
	clientIP = user["ipaddress"],
	clientBuildNumber = client["ClientBuildNumber"],
	clientId = "",
	clientIPV4 = user["ipaddress"],
	clientProductId = client["ClientProductID"],
	clientVersion = client["ClientVersion"],
	connectTime = eventTime,
	currentTime = eventTime,
	disconnectTime = eventTime,
	lastInputTime = eventTime,
	loginTime = eventTime,
	machineName = server["ServerName"],
	serverName = server["ServerName"],
	sessionId = "",
	userName = username,
	farmName = farm["FarmName"],
	sessionUID = eventTime + ":" + username +":" + str(random.randint(0, 5000)),
	host = server["ServerName"]
	)
	
	xa_sessions_out.writelines(log_line)
	xa_sessions_out.flush()
	

	log_line = """***SPLUNK*** host={host} {time} - AccountDisplayName="{userName}" BasePriority="8" CreationTime="{creationTime}" CurrentPagedPoolQuota="552768" CurrentVirtualSize="0" CurrentWorkingSetSize="22052864" KernelTime="671"
MachineName="{machineName}" PageFaultCount="51565" PageFileUsage="56877056" ParentId="20416" PeakNonPagedPoolQuota="66564" PeakPagedPoolQuota="554560" PeakVirtualSize="0" PeakWorkingSetSize="41631744"
PercentCpuLoad="4.61" PrivatePageCount="0" ProcessId="6284" ProcessName="{processName}" ServerName="{serverName}" SessionId="{sessionId}" State="Unknown" UserTime="1311" FarmName="{farmName}" ScriptRunTime="129816576534019248"
""".format(
	time = eventTime,
	userName = username,
	creationTime = eventTime,
	machineName = server["ServerName"],
	processName = "mmc.exe",
	serverName = server["ServerName"],
	sessionId = "",
	farmName = farm["FarmName"],
	host = server["ServerName"]
	)

	xa_sessionprocess_out.writelines(log_line)	
	xa_sessionprocess_out.flush()
	
	
	InputSessionBandwidth = random.randint(160, 1000000)
	OutputSessionBandwidth = random.randint(150, 1000000)
	LatencySessionAverage = random.randint(100, 400)
	
	log_line = """***SPLUNK*** host={host} {time} - Caption="" Description="" Frequency_Object="" Frequency_PerfTime="" Frequency_Sys100NS="" InputAudioBandwidth="0" InputClipboardBandwidt="0" InputCOM1Bandwidth="0" InputCOM2Bandwidth="0"
InputCOMBandwidth="0" InputControlChannelBandwidth="0" InputDriveBandwidth="0" InputFontDataBandwidth="0" InputHDXMediaStreamforFlashDataBandwidth="0" InputHDXMediaStreamforFlashv2DataBandwidth="0"
InputLicensingBandwidth="0" InputLPT1Bandwidth="0" InputLPT2Bandwidth="0" InputPNBandwidth="0" InputPrinterBandwidth="0" InputSeamlessBandwidth="0" InputSessionBandwidth="{inputSessionBandwidth}"
InputSessionCompression="35" InputSessionLineSpeed="0" InputSpeedScreenDataChannelBandwidth="0" InputTextEchoBandwidth="0" InputThinWireBandwidth="0" InputTWAINBandwidth="0" LatencyLastRecorded="76"
LatencySessionAverage="{latencySessionAvg}" LatencySessionDeviation="49" Name="{name}" UserName="{userName}" OutputAudioBandwidth="0" OutputClipboardBandwidth="0" OutputCOM1Bandwidth="0" OutputCOM2Bandwidth="0"
OutputCOMBandwidth="0" OutputControlChannelBandwidth="0" OutputDriveBandwidth="0" OutputFontDataBandwidth="0" OutputHDXMediaStreamforFlashDataBandwidth="0" OutputHDXMediaStreamforFlashv2DataBandwidth="0"
OutputLicensingBandwidth="0" OutputLPT1Bandwidth="0" OutputLPT2Bandwidth="0" OutputPNBandwidth="0" OutputPrinterBandwidth="0" OutputSeamlessBandwidth="0" OutputSessionBandwidth="{outputSessionBandwidth}"
OutputSessionCompression="19" OutputSessionLineSpeed="1006744" OutputSpeedScreenDataChannelBandwidth="0" OutputTextEchoBandwidth="0" OutputThinWireBandwidth="0" OutputTWAINBandwidth="0" ResourceShares="0"
Timestamp_Object="" Timestamp_PerfTime="" Timestamp_Sys100NS="" __CLASS="Win32_PerfFormattedData_CitrixICA_ICASession" __DERIVATION="Win32_PerfFormattedData;Win32_Perf;CIM_StatisticalInformation"
__DYNASTY="CIM_StatisticalInformation" __GENUS="2" __NAMESPACE="root\cimv2" __PATH="\\server\root\cimv2:Win32_PerfFormattedData_CitrixICA_ICASession.Name="{name}"
__PROPERTY_COUNT="59" __RELPATH="Win32_PerfFormattedData_CitrixICA_ICASession.Name="{name}" __SERVER="{serverName}"
__SUPERCLASS="Win32_PerfFormattedData" ScriptRunTime="129816577108411248""".format(
	time = eventTime,
	inputSessionBandwidth = InputSessionBandwidth,
	latencySessionAvg = LatencySessionAverage,
	name = "ICA-TCP (" + username + ")",
	userName = username,
	outputSessionBandwidth = OutputSessionBandwidth,
	serverName = server["ServerName"],
	host = server["ServerName"]
	)

	xa_icasession_out.writelines(log_line)
	xa_icasession_out.flush()


##############################################
#
#    Application
#
##############################################		
def writeApplication(eventTime, farm):
	
	server = xaServers.getXAServer()
	app = xaApps.getXAApp()
	
	log_line = """***SPLUNK*** host={host} {time} - AccessSessionConditions="" AccessSessionConditionsEnabled="False" AddToClientDesktop="False" AddToClientStartMenu="False" AlternateProfiles="" AnonymousConnectionsAllowed="False"
ApplicationId="{applicationId}" ApplicationType="ServerInstalled" AudioRequired="False" AudioType="Basic" BrowserName="{browserName}" CachingOption="" ClientFolder="" ColorDepth="Colors32Bit"
CommandLineExecutable="{commandLineExecutable}" ConnectionsThroughAccessGatewayAllowed="True" ContentAddress="" CpuPriorityLevel="Normal" Description="" DisplayName="{displayName}" Enabled="True"
EncryptionLevel="Basic" EncryptionRequired="False" FolderPath="Applications" HideWhenDisabled="False" InstanceLimit="-1" LoadBalancingApplicationCheckEnabled="True" MachineName="{machineName}"
MaximizedOnStartup="False" MultipleInstancesPerUserAllowed="True" OfflineAccessAllowed="" OtherConnectionsAllowed="True" PreLaunch="False" ProfileLocation="" ProfileProgramArguments="" ProfileProgramName=""
RunAsLeastPrivilegedUser="" SequenceNumber="1333750185" SslConnectionEnabled="False" StartMenuFolder="" TitleBarHidden="False" WaitOnPrinterCreation="False" WindowType="1024x768" WorkingDirectory=""
FarmName="{farmName}" ScriptRunTime="129816577106071248"
""".format(
	time = eventTime,
	applicationId = app["ApplicationId"],
	browserName = app["BrowserName"],
	commandLineExecutable = app["CommandLineExecutable"],
	displayName = app["DisplayName"],
	machineName = server["ServerName"],
	farmName = farm["FarmName"],
	host = server["ServerName"]
	)

	xa_application_out.writelines(log_line)
	xa_application_out.flush()
	

##############################################
#
#    Performance
#
##############################################	
def writePerfMon(ServerName, dateTime):
    #EventTime = dateTime.strftime("%m/%d/%Y %H:%M:%S.%f %z")

    # CPULoad
    cpu = random.uniform(30,80)
    print """
***SPLUNK*** host={host} source=PerfmonMk:CPULoad sourcetype=PerfmonMk:CPULoad
{time} 
collection=CPULoad
category=CPULoad
object=Processor
instance\t%_Processor_Time
_Total\t{processor}\t

""".format(
        host = ServerName,
        time = dateTime,
        processor = cpu,
	)

    # AvailableMemory
    print """
***SPLUNK*** host={host} source=PerfmonMk:AvailableMemory sourcetype=PerfmonMk:AvailableMemory
{time}
collection=AvailableMemory
category=AvailableMemory
object=Memory
instance\tAvailable_Bytes
0\t{available}\t

""".format(
    host = ServerName,
    time = dateTime,
    available = random.randint(268435456, 1610612736),
	)

    # PhysicalDisk
    # LogicalDisk
    reads = random.uniform(0.005,0.13)
    reads = random.choice([0,reads])
    writes = random.gauss(0.549401, 0.521513)
    ios = random.uniform(0.11,0.71)

    print """
***SPLUNK*** host={host} source=PerfmonMk:LogicalDisk sourcetype=PerfmonMk:LogicalDisk
{time}
collection=LogicalDisk
category=LogicalDisk
object=LogicalDisk
instance\tFree_Megabytes\t%_Free_Space\tSplit_IO/Sec\tDisk_Reads/Sec\tDisk_Writes/Sec\tDisk_Transfers/Sec\tDisk_Bytes/Sec\t%_Disk_Time
_Total\t{freeMb}\t{freePc}\t{splitIO}\t{diskReads}\t{diskWrites}\t{diskXfer}\t{diskBytes}\t{diskTime}\t

""".format(
        host = ServerName,
        time = dateTime,
        freeMb = random.randint(5120, 10240),
        freePc = random.uniform(0.50, 0.99),
        diskTime = random.gauss(0.211,0.44),
        splitIO = random.choice([0,0,ios]),
        diskReads = reads,
        diskWrites = writes,
        diskXfer = reads + writes,
        diskBytes = random.choice([0,random.uniform(2000,80000)])
    )

    # NetworkInterface
    print """
***SPLUNK*** host={host} source=PerfmonMk:NetworkInterface sourcetype=PerfmonMK:NetworkInterface
{time}
collection=NetworkInterface category=NetworkInterface object=Network_Interface
instance\tBytes_Received/sec\tBytes_Sent/sec
Intel[R] PRO_1000 MT Network Connection\t{received}\t{sent}

""".format(
        host = ServerName,
        time = dateTime,
        received = random.randint(20480, 204800),
        sent = random.randint(20480, 204800))


    # RunningProcesses
    PROCS = {
        "CdfSvc"                : (2,  5120880,  1, 3, 2, 1255),
        "CitrixCGPServer"       : (2,  21662345, 1, 1, 2, 1235),
        "CtxAudioService"       : (6,  65755483, 2, 4, 4, 4256),
        "CtxSvcHost"            : (4,  5120550,  1, 1, 2, 3529),
        "FlashUtil11e_ActiveX"  : (19, 456423,  1, 1, 2, 3321),
        "LogonUI"               : (.01, 125534, 4, 4, 2, 3601),
        "PicaSessionMgr"        : (2,  34567,   8, 8, 2, 5305),
        "PvsVmAgent"            : (2,  5125500, 1, 1, 2, 2368),
        "WmiPrvSE"              : (2,  51200,   1, 1, 2, 1922),
        "WorkstationAgent"      : (2,  51200,   1, 1, 2, 5903),
        "ccsvchst"              : (20, 102400,  1, 3, 7, 4988),
        "explorer"              : (3,  637495,  1, 2, 1, 1893),
        "iexplore"              : (19, 51200,  10, 10, 20, 1204),
        "jusched"               : (9,  6455759, 4, 5, 4, 2395)
    }

    print """
***SPLUNK*** host={host} source=PerfmonMk:RunningProcesses sourcetype=PerfmonMK:RunningProcesses
{time}
collection=RunningProcesses
category=RunningProcesses
object=Process
instance\t%_Processor_Time\tVirtual_Bytes\tIO_Write_Operations/sec\tIO_Read_Operations/sec\tID_Process\tPage_Faults/Sec\tElapsed_Time""".format( host = ServerName, time = dateTime)

    for P in PROCS:
        print "{process}\t{percent}\t{virtual}\t{writes}\t{reads}\t{id}\t{faults}\t{elapsed}".format(
            host = ServerName,
            time = dateTime,
            process = P,
            percent = PROCS[P][0],
            virtual = PROCS[P][1],
            reads = PROCS[P][2],
            writes = PROCS[P][3],
            faults = random.choice([0,0,0,0,random.uniform(0.01,120.0)]),
            id = PROCS[P][4],
            elapsed = random.uniform(0.500000, 1500000.000000)
        )

    print ""
    
def writeAlert(eventTime):
	
	server = xaServers.getXAServer()
	alert = xaAlerts.getXAAlert()
	user = localUsers.getUser()
	username = user["loginid"][user["loginid"].find('\\')+1:]
	
	log_line = """***SPLUNK*** host={host} source="{source}" sourcetype="stash" {time} search_name="{searchName}", search_now=1352963400.000, info_min_time=1352959200.000, info_max_time=1352963400.000, info_search_time=1352963410.347, LogOnTime="{logonTime}", ServerName="{serverName}", UserName={userName}, Value={value}, alert_name="{alertName}", usrexp={usrExp}

""".format(
	host = server["ServerName"],
	source = alert["source"],
	time = eventTime,
	searchName = alert["source"],
	logonTime = eventTime,
	serverName = server["ServerName"],
	userName = username,
	value = alert["Value"],
	alertName = alert["alert_name"],
	usrExp = alert["usrexp"]
	)

	xa_alerts_out.writelines(log_line)
	xa_alerts_out.flush()
	

def generateData(farm):
	
	START_TIME = datetime.datetime.now() + datetime.timedelta(days=_START)
	END_TIME = datetime.datetime.now() + datetime.timedelta(days=_END)
	
	EventTime = START_TIME
	
	while EventTime < END_TIME:
		
		strEventTime = EventTime.strftime('%x %X')
		
		writeFarmRecord(strEventTime, farm)

		for svr in range(int(farm["ServerCount"])):
			writeServerRecord(strEventTime, farm)
			
		for i in range(int(farm["SessionCount"])):
			writeSessionRecord(strEventTime, farm)

		for app in range(int(farm["AppCount"])):
			writeApplication(strEventTime, farm)
		
		writeAlert(strEventTime)
		
		EventTime = EventTime + datetime.timedelta(minutes=15)
		
if __name__ == "__main__":
	
	### Adjusting sys.path to include BD-Datagen
	libDir = os.path.join(os.environ["SPLUNK_HOME"], 'etc', 'apps', 'BD-Datagen', 'bin')
	sys.path.insert(1, libDir)
	
	### Importing BD-Datagen Modules
	from datagen.localusers import LocalUsers
	from datagen.logGenerator import LogStore
	from datagen.windowsprocesses import WindowsProcesses
	from xaservers import XAServers
	from xafarms import XAFarms
	from xaapps import XAApps
	from ctxReceiverClients import CtxReceiverClients
	from xaalerts import XAAlerts

	localUsers = LocalUsers()

	xaFarms = XAFarms()
	clients = CtxReceiverClients()
	xaAlerts = XAAlerts()
	
	farm = xaFarms.getXAFarm(0)
	xaServers = XAServers(farm["FarmName"])
	xaApps = XAApps()
	
	generateData(farm)
	
	#farm = xaFarms.getXAFarm(1)
	#generateData(farm)