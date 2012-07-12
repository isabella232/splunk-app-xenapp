# # # # # # # # # # # # # # # # # # # # # # #

#	Data Generator for a XD5 Deployment 

#	- XenDesktop 5 Sessions
#	- XenDesktop 5 Desktops
#	- Windows Perfmon Counters
#	- XenDesktop 5 Desktops
#	- Un-Authorized Device Access Scenerio 

# # # # # # # # # # # # # # # # # # # # # # #

import time,sys,os,traceback,random,datetime

_START =	-1
_END = 0
_SESSIONS = 25
BAD_USERS= [
{'GUID': 'BC9CCABC-DA44-11E0-B014-91A3616AB75D', 'SID': 'S-1-5-21-3623811017-899348573-30700820-9921', 'site': 'AUSTIN', 'iphostname': 'dhcp-172-16-210-11', 'mboxserver': 'exch-mbx-san-01', 'ipaddress': '172.11.210.11', 'email': 'dan@spl.com', 'loginid': 'SPL\\dan'},
{'GUID': 'BC9CCABC-DA44-11E0-B014-91A3616AB75D', 'SID': 'S-1-5-21-3623811017-899348573-30700820-5421', 'site': 'AUSTIN', 'iphostname': 'dhcp-172-16-210-10', 'mboxserver': 'exch-mbx-san-01', 'ipaddress': '172.11.210.10', 'email': 'brett@spl.com', 'loginid': 'SPL\\brett'},
{'GUID': 'BC9CCABC-DA44-11E0-B014-91A3616AB75D', 'SID': 'S-1-5-21-3623811017-899348573-30700820-5021', 'site': 'AUSTIN', 'iphostname': 'dhcp-172-16-210-08', 'mboxserver': 'exch-mbx-san-01', 'ipaddress': '172.11.210.08', 'email': 'wilde@spl.com', 'loginid': 'SPL\\wilde'},
{'GUID': 'BC9CCABC-DA44-11E0-B014-91A3616AB75D', 'SID': 'S-1-5-21-3623811017-899348573-30700820-5021', 'site': 'AUSTIN', 'iphostname': 'dhcp-172-16-210-07', 'mboxserver': 'exch-mbx-san-01', 'ipaddress': '172.11.210.07', 'email': 'hal@spl.com', 'loginid': 'SPL\\hal'}
]

TARGET_IPS = ["172.16.210.89","172.16.210.90","172.16.210.91","172.16.210.92","172.16.210.93","172.16.210.94"]
	
APP_NAME = 'BD-Datagen-XENDT'
## Define output log
xd_sessions_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xd5_sessions_badusr.log'),'w')
xd_desktops_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xd5_desktops_badusr.log'),'w')
xd_desktopsgroups_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xd5_desktop_groups_badusr.log'),'w')
xd_ica_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','xd5_ica_badusr.log'),'w')

badusr_cisco_wsa_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','cisco_wsa_badusr.log'),'w')
badusr_cisco_ips_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','cisco_ips_badusr.log'),'w')
badusr_cisco_fw_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','cisco_fw_badusr.log'),'w')
badusr_exchwinevent_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','exch-hub-cup-01','win-eventlog-exch-hub-cup.log'),'w')
badusr_exchwinevent2_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','exch-hub-cup-01','win-eventlog-exch-hub-cup.log'),'w')

badusr_exchmsgtrack_out = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'logs','exch-hub-cup-01','exchange-msgtrack-exch-hub-san-01-2012-02-27-20:01:16.log'),'w')
xd_perfmon_out = "" 



def logger(string):
	BD_DATAGEN_LOG.write(time.asctime() + ' - ' + string + "\n")
	BD_DATAGEN_LOG.flush()
#	print time.asctime() + ' - ' + string
	return 0


def writeIPSAlert(User,EventTime):
	ts = ( EventTime - datetime.timedelta(hours=3) ).strftime('%X %x')
	
	for ip in TARGET_IPS:
		evt =  str(ts) + ' eventid="1278457197410173971" severity=severe mars_category="Info/AllSession" hostId=ips.secure.acme signature=4151-0 description="BOBAX Virus Activity " attacker='+User['ipaddress']+' target='+ip+' target=141.146.8.66  gc_score="1" gc_riskdelta="1" gc_riskrating="false" gc_deny_packet="true" gc_deny_attacker="false" \n\n' 
		badusr_cisco_ips_out.writelines(evt)
		badusr_cisco_ips_out.writelines("\n")
#		print evt
#		print ' 18:18:09 02/27/12 eventid="1278457197410173971" severity=severe mars_category="Info/AllSession" hostId=s signature=4151-0 description="BOBAX Virus Activity " attacker=202.111.0.17 target=125.17.14.100 target=141.146.8.66  gc_score="1" gc_riskdelta="1" gc_riskrating="false" gc_deny_packet="true" gc_deny_attacker="false" '
	badusr_cisco_ips_out.flush()
	return 0

def writeFirewallEvent(User,EventTime):
#	print "FIREWALL:::"+str(User)
	BOTNET = ["110.173.32.20","110.240.0.12","110.52.0.15","109.120.0.18","110.16.0.14"]
	ts = ( EventTime - datetime.timedelta(hours=3) ).strftime('%b %d  %H:%M:%S: ')
	for ip in BOTNET:
		evt = str(ts) + "%ASA-4-338002: Dynamic Filter blocked black listed TCP traffic from inside:"+User['ipaddress']+"/6798 ("+User['ipaddress']+"/7890) to outside:"+ip+"/80 ("+ip+"/80), destination "+ip+" resolved from dynamic list: bad.example.com\n\n\n"
		badusr_cisco_fw_out.writelines(evt)
		badusr_cisco_fw_out.writelines('\n')
	badusr_cisco_fw_out.flush()
##  %b %d %H:%M:%S 1,%Y/%m/%d %H:%M:%S,
##"Feb 25 01:01:40 1,2012/02/25 01:01:40,"
	return 0


def writeBadWSATraffic(User,EventTime):
#BAD WEB BROWSING WSA SAMPLES
	badusr_cisco_wsa_in = open(os.path.join(os.environ["SPLUNK_HOME"], 'etc','apps',APP_NAME,'bin','data','bad_wsa_traffic'))
	badTraffic = badusr_cisco_wsa_in.readlines()
	for line in badTraffic:
		user = User['loginid'][User['loginid'].find('\\')+1:]
		l = line.replace('###C_IP###',User['ipaddress']).replace('###USER###',user)
		evt = str(time.time()- 86400) + l[l.find(' '):] + "\n"
		badusr_cisco_wsa_out.writelines(evt)
		badusr_cisco_wsa_out.writelines('\n')

		
#	return 0


def writeDesktopGroupRecord(DesktopGroupName,EventTime):
	
	DesktopGrops = {"Developer XP Desktops":(100,1,3,30,10,300),"Developer Win7 64 Bit":(200,5,12,30,40,500),"Developer Win7 32 Bit":(300,5,12,40,70,500),"Developer Win Vista":(100,2,1,90,4,400),"Production Win 7 x64":(450,5,35,50,2,700),"Developer Win7 32 Bit":(900,5,23,10,6,1000) }
	log_line = ' - AdministratorNames="" AutomaticPowerOnForAssigned="True" ColorDepth="TwentyFourBit" Description="" DesktopKind="Shared" DesktopsAvailable="' + str( DesktopGrops[DesktopGroupName][0] )  + '" DesktopsDisconnected="' + str( DesktopGrops[DesktopGroupName][1] )  + '" DesktopsInUse="' + str( DesktopGrops[DesktopGroupName][2] )  + '" DesktopsNeverRegistered="' + str( DesktopGrops[DesktopGroupName][3] )  + '" DesktopsUnregistered="' + str( DesktopGrops[DesktopGroupName][4] )  + '" Enabled="True" IconUid="1" InMaintenanceMode="False" Name="'+DesktopGroupName+'" OffPeakBufferSizePercent="10" OffPeakDisconnectAction="Nothing" OffPeakDisconnectTimeout="0" OffPeakExtendedDisconnectAction="Nothing" OffPeakExtendedDisconnectTimeout="0" OffPeakLogOffAction="Nothing" OffPeakLogOffTimeout="0" PeakBufferSizePercent="10" PeakDisconnectAction="Nothing" PeakDisconnectTimeout="0" PeakExtendedDisconnectAction="Nothing" PeakExtendedDisconnectTimeout="0" PeakLogOffAction="Nothing" PeakLogOffTimeout="0" ProtocolPriority="" PublishedName="' + DesktopGroupName + '" SecureIcaRequired="False" ShutdownDesktopsAfterUse="False" Tags="" TimeZone="Pacific Standard Time" TotalDesktops=" '+ str( DesktopGrops[DesktopGroupName][5] )  + '" Uid="9" UUID="2ea8e3f2-7cac-421d-b593-a25622ea598d" \n'
	evt = EventTime + " - " + log_line 
	xd_desktopsgroups_out.writelines("")
	xd_desktopsgroups_out.writelines(evt)
	xd_desktopsgroups_out.writelines("")
	xd_desktopsgroups_out.flush()
	return 0

def writeICARecord(Desktop,User,EventTime):
	Desktop = Desktop["MachineName"][Desktop["MachineName"].find('\\')+1:]
	User = User["loginid"][User["loginid"].find('\\')+1:]
	BANDWIDTH = random.randint(150, 10000)
	BANDWIDTH2 = random.randint(160, 10000)
	LATANCY = random.randint(250, 800)
	evt = "\n"+ EventTime + " GMT - hostname="+Desktop+' Caption="" Description="" Frequency_Object="" Frequency_PerfTime="" Frequency_Sys100NS="" InputAudioBandwidth="0" InputClipboardBandwidt="0" InputCOM1Bandwidth="0" InputCOM2Bandwidth="0" InputCOMBandwidth="0" InputControlChannelBandwidth="0" InputDriveBandwidth="0" InputHDXMediaStreamforFlashDataBandwidth="0" InputLPT1Bandwidth="0" InputLPT2Bandwidth="0" InputPrinterBandwidth="0" InputSessionBandwidth="'+str(BANDWIDTH2)+'" InputSessionCompression="0" InputSessionLineSpeed="0" InputSmartCardBandwidth="0" InputSpeedScreenDataChannelBandwidth="0" InputSpeedScreenMultimediaAccelerationBandwidth="0" InputThinWireBandwidth="0" InputUSBBandwidth="0" LatencyLastRecorded="0" LatencySessionAverage="'+str(LATANCY)+'" LatencySessionDeviation="5" Name="Console ('+User+')" UserName="'+User+'" OutputAudioBandwidth="0" OutputClipboardBandwidth="0" OutputCOM1Bandwidth="0" OutputCOM2Bandwidth="0" OutputCOMBandwidth="0" OutputControlChannelBandwidth="0" OutputDriveBandwidth="0" OutputHDXMediaStreamforFlashDataBandwidth="0" OutputLPT1Bandwidth="0" OutputLPT2Bandwidth="0" OutputPrinterBandwidth="0" OutputSessionBandwidth="'+str(BANDWIDTH)+'" OutputSessionCompression="15" OutputSessionLineSpeed="35698896" OutputSmartCardBandwidth="0" OutputSpeedScreenDataChannelBandwidth="0" OutputSpeedScreenMultimediaAccelerationBandwidth="0" OutputThinWireBandwidth="13" OutputUSBBandwidth="0" Timestamp_Object="" Timestamp_PerfTime="" Timestamp_Sys100NS="" __CLASS="Win32_PerfFormattedData_CitrixICA_ICASession" __DERIVATION="Win32_PerfFormattedData;Win32_Perf;CIM_StatisticalInformation" __DYNASTY="CIM_StatisticalInformation" __GENUS="2" __NAMESPACE="root\cimv2" __PATH="\\'+Desktop+'\root\cimv2:Win32_PerfFormattedData_CitrixICA_ICASession.Name="Console ('+User+')"" __PROPERTY_COUNT="50" __RELPATH="Win32_PerfFormattedData_CitrixICA_ICASession.Name="Console ('+User+')"" __SERVER="'+Desktop+'\n' 
#	print evt
	xd_ica_out.writelines("")
	xd_ica_out.writelines(evt)
	xd_ica_out.writelines("")
	xd_ica_out.flush()
	





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
	xd_session["AutonomouslyBrokered"] = "False"
	xd_session["AutonomouslyBrokered"] = "False" 
	xd_session["Protocol"] ="HDX"
	xd_session["SecureIcaActive"] ="False"
	xd_session["SessionId"] ="0"
	xd_session["SessionState"] ="Active"
	xd_session["SmartAccessTags"] =""
	xd_session["SessionUID"]  = str(xd_session["StartTime"]) + ":"+str(xd_session["UserSID"]) + ":"+str(xd_session["DesktopSID"])
	return xd_session




def writePerfMon(Desktop, EventTime):
	host = Desktop["MachineName"][Desktop["MachineName"].find('\\')+1:]
	perf_ts = EventTime
	
	
	print "***SPLUNK*** host="+host+" source=Perfmon:CPULoad sourcetype=Perfmon:CPULoad "
	print perf_ts
	CPU = random.randint(95,100)
	print 'collection=CPULoad' 
	print 'object=Processor'
	print 'counter="% Processor Time'
	print 'instance=Idle'
	print 'Value='+str(CPU)
	print ""

	print "***SPLUNK*** host="+host+" source=Perfmon:AvailableMemory sourcetype=Perfmon:AvailableMemory "
	print perf_ts
	MEM = random.randint(31457280,104857600)
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
	
	XFER = random.randint(25,50)
	print "***SPLUNK*** host="+host+" source=Perfmon:perfmon:LogicalDisk sourcetype=Perfmon:LogicalDisk "	
	print perf_ts
	print 'collection=LogicalDisk'
	print 'object=LogicalDisk'
	print 'counter="Disk Transfers/Sec"'
	print 'instance=_Total'
	print 'Value='+str(XFER)
	
	
	
	PROCS = {
		
				"SuperScan":(100,1500483648,45,14),"T00LBar":(3,2147483648,25,2), "CdfSvc":(2,1018171,1,.01),"CitrixCGPServer":(2,1018171,1,.01),"CtxAudioService":(2,101817100,1,.01),"CtxSvcHost":(2,101817100,1,.01),"FlashUtil11e_ActiveX":(2,101817100,1,.01),"OUTLOOK":(.01,125534,4,4,2),"ccsvchst":(15,1610612736,15,65),"explorer":(75,637495,1,2,1),"iexplore":(100,51200,2,15,20)
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
			
		print "***SPLUNK*** host="+host+" index=xendesktop_winevents  source=WinEventLog:ApplicationX sourcetype=WinEventLog:ApplicationX"
		print str(perf_ts) + ' LogName="Application",SourceName="SuperSaver",EventCode="1008",EventType="2",Type="Error",ComputerName="'+host+'" TaskCategory="None",OpCode="None",RecordNumber="85810",Keywords="Classic",Message="Executable T00LBar.exe failed to respond."'
		print "***SPLUNK*** host="+host+" index=xendesktop_winevents source=WinEventLog:ApplicationX sourcetype=WinEventLog:ApplicationX"
		print str(perf_ts) +  ' LogName="Application ",SourceName="Internet Explorer ",EventCode="1000 ",EventType="2 ",Type="Error ",ComputerName="'+host+'" TaskCategory="Application Crashing Events ",OpCode="Info ",RecordNumber="1194 ",Keywords="Classic ",Message="Faulting module name: MSVCR90.dll, version: 9.0.30729.4940, time stamp: 0x4ca2e32e Exception code: 0xc0000417 Fault offset: 0x00000000000552c0 Faulting process id: 0x1064  Faulting application start time: 0x01cce8de74bc9fdf  Faulting application path: C:\Windows\System32\InternetExplorer\iexplorer.exe  Faulting module path: C:\Windows\WinSxS\amd64_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4940_none_08e4299fa83d7e3c\MSVCR90.dll  Report Id: b6bd1abf-54d1-11e1-843e-00155d00080e "'





def writeInventory(Desktop, EventTime):	
		perf_ts = EventTime
		host = Desktop["MachineName"][Desktop["MachineName"].find('\\')+1:]
		print ""
		print ""		
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
		print ' Vendor="Symantec Inc."	Name="Norton Antivirus" Version="8.0.2"'
		print ' Vendor="Super Savers Inc0rporated"	Name="Super Saver Super Browser Toolbar" Version="2.0.5"'
		print ' Vendor="Super Savers Inc0rporated"	Name="Super Saver Desktop Deals" Version="1.0.2" '
		print ' Vendor="Splunk, Inc."	Name"Universal Forwarder" Version="4.2.3.105575" '
		return 0

def writeMSExchange(User,EventTime):
	rndmsgint = str( random.randint(45938, 77777) )
	MSG_ID = '<20120228010400.'+rndmsgint+'.56785@spl.com>'
	user = User['loginid'][User['loginid'].find('\\')+1:]
	WINMSG = '''
	"START_OF_EVENT"
	 EventTime
	"EventCode=3002"
	"EventType=4"
	"Type=Information"
	"SourceName=FSCTransportScanner"
	"ComputerName=EXCH-HUB-PLA-01"
	"Category=3"
	"CategoryString=Scan Results"
	"Record=50389"
	"Message=Internet Scan found virus:"
	"\tFolder: SMTP Messages\External"
	"\tMessage: Super Saver Toolbar! The Last Toolbar You will Ever Need!!"
	"\tMessage ID: "+MSG_ID
	"\tFile: winmail.dat->attachment"
	"\tIncident: VIRUS= Virus: Exploit-CVE-2010-2568"
	"\tState: Removed"
	""
	""
	'''

	MSGTRACK1 = str(EventTime) + ',,exch-hub -cup-01,,exch-mbx-den-00,,,STOREDRIVER,DELIVER,83322,'+MSG_ID+','+user+'@spl.com,,1441,1,,,Super Saver Toolbar! The Last Toolbar You will Ever Need!!,clayton@xvfz.com,clayton@xvfz.com,2012-02-29T16:18:25.481Z \n'
	MSGTRACK2 = str(EventTime) + ',172.16.44.27,dhcp-172-16-44-27,172.16.43.10,exch-hub-cup-01,,,STOREDRIVER,RECEIVE,83321,'+MSG_ID+','+user+'@spl.com,,1441,1,,,Super Saver Toolbar! The Last Toolbar You will Ever Need!!,clayton@xvfz.com,clayton@xvfz.com,04I: \n'

#20120229062125.31558.51748@ariad.com

	badusr_exchmsgtrack_out.writelines(MSGTRACK1)
	badusr_exchmsgtrack_out.writelines("\n")
	badusr_exchmsgtrack_out.writelines(MSGTRACK2)
	badusr_exchmsgtrack_out.writelines("\n")
	badusr_exchwinevent_out.writelines(WINMSG)
	badusr_exchwinevent_out.writelines("\n")
	badusr_exchwinevent2_out.writelines(WINMSG)
	badusr_exchwinevent2_out.writelines("\n")

	badusr_exchwinevent_out.flush()
	badusr_exchmsgtrack_out.flush()

if __name__ == "__main__":

### Adjusting sys.path to include BD-Datagen

	libDir = os.path.join(os.environ["SPLUNK_HOME"], 'etc', 'apps', 'BD-Datagen', 'bin')
	sys.path.insert(1, libDir)
	
	
### Importing BD-Datagen Modules
	from datagen.localusers import LocalUsers
	from datagen.remotedomains import RemoteUsers
	from datagen.sysHosts import SystemHosts
	from datagen.logGenerator import LogStore
	from datagen.virtualdesktops import VirtualDesktops
	from datagen.vdiclients import VDIClients
	from datagen.windowsprocesses import WindowsProcesses

	localUsers = LocalUsers()
	virtualdesktops = VirtualDesktops()
	vdiclients = VDIClients()

	for USR in BAD_USERS:
#			print "starting user:" + str(USR)
## Write Data Between the Start and end times
		VDI_SESSION = {}
		VDI_SESSION["LOGIN_DELAY"] =  random.randint(5,60)
		VDI_SESSION["DESKTOP"] =  virtualdesktops.getVDI()
		VDI_SESSION["USER"] = USR
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
				writeInventory(VDI_SESSION["DESKTOP"], EventTime)
				writeIPSAlert(VDI_SESSION["USER"],EventTime)
				writeFirewallEvent(VDI_SESSION["USER"],EventTime)
				writeBadWSATraffic(VDI_SESSION["USER"],EventTime)
				badusr_cisco_wsa_out.flush()
#				writeMSExchange(VDI_SESSION["USER"],EventTime)
				i = 0
			else:
				i = i + 1
				
