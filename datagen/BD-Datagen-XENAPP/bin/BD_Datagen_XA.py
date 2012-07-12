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
#	_Sessions is the number of unique user sessions per day. 
#

# # # # # # # # # # # # # # # # # ## # # ## # # #

_START = -2
_END = 2
_SESSIONS = 25
_SERVERS = 10
_APPLICATIONS = 15

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

def logger(string):
	BD_DATAGEN_LOG.write(time.asctime() + ' - ' + string + "\n")
	BD_DATAGEN_LOG.flush()
#	print time.asctime() + ' - ' + string
	return 0

def writeServerRecord(EventTime, ServerName, ServerIP, SessionCount, FarmName):
	log_line =  '\n' + EventTime + ' - CitrixEdition="Platinum" CitrixEditionString="PLT" CitrixInstallDate="02/10/2012 06:41:00" \
	CitrixInstallPath="C:\Program Files (x86)\Citrix\" \
	CitrixProductName="Citrix Presentation Server" CitrixServicePack="0" CitrixVersion="6.5.6682" ElectionPreference="MostPreferred" \
	FolderPath="Servers" IcaPortNumber="1494" IPAddresses="' + ServerIP + '" Is64Bit="True" IsSpoolerHealthy="True" \
	LicenseServerName="lic-01.domain.com" LicenseServerPortNumber="27000" LogOnMode="AllowLogOns" LogOnsEnabled="True" \
	MachineName="' + ServerName + '" OSServicePack="Service Pack 1" OSVersion="6.1.7601" PcmMode="Normal" RdpPortNumber="3389" \
	ServerFqdn="' + ServerName + '.domain.com" ServerId="0673-000C-000000BE" ServerName="' + ServerName + '" \
	SessionCount="' + SessionCount + '" ZoneName="SFO-1" FarmName="' + FarmName + '" ScriptRunTime="' + str(EventTime) + '"'
	
	xa_server_out.writelines(log_line)
	xa_server_out.flush()
	
def writeFarmRecord(eventTime, farm):
	log_line = '\n' + eventTime + ' - FarmName="' + farm["FarmName"] + '" SessionCount="' + str(_SESSIONS) + '" \
	"Users="' + str(_SESSIONS) + '" \
	Servers="' + str(_SERVERS) + '" Applications="' + farm["AppCount"] + '"'
	
	xa_farm_out.writelines(log_line)
	xa_farm_out.flush()
	
def writeServerHotfix(EventTime, Username, ServerName, FarmName):
	log_line = '\n' + EventTime + ' - HotfixesReplaced="XA600W2K8R2X64001;XA600W2K8R2X64002;XA600W2K8R2X64003;XA600W2K8R2X64004;XA600W2K8R2X64005;XA600W2K8R2X64006;XA600W2K8R2X64007;XA600W2K8R2X64008;XA600W2K8R2X64009;XA600W2K8R2X64010;XA600W2K8R2X64011;XA600W2K8R2X64012;XA600W2K8R2X64013;XA600W2K8R2X64014;XA600W2K8R2X64015;XA600W2K8R2X64016;XA600W2K8R2X64017;XA600W2K8R2X64018;XA600W2K8R2X64019;XA600W2K8R2X64020;XA600W2K8R2X64021;XA600W2K8R2X64022;XA600W2K8R2X64023;XA600W2K8R2X64024;XA600W2K8R2X64025;XA600W2K8R2X64026;XA600W2K8R2X64027;XA600W2K8R2X64028;XA600W2K8R2X64029;XA600W2K8R2X64030;XA600W2K8R2X64031;XA600W2K8R2X64032;XA600W2K8R2X64033;XA600W2K8R2X64034;XA600W2K8R2X64035;XA600W2K8R2X64036;XA600W2K8R2X64037;XA600W2K8R2X64038;XA600W2K8R2X64039;XA600W2K8R2X64040;XA600W2K8R2X64041;XA600W2K8R2X64042;XA600W2K8R2X64043;XA600W2K8R2X64044;XA600W2K8R2X64045;XA600W2K8R2X64046;XA600W2K8R2X64047;XA600W2K8R2X64048;XA600W2K8R2X64049;XA600W2K8R2X64050;XA600W2K8R2X64051;XA600W2K8R2X64052;XA600W2K8R2X64053;XA600W2K8R2X64054;XA600W2K8R2X64055;XA600W2K8R2X64056;XA600W2K8R2X64057;XA600W2K8R2X64058;XA600W2K8R2X64059;XA600W2K8R2X64060;XA600W2K8R2X64061;XA600W2K8R2X64062;XA600W2K8R2X64063;XA600W2K8R2X64064;XA600W2K8R2X64065;XA600W2K8R2X64066;XA600W2K8R2X64067;XA600W2K8R2X64068;XA600W2K8R2X64069;XA600W2K8R2X64070;XA600W2K8R2X64071;XA600W2K8R2X64072;XA600W2K8R2X64073;XA600W2K8R2X64074;XA600W2K8R2X64075;XA600W2K8R2X64076;XA600W2K8R2X64077;XA600W2K8R2X64078;XA600W2K8R2X64079;XA600W2K8R2X64080;XA600W2K8R2X64081;XA600W2K8R2X64082;XA600W2K8R2X64083;XA600W2K8R2X64084;XA600W2K8R2X64085;XA600W2K8R2X64086;XA600W2K8R2X64087;XA600W2K8R2X64088;XA600W2K8R2X64089;XA600W2K8R2X64090;XA600W2K8R2X64091;XA600W2K8R2X64092;XA600W2K8R2X64093;XA600W2K8R2X64094;XA600W2K8R2X64095;XA600W2K8R2X64096;XA600W2K8R2X64097;XA600W2K8R2X64098;XA600W2K8R2X64099;XA600W2K8R2X64100;XA600W2K8R2X64101;XA600W2K8R2X64102;XA600W2K8R2X64103;XA600W2K8R2X64104;XA600W2K8R2X64105;XA600W2K8R2X64106" \
	HotfixName="XA600W2K8R2X64R01" HotfixType="HRP" InstalledBy="' + Username + '" InstalledOn="04/23/2012 13:26:07" \
	LanguageId="1033" MoreInformationAt="http://support.citrix.com/article/CTX130473" ServerName="' + ServerName + '" \
	TargetProduct="Citrix XenApp 6.0" Valid="True" FarmName="' + FarmName + '" ScriptRunTime="129816576498909534"'
	
	xa_serverhotfix_out.writelines(log_line)
	xa_serverhotfix_out.flush()

def writeSessionProcess(EventTime, Username, ServerName, SessionID, FarmName):
	log_line = '\n' + EventTime + ' - AccountDisplayName="' + Username + '" BasePriority="8" CreationTime="' + EventTime + '" CurrentPagedPoolQuota="552768" \
	CurrentVirtualSize="0" CurrentWorkingSetSize="22052864" KernelTime="671" \
	MachineName="' + ServerName + '" PageFaultCount="51565" PageFileUsage="56877056" ParentId="20416" PeakNonPagedPoolQuota="66564" \
	PeakPagedPoolQuota="554560" PeakVirtualSize="0" PeakWorkingSetSize="41631744" PercentCpuLoad="4.61" \
	PrivatePageCount="0" ProcessId="6284" ProcessName="mmc.exe" ServerName="' + ServerName + '" SessionId="' + SessionID + '" State="Unknown" \
	UserTime="1311" FarmName="' + FarmName + '" ScriptRunTime="129816576534019248"'
	
	xa_sessionprocess_out.writelines(log_line)	
	xa_sessionprocess_out.flush()
	
def writeSession(EventTime, Username, Appname, ClientIP, client, Servername, SessionID, FarmName):
	log_line = '\n' + EventTime + ' - AccessSessionGuid="" AccountName="' + Username + '" ApplicationState="NotApplicable" \
	BrowserName="' + Appname + '" ClientAddress="' + ClientIP + '" ClientBuffers="0 x 0" ClientBuildNumber="' + client["ClientVersion"] + '" \
	ClientCacheDisk="0" ClientCacheLow="3145728" ClientCacheMinBitmapSize="0" ClientCacheSize="0" ClientCacheTiny="32768" \
	ClientCacheXms="0" ClientDirectory="" ClientId="' + client["ClientVersion"] + '" ClientIPV4="' + ClientIP + '" ClientName="" \
	ClientProductId="' + client["ClientProductID"] + '" ClientType="WI" ClientVersion="' + client["ClientVersion"] + '" ColorDepth="Colors32Bit" \
	ConnectTime="04/26/2012 14:08:27" CurrentTime="05/16/2012 09:00:53" DirectXEnabled="True" DisconnectTime="04/26/2012 15:17:41" \
	EncryptionLevel="Basic" FlashEnabled="True" HorizontalResolution="0" LastInputTime="04/26/2012 15:17:41" \
	LogOnTime="' + EventTime + '" MachineName="' + Servername + '" Protocol="Ica" ServerBuffers="0 x 0" \
	ServerName="' + Servername + '" SessionId="' + SessionID + '" SessionName="" SmartAccessFilters="" State="Active" \
	UsbEnabled="False" VerticalResolution="0" VirtualIP="" WmpEnabled="True" UserName="' + Username + '" FarmName="' + FarmName + '" \
	SessionUID="' + EventTime + ':' + SessionID + ':' + Servername + '"'

	xa_sessions_out.writelines(log_line)
	xa_sessions_out.flush()
	
	
def writeServerLoad(EventTime, ServerLoad, ServerName, FarmName):
	log_line = '\n' + EventTime + ' - Load="' + ServerLoad + '" MachineName="' + ServerName + '" ServerName="' + ServerName + '" FarmName="' + FarmName + '" ScriptRunTime="129816577132435248"'
	
	xa_serverload_out.writelines(log_line)
	xa_serverload_out.flush()
	
	
def writeICASesion(EventTime, SessionID, Username, ServerName):
	
	InputSessionBandwidth = random.randint(160, 1000000)
	OutputSessionBandwidth = random.randint(150, 1000000)
	LatencySessionAverage = random.randint(100, 400)
	
	log_line = '\n' + EventTime + ' - Caption="" Description="" Frequency_Object="" Frequency_PerfTime="" Frequency_Sys100NS="" \
	InputAudioBandwidth="0" InputClipboardBandwidt="0" InputCOM1Bandwidth="0" InputCOM2Bandwidth="0" InputCOMBandwidth="0" \
	InputControlChannelBandwidth="0" InputDriveBandwidth="0" InputFontDataBandwidth="0" InputHDXMediaStreamforFlashDataBandwidth="0" \
	InputHDXMediaStreamforFlashv2DataBandwidth="0" InputLicensingBandwidth="0" InputLPT1Bandwidth="0" InputLPT2Bandwidth="0" \
	InputPNBandwidth="0" InputPrinterBandwidth="0" InputSeamlessBandwidth="0" InputSessionBandwidth="' + str(InputSessionBandwidth) + '" InputSessionCompression="35" \
	InputSessionLineSpeed="0" InputSpeedScreenDataChannelBandwidth="0" InputTextEchoBandwidth="0" InputThinWireBandwidth="0" \
	InputTWAINBandwidth="0" LatencyLastRecorded="76" LatencySessionAverage="' + str(LatencySessionAverage) + '" \
	LatencySessionDeviation="49" Name="ICA-TCP ' + SessionID + ' (' + Username + ')" UserName="' + Username + '" OutputAudioBandwidth="0" OutputClipboardBandwidth="0" \
	OutputCOM1Bandwidth="0" OutputCOM2Bandwidth="0" OutputCOMBandwidth="0" OutputControlChannelBandwidth="0" OutputDriveBandwidth="0" \
	OutputFontDataBandwidth="0" OutputHDXMediaStreamforFlashDataBandwidth="0" OutputHDXMediaStreamforFlashv2DataBandwidth="0" \
	OutputLicensingBandwidth="0" OutputLPT1Bandwidth="0" OutputLPT2Bandwidth="0" OutputPNBandwidth="0" OutputPrinterBandwidth="0" \
	OutputSeamlessBandwidth="0" OutputSessionBandwidth="' + str(OutputSessionBandwidth) + '" OutputSessionCompression="19" OutputSessionLineSpeed="1006744" \
	OutputSpeedScreenDataChannelBandwidth="0" OutputTextEchoBandwidth="0" OutputThinWireBandwidth="0" OutputTWAINBandwidth="0" \
	ResourceShares="0" Timestamp_Object="" Timestamp_PerfTime="" Timestamp_Sys100NS="" __CLASS="Win32_PerfFormattedData_CitrixICA_ICASession" \
	__DERIVATION="Win32_PerfFormattedData;Win32_Perf;CIM_StatisticalInformation" __DYNASTY="CIM_StatisticalInformation" __GENUS="2" \
	__NAMESPACE="root\cimv2" __PATH="\\BD-XA65-01\root\cimv2:Win32_PerfFormattedData_CitrixICA_ICASession.Name="ICA-TCP ' + SessionID + ' (' + Username + ')"" \
	__PROPERTY_COUNT="59" __RELPATH="Win32_PerfFormattedData_CitrixICA_ICASession.Name="ICA-TCP ' + SessionID + ' (' + Username + ')"" __SERVER="' + ServerName + '" \
	__SUPERCLASS="Win32_PerfFormattedData" ScriptRunTime="129816577108411248"'
	
	xa_icasession_out.writelines(log_line)
	xa_icasession_out.flush()
	
def writeApplication(EventTime, AppName, ServerName, FarmName):
	log_line='\n' + EventTime + ' - AccessSessionConditions="" AccessSessionConditionsEnabled="False" AddToClientDesktop="False" \
	AddToClientStartMenu="False" AlternateProfiles="" AnonymousConnectionsAllowed="False" ApplicationId="0673-0006-000001f4" \
	ApplicationType="ServerInstalled" AudioRequired="False" AudioType="Basic" BrowserName="' + AppName + '" CachingOption="" \
	ClientFolder="" ColorDepth="Colors32Bit" CommandLineExecutable="%windir%\system32\mmc.exe "%ProgramFiles%\Hyper-V\virtmgmt.msc"" \
	ConnectionsThroughAccessGatewayAllowed="True" ContentAddress="" CpuPriorityLevel="Normal" Description="" \
	DisplayName="' + AppName + '" Enabled="True" EncryptionLevel="Basic" EncryptionRequired="False" FolderPath="Applications" \
	HideWhenDisabled="False" InstanceLimit="-1" LoadBalancingApplicationCheckEnabled="True" MachineName="' + ServerName + '" \
	MaximizedOnStartup="False" MultipleInstancesPerUserAllowed="True" OfflineAccessAllowed="" OtherConnectionsAllowed="True" \
	PreLaunch="False" ProfileLocation="" ProfileProgramArguments="" ProfileProgramName="" RunAsLeastPrivilegedUser="" \
	SequenceNumber="1333750185" SslConnectionEnabled="False" StartMenuFolder="" TitleBarHidden="False" WaitOnPrinterCreation="False" \
	WindowType="1024x768" WorkingDirectory="" FarmName="' + FarmName + '" ScriptRunTime="129816577106071248"'
	
	xa_application_out.writelines(log_line)
	xa_application_out.flush()
	

def writeDesktopRecord(Desktop,EventTime):
	log_line = ""
	for key in Desktop:
		log_line = log_line + ' ' + key + '="'+Desktop[key]+'" '
	evt = EventTime + " - " + log_line + "\n"
	xd_desktops_out.writelines("")
	xd_desktops_out.writelines(evt)
	xd_desktops_out.writelines("")
	xd_desktops_out.flush()
#	print evt

def writeVDISession(XD_SESSION):
	log_line = ""
	for key in XD_SESSION:
		log_line = log_line + ' ' + key + '="'+XD_SESSION[key]+'" '
	evt = XD_SESSION["EventTime"] + " - " + log_line + "\n"
	xd_sessions_out.writelines("")
	xd_sessions_out.writelines(evt)
	xd_sessions_out.writelines("")
	xd_sessions_out.flush()
#	print evt


def getXDSession(VDI_SESSION):
	xd_session = {}
	xd_session["DesktopName"] = VDI_SESSION["DESKTOP"]["MachineName"]
	xd_session["SessionStateChangeTime"] = time.strftime('%x %X')
	xd_session["BrokeringTime"] = time.strftime('%x %X')
	xd_session["StartTime"] = time.strftime('%x %X')
	
#Desktop Info
	xd_session["DesktopSID"] = VDI_SESSION["DESKTOP"]["SID"]
	xd_session["DesktopUid"] = VDI_SESSION["DESKTOP"]["Uid"]
	xd_session["LaunchedViaHostName"] ="bd-xd5.ad.splunk.com"
	xd_session["LaunchedViaIP"] ="10.1.232.20"
	
#User Info
#Connected is where you came from
#Launched is the Web interface machine
	xd_session["ConnectedViaHostName"] = " "
	xd_session["ConnectedViaIP"] = VDI_SESSION["USER"]["ipaddress"]
	xd_session["BrokeringUserName"] = VDI_SESSION["USER"]["loginid"]
	xd_session["BrokeringUserSID"] = VDI_SESSION["USER"]["SID"]
	xd_session["Uid"] = "15"
	xd_session["UserName"] = VDI_SESSION["USER"]["loginid"]
	xd_session["UserSID"] = VDI_SESSION["USER"]["SID"]
	xd_session["ClientAddress"] = VDI_SESSION["USER"]["ipaddress"]

#Client Info
	xd_session["ClientName"] = VDI_SESSION["CLIENT"]["ClientName"]
	xd_session["ClientVersion"] = VDI_SESSION["CLIENT"]["ClientVersion"]
	xd_session["DeviceId"] = VDI_SESSION["CLIENT"]["DeviceId"]
	xd_session["HardwareId"] = VDI_SESSION["CLIENT"]["HardwareId"]

#Random Stuff
	xd_session["SessionUID"]  = str(xd_session["StartTime"]) + ":"+str(xd_session["UserSID"]) + ":"+str(xd_session["DesktopSID"])
	xd_session["AutonomouslyBrokered"] = "False"
	xd_session["AutonomouslyBrokered"] = "False" 
	xd_session["Protocol"] ="HDX"
	xd_session["SecureIcaActive"] ="False"
	xd_session["SessionId"] ="0"
	xd_session["SessionState"] ="Active"
	xd_session["SmartAccessTags"] =""
	return xd_session

def writePerfMon(ServerName, EventTime):
	host = ServerName
	perf_ts = EventTime
	
	
	print "***SPLUNK*** host="+host+" source=Perfmon:CPULoad sourcetype=Perfmon:CPULoad "
	print perf_ts
	CPU = random.randint(30,80)
	print 'collection=CPULoad' 
	print 'object=Processor'
	print 'counter="% Processor Time'
	print 'instance=Idle'
	print 'Value='+str(CPU)
	print ""

	print "***SPLUNK*** host="+host+" source=Perfmon:AvailableMemory sourcetype=Perfmon:AvailableMemory "
	print perf_ts
	MEM = random.randint(268435456,1610612736)
	print 'collection=AvailableMemory' 
	print 'object=Memory'
	print 'counter="Available Bytes'
	print 'Value='+str(MEM)
	print ""

	print "***SPLUNK*** host="+host+" source=Perfmon:FreeDiskSpace sourcetype=Perfmon:FreeDiskSpace "
	print perf_ts
	FREE = random.randint(5120,10240)
	print 'collection=FreeDiskSpace' 
	print 'object=LogicalDisk'
	print 'counter="Free Megabytes'
	print 'instance=_Total'
	print 'Value='+str(FREE)
	print ""
	print perf_ts
	FREEPERC = random.randint(50,99)
	print 'collection=FreeDiskSpace' 
	print 'object=LogicalDisk'
	print 'counter="% Free Space'
	print 'instance=_Total'
	print 'Value='+str(FREEPERC)
	print ""

	print "***SPLUNK*** host="+host+" source=Perfmon:NetworkInterface sourcetype=Perfmon:NetworkInterface "
	IN = random.randint(20480,204800)
	print perf_ts
	print 'collection=NetworkInterface' 
	print 'object=Network Interface'
	print 'counter="Bytes Sent/sec'
	print 'instance=Intel[R] PRO_1000 MT Network Connection'
	print 'Value='+str(IN)
	print ""

	OUT = random.randint(20480,204800)
	print perf_ts
	print 'collection=NetworkInterface' 
	print 'object=Network Interface'
	print 'counter=Bytes Received/sec'
	print 'instance=Intel[R] PRO_1000 MT Network Connection'
	print 'Value='+str(OUT)
	print ""
	
	XFER = random.randint(1,50)
	print "***SPLUNK*** host="+host+" source=Perfmon:perfmon:LogicalDisk sourcetype=Perfmon:LogicalDisk "	
	print perf_ts
	print 'collection=LogicalDisk'
	print 'object=LogicalDisk'
	print 'counter="Disk Transfers/Sec"'
	print 'instance=_Total'
	print 'Value='+str(XFER)
	
	
	PROCS = {
			"CdfSvc":(2,5120880,1,3,2,5,2),"CitrixCGPServer":(2,21662345,1,1,2),"CtxAudioService":(6,65755483,2,4,4),"CtxSvcHost":(4,5120550,1,1,2),"FlashUtil11e_ActiveX":(19,456423,1,1,2),"LogonUI":(.01,125534,4,4,2),"PicaSessionMgr":(2,34567,8,8,2),"PvsVmAgent":(2,5125500,1,1,2),"WmiPrvSE":(2,51200,1,1,2),"WorkstationAgent":(2,51200,1,1,2),"ccsvchst":(20,102400,1,3,7),"explorer":(3,637495,1,2,1),"iexplore":(19,51200,10,10,20),"jusched":(9,6455759,4,5,4)
		}
		
	

	for P in PROCS:
		CPU = PROCS[P][0]
		MEM = PROCS[P][1]
		READ = PROCS[P][2]
		WRITE = PROCS[P][3]
		print "***SPLUNK*** host="+host+" source=Perfmon:RunningProcesses sourcetype=Perfmon:RunningProcesses "
		print perf_ts
		print 'collection=RunningProcesses' 
		print 'object=Process'
		print 'counter=Virtual Bytes'
		print 'instance='+P
		print 'Value='+str(MEM)
		print ""
		print ""
		print "***SPLUNK*** host="+host+" source=Perfmon:RunningProcesses sourcetype=Perfmon:RunningProcesses "
		print perf_ts
		print 'collection=RunningProcesses' 
		print 'object=Process'
		print 'counter=% Processor Time'
		print 'instance='+P
		print 'Value='+str(CPU)
		print ""
		print ""
		print "***SPLUNK*** host="+host+" source=Perfmon:RunningProcesses sourcetype=Perfmon:RunningProcesses "
		print perf_ts
		print 'collection=RunningProcesses' 
		print 'object=Process'
		print 'counter="IO Read Operations/sec"'
		print 'instance='+P
		print 'Value='+str(READ)
		print ""
		print ""
		print "***SPLUNK*** host="+host+" source=Perfmon:RunningProcesses sourcetype=Perfmon:RunningProcesses "
		print perf_ts
		print 'collection=RunningProcesses' 
		print 'object=Process'
		print 'counter="IO Write Operations/sec"'
		print 'instance='+P
		print 'Value='+str(WRITE)
		print ""
		print ""		


def writeInventory(Desktop, EventTime):
		perf_ts = EventTime
		host = Desktop["MachineName"][Desktop["MachineName"].find('\\')+1:]
		print "***SPLUNK*** host="+host+" source=WMI:Win32BIOS sourcetype=WMI:Win32BIOS index=xendesktop_winevents"
		print str(perf_ts) + 'BIOSVersion="<unknown variant result type 8200>",BiosCharacteristics="<unknown variant result type 8195>",BuildNumber="NULL",Caption="BIOS Date: 04/18/11 15:42:51  Ver: 09.00.05",CodeSet="NULL",CurrentLanguage="enUS",Description="BIOS Date: 04/18/11 15:42:51  Ver: 09.00.05",IdentificationCode="NULL",InstallDate="NULL",InstallableLanguages="1",LanguageEdition="NULL",ListOfLanguages="<unknown variant result type 8200>",Manufacturer="American Megatrends Inc.",Name="BIOS Date: 04/18/11 15:42:51  Ver: 09.00.05",OtherTargetOS="NULL",PrimaryBIOS="True",ReleaseDate="20110418000000.000000+000",SMBIOSBIOSVersion="090005 ",SMBIOSMajorVersion="2",SMBIOSMinorVersion="3",SMBIOSPresent="True",SerialNumber="8673-6295-2060-8920-1337-4426-46",SoftwareElementID="BIOS Date: 04/18/11 15:42:51  Ver: 09.00.05",SoftwareElementState="3",Status="OK",TargetOperatingSystem="0",Version="VRTUAL - 4001118",wmi_type="Win32BIOS	'
		print ""
		print ""		
		print "***SPLUNK*** host="+host+" source=Windows:PowerShell  sourcetype=WMI:InstalledSoftware index=xendesktop_winevents"		
		print ' Vendor="Citrix Systems, Inc"	Name="PVS PowerShell SDK x64" Version="1.01"'
		print ' Vendor="Citrix Systems, Inc."	Name="Citrix AD Identity Service" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" AD Identity SnapIn" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Broker PowerShell Snap-In" Version="5.1.0.21"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Broker Service" Version="5.1.0.21"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Common Commands" Version="1.1.2.0"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Configuration Service" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Configuration SnapIn" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Desktop Director" Version="Version="2.0.0.186"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Desktop Studio" Version="5.1.0.207"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Group Policy Management (x64)" Version="1.5.0.0"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Host Service" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Host SnapIn" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Machine Creation Service" Version="5.1.0.192"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" Web Interface" Version="5.4.0.59"'
		print ' Vendor="Citrix Systems, Inc." Name="Citrix" XenDesktop" Version="5.5"'
		print ' Vendor="Adobe Corporation"	Name="Adobe Flash" Version="10.1"'
		print ' Vendor="Microsoft Corporation"	Name="Microsoft SQL Server 2008 R2 Management Objects" Version="10.50.1600.1"'
		print ' Vendor="Microsoft Corporation"	Name="Microsoft SQL Server 2008 R2 Management Objects (x64)" Version="10.50.1600.1"'
		print ' Vendor="Microsoft Corporation"	Name="Microsoft SQL Server System CLR Types" Version="10.50.1600.1"'
		print ' Vendor="Microsoft Corporation"	Name="Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.4148" Version="9.0.30729.4148"'
		print ' Vendor="Microsoft Corporation"	Name="Microsoft Visual J# 2.0 Redistributable Package - SE (x64)" Version="2.0.50728"'
		print ' Vendor="Splunk, Inc."	Name"Universal Forwarder" Version="4.2.3.105575" '


def generateData(farm):
	
	print farm["FarmName"]
	
	START_TIME = datetime.datetime.now() + datetime.timedelta(days=_START)
	END_TIME = datetime.datetime.now() + datetime.timedelta(days=_END)
	
	EventTime = START_TIME
	
	while EventTime < END_TIME:
		
		strEventTime = EventTime.strftime('%x %X')
		
		writeFarmRecord(strEventTime, farm)
		
		for svr in range(int(farm["ServerCount"])):
			server = xaServers.getXAServer()
			sessionCount = str(random.randint(5, 50))
			writeServerRecord(strEventTime, server["ServerName"], server["ServerIP"], sessionCount, farm["FarmName"])
			
			ServerLoads = ["100","10000","1200","2000","1800"]
			ServerLoad = ServerLoads[random.randint(0,len(ServerLoads)-1)]
			writeServerLoad(strEventTime, ServerLoad, server["ServerName"], farm["FarmName"])
			
			writeServerHotfix(strEventTime, "Administrator", server["ServerName"], farm["FarmName"])
			
			writePerfMon(server["ServerName"], strEventTime)
			
		for i in range(_SESSIONS):
			user = localUsers.getUser()
			server = xaServers.getXAServer()
			appName = "APP" + str(i)
			clientIP = "10.20.30." + str(i)
			sessionID = str(i)
			client = clients.getCtxReceiverClient()
			
			writeSessionProcess(strEventTime, user["loginid"], server["ServerName"], sessionID, farm["FarmName"])
			writeSession(strEventTime, user["loginid"], appName, clientIP, client, server["ServerName"], sessionID, farm["FarmName"])
			writeICASesion(strEventTime, sessionID, user["loginid"], server["ServerName"])
			
		for app in range(_APPLICATIONS):
			server = xaServers.getXAServer()
			appName = "App" + str(app)
			writeApplication(strEventTime, appName, server["ServerName"], farm["FarmName"])
		
		EventTime = EventTime + datetime.timedelta(minutes=15)
		
if __name__ == "__main__":
	
	### Adjusting sys.path to include BD-Datagen
	libDir = os.path.join(os.environ["SPLUNK_HOME"], 'etc', 'apps', 'BD-Datagen', 'bin')
	sys.path.insert(1, libDir)
	
	### Importing BD-Datagen Modules
	from datagen.localusers import LocalUsers
	from datagen.logGenerator import LogStore
	from datagen.virtualdesktops import VirtualDesktops
	from datagen.vdiclients import VDIClients
	from datagen.windowsprocesses import WindowsProcesses
	from xaservers import XAServers
	from xafarms import XAFarms
	from datagen.ctxReceiverClients import CtxReceiverClients

	localUsers = LocalUsers()
	virtualdesktops = VirtualDesktops()
	vdiclients = VDIClients()
	xaServers = XAServers()
	xaFarms = XAFarms()
	clients = CtxReceiverClients()
	
	farm = xaFarms.getXAFarm(0)
	
	generateData(farm)
	
	farm = xaFarms.getXAFarm(1)
	generateData(farm)
	#generateData("XA50")
		
		
			
	'''
## Write Data Between the Start and end times
		VDI_SESSION = {}
		VDI_SESSION["LOGIN_DELAY"] =  random.randint(5,60)
		VDI_SESSION["DESKTOP"] =  virtualdesktops.getVDI()
		VDI_SESSION["USER"] = localUsers.getUser()
		VDI_SESSION["CLIENT"] = vdiclients.getVDIClient()
		DRIFT = random.randint(4,15)
		XD_SESSION = getXDSession(VDI_SESSION)
		StartTime = datetime.datetime.now() + datetime.timedelta(days=_START)
		XD_SESSION["StartTime"] = StartTime.strftime('%x %X')
		XD_SESSION["BrokeringTime"] = StartTime.strftime('%x %X')
		SessionStateChangeTime =  StartTime + datetime.timedelta(seconds=VDI_SESSION["LOGIN_DELAY"])
		XD_SESSION["SessionStateChangeTime"] = SessionStateChangeTime.strftime('%x %X')
		XD_SESSION["EventTime"] = SessionStateChangeTime.strftime('%x %X')
		EventTime = SessionStateChangeTime
		DATE_COUNTER = StartTime
		BREAK = random.randint(28,35)
		i = 0
		END_TIME = datetime.datetime.now() + datetime.timedelta(days=_END)
		
		while EventTime < END_TIME:
			writeVDISession(XD_SESSION)
			writeDesktopRecord(VDI_SESSION["DESKTOP"],XD_SESSION["EventTime"])
			
			writePerfMon(VDI_SESSION["DESKTOP"], EventTime)
			
			writeDesktopGroupRecord(VDI_SESSION["DESKTOP"]["DesktopGroupName"],XD_SESSION["EventTime"])

			writeICARecord(VDI_SESSION["DESKTOP"],VDI_SESSION["USER"],XD_SESSION["EventTime"])
			EventTime = EventTime + datetime.timedelta(minutes=15)
			XD_SESSION["EventTime"] = EventTime.strftime('%x %X')
#			print str(i) + " ::: " + XD_SESSION["EventTime"] + " ::: " + str(BREAK)

			if i > BREAK:
#				print "BUMP"

				###if things get weird make this number 45. Keeping low for dense reports
				NewEventTime = EventTime + datetime.timedelta(minutes=15)

				NewStartTime = EventTime
				NewSessionStateChangeTime =  EventTime
				XD_SESSION["StartTime"] = NewStartTime.strftime('%x %X')
				XD_SESSION["SessionStateChangeTime"] = NewSessionStateChangeTime.strftime('%x %X')
				XD_SESSION["EventTime"] = NewEventTime.strftime('%x %X')
#				print "BUMP!"+str(BREAK)
				i = 0
				miscDesktop = virtualdesktops.getVDI()
				STATES = ["Disconnected","Off","Unregistered","Disconnected","Off","Disconnected","Off","Disconnected","Off","Disconnected","Off","Disconnected","Off","Disconnected","Off","Disconnected","Off","Unregistered"]
				miscDesktop["SummaryState"] = STATES[random.randint(0,len(STATES)-1)]	
				writeDesktopRecord(miscDesktop,XD_SESSION["EventTime"])
				writeInventory(VDI_SESSION["DESKTOP"], EventTime)
			else:
				i = i + 1
#			print XD_SESSION["UserName"]
#			print x
			
	'''	
				

				
