param(
    [Parameter()]
    [String]$UseCallingVenv
)

Set-PSDebug -Trace 0  # Use 1 for LOTS of output

# echo "Running at caller path: $PWD"

if($UseCallingVenv -eq "CallingVenv") { 
    .\venv\Scripts\activate
}

# change path to project
$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot

try {
    if($UseCallingVenv -ne "CallingVenv") { 
        .\venv\Scripts\activate
    }
        python api_logic_server_run.py
}
finally {
  $prevPwd | Set-Location
}
