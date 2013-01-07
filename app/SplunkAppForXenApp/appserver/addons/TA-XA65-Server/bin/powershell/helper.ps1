function ConvertTo-SplunkTable
{
	[cmdletbinding()]
    param(
        [Parameter(ValueFromPipeline=$true)]
        [Object]$InputObject,
        
        [Parameter()]
        [System.Collections.Hashtable]$Properties,
		
		[Parameter()]
		[string]$Filter = ".*"
		
    )
	Begin
	{
		function Get-Header($object)
		{
			($object | Get-Member -MemberType Properties | %{$_.Name -replace "\s","_" } ) -join " "
		}
		
		$RetrieveHeader = $false
		$ScriptRunTime = (get-date).ToFileTime()
		"{0:MM/dd/yyyy HH:mm:ss} GMT - {0}" -f ((get-date).ToUniversalTime())
	}
	Process
	{
		if(!$RetrieveHeader)
		{
			'{0}="{1}"' -f "ScriptRunTime",$ScriptRunTime
			Get-Header $InputObject
			$RetrieveHeader = $true
		}
		$Events = @()
		$InputObject | Get-Member -MemberType Properties | foreach-object {
			$Name = $_.Name
			if( $InputObject.$Name )
			{
				$Events += $InputObject.$Name -replace "\s","_" 
			}
			else
			{
				$Events += "null"
			}
        }
		
		$Events -join " "
		
	}
}

function ConvertTo-SplunkString
{
    [cmdletbinding()]
    param(
        [Parameter(ValueFromPipeline=$true)]
        [Object]$InputObject,
        
        [Parameter()]
        [System.Collections.Hashtable]$Properties,
		
		[Parameter()]
		[string]$Filter = ".*"
		
    )
    
    Process
    {
    
        $ScriptRunTime = (get-date).ToFileTime()

        $InputObject | foreach-object {
            $Current = $_
            $output = $Current | Get-Member -MemberType Properties | where{$_.name -match $Filter } | foreach-object {
                $Key = $_.Name
                $Value = $Current.$Key -join ";"
                '{0}="{1}"' -f $Key,$Value
                foreach($Property in $Properties.Keys)
                {
                    if($Key -eq $Property)
                    {
                        if($Properties[$Property] -is [system.array])
                        {
                            '{0}="{1}"' -f ($Properties[$Property][0]),($Value -replace $Properties[$Property][1],'$1')
                        }
                        else
                        {
                            '{0}="{1}"' -f $Properties[$Property],$Value
                        }
                    }
                }
            }

            $output += '{0}="{1}"' -f "ScriptRunTime",$ScriptRunTime

            $Message = ("{0:MM/dd/yyyy HH:mm:ss} GMT - {1}" -f ((get-date).ToUniversalTime()),( $output -join " " ))
            Write-Verbose $Message
            $Message
            
        }
        
    }
}