Function GetXASessionState ($state) 
{
	switch($state) 
	{
		0 { "Unknown" }
		1 { "Active" }
		2 { "Connected" }
		3 { "Connecting" }
		4 { "Shadowing" }
		5 { "Disconnected" }
		6 { "Idle" }
		7 { "Listening" }
		8 { "Resetting" }
		9 { "Down" }
		10 { "Initializing" }
		11 { "Stale" }
		12 { "Licensed" }
		13 { "Unlicensed" }
		14 { "Reconnected" }
		default { "Unknown" }
	}
}

Function GetProcessState($processState)
{
	switch($processState)
	{
		0 { "Unknown" }
		1 { "Initialized" }
		2 { "Ready" }
		3 { "Running" }
		4 { "Standby" }
		5 { "Terminated" }
		7 { "InTransit" }
		8 { "Executive" }
		9 { "WaitingFreePage" }
		10 { "WaitingPagedIn" }
		11 { "WaitingPoolAlloc" }
		12 { "Delayed" }
		13 { "Suspended" }
		14 { "WaitingUserRequest" }
		15 { "EventHigh" }
		16 { "EventLow" }
		17 { "LpcReceive" }
		18 { "LpcReply" }
		19 { "WaitingMemory" }
		20 { "PageOut" }
		21 { "WaitOther" }
		default { "Unknown" }
	}
}

Function ConvertMFTime($mfTime) 
{
    $dt = Get-Date

	try
	{
        $dt = (Get-Date -Year $mfTime.Year -Month $mfTime.Month -Day $mfTime.Day -Hour $mfTime.Hour -Minute $mfTime.Minute -Second $mfTime.Second).ToUniversalTime()
    }
	catch [System.Exception]
	{
		# log error here
	}

    return $dt;
}

Function GetMFDuration($mfTime)
{
	return [Math]::Abs($mfTime.HightPart * [Math]::Pow(2, 32) + $mfTime.LowPart)
}

Function GetProtocolType($protocolType)
{
	switch($protocolType)
	{
		0 { "Unknown" }
		1 { "Ica" }
		2 { "Rdp" }
		3 { "Console" }
		default { "Unknown" }
	}
}

Function GetCPUPriorityLevel($cpuLevel)
{
	switch($cpuLevel)
	{
		0 { "Unknown" }
		1 { "BelowNormal" }
		2 { "Low" }
		3 { "Normal" }
		4 { "AboveNormal" }
		5 { "High" }
		default { "Unknown" }
	}
}

Function GetColorDepth($colorDepth)
{
	switch($colorDepth)
	{
		0 { "Unknown" }
		1 { "Colors4Bit" }
		2 { "Colors8Bit" }
		3 { "Colors16Bit" }
		4 { "Colors24Bit" }
		default { "Unknown" }
	}
}

Function GetCachingOption($cachingOption)
{
	switch($cachingOption)
	{
		0 { "Unknown" }
		1 { "PreLaunch" }
		2 { "AtLaunch" }
	}
}

Function GetWindowType($windowType)
{
	switch($windowType)
	{
		0 { "Unknown" }
		1 { "640x480" }
		2 { "800x600" }
		3 { "1024x768" }
		4 { "1280x1024" }
		5 { "Custom" }
		6 { "Percent" }
		7 { "FullScreen" }
		8 { "1600x1200" }
		default { "Unknown" }
	}
}

Function GetEncryptionLevel($encryptionLevel)
{
	switch($encryptionLevel)
	{
		0 { "Unknown" }
		1 { "Basic" }
		2 { "LogOn" }
		3 { "Bits40" }
		4 { "Bits56" }
		5 { "Bits128" }
		default { "Unknown" }
	}
}

Function GetAudioType($audioType)
{
	switch($audioType)
	{
		0 { "Unknown" }
		1 { "None" }
		2 { "Basic" }
		default { "Unknown" }
	}
}

Function GetMFType($mfType)
{
	switch($mfType)
	{
		0 { "Unknown" }
		1 { "Farm" }
		2 { "Zone" }
		3 { "ServerInstalled" }
		4 { "License" }
		5 { "AccountAuthority" }
		6 { "Server" }
		7 { "User" }
		8 { "Group" }
		9 { "Process" }
		10 { "Session" }
		11 { "VirtualChannel" }
		12 { "ApplicationFolder" }
		13 { "ServerFolder" }
		14 { "InstallationManagerServiceApplication" }
		15 { "ResourceManagerService" }
		16 { "UNIXApplication" }
		17 { "Content" }
		18 { "FileType" }
		19 { "SessionPolicy" }
		20 { "LicenseSet" }
		21 { "LicenseNumber" }
		22 { "AccountFolder" }
		23 { "Printer" }
		24 { "PrinterDriver" }
		25 { "Administrator" }
		26 { "MeArray" }
		27 { "LoadEvaluator" }
		28 { "PolicyFilter" }
		29 { "ApplicedPolicy" }
		30 { "File" }
		31 { "Icon" }
		32 { "VirtualIPRange" }
		33 { "LoadManagerRule" }
		34 { "AIE" }
		35 { "AIEFolder" }
		36 { "AIERule" }
		37 { "Hotfix" }
		38 { "StreamedToServer" }
		39 { "InstallationManagerPackage" }
		40 { "InstallationManagerPackageGroup" }
		41 { "ServerGroup" }
		42 { "MonitoringProfileFolder" }
		43 { "InstallationManagerConfiguration" }
		44 { "InstallationManagerJob" }
		default { "Unknown" }
	}
}

Function GetXAElectionPreference($electionPref)
{
	switch($electionPref)
	{
		0 { "Unknown" }
		1 { "MostPreferred" }
		2 { "Preferred" }
		3 { "DefaultPreference" }
		4 { "NotPreferred" }
		default { "Unknown" }
	}
}

Function GetXAEdition($edition)
{
	switch ($edition)
	{
		"STD" { "Standard" }
		"ADV" { "Advanced" }
		"ENT" { "Enterprise" }
		"PLT" { "Platinum" }
		default { "Unknown" }
	}
}

