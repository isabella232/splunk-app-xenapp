Param($Computer = $ENV:ComputerName)   

$ScriptRunTime = (get-date).ToFileTime()
$myobjs = @()   
$RemoteRegistry = [Microsoft.Win32.RegistryKey]::OpenRemoteBaseKey("LocalMachine",$Computer)   

$RegKey = $RemoteRegistry.OpenSubKey("SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\")  
foreach($key in $RegKey.GetSubKeyNames())   
{   
    $SubKey = $RegKey.OpenSubKey($key)
    $DisplayName = $SubKey.GetValue("DisplayName")
    if($DisplayName)
    {
        write-Host ('Name="{0}" '           -f $DisplayName) 	-nonewline
        write-Host ('Version="{0}" '        -f $SubKey.GetValue("DisplayVersion"))  -nonewline
        write-Host ('InstallLocation="{0}" ' -f $SubKey.GetValue("InstallLocation"))  -nonewline
        write-Host ('Vendor="{0}" '         -f $SubKey.GetValue("Publisher")) -nonewline
        write-Host ('ScriptRunTime="{0}"'   -f $ScriptRunTime)
    }

}   

$RegKey = $RemoteRegistry.OpenSubKey("SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall")   
foreach($key in $RegKey.GetSubKeyNames())   
{   
    $SubKey = $RegKey.OpenSubKey($key)   
    $DisplayName = $SubKey.GetValue("DisplayName")
    if($DisplayName)
    {
        write-Host ('Name="{0}" '           -f $DisplayName) 	-nonewline
        write-Host ('Version="{0}" '        -f $SubKey.GetValue("DisplayVersion"))  -nonewline
        write-Host ('InstallLocation="{0}" ' -f $SubKey.GetValue("InstallLocation"))  -nonewline
        write-Host ('Vendor="{0}" '         -f $SubKey.GetValue("Publisher")) -nonewline
        write-Host ('ScriptRunTime="{0}"'   -f $ScriptRunTime)
    }
}   
