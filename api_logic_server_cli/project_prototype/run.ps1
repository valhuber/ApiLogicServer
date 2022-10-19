Set-PSDebug -Trace 0  # Use 1 for LOTS of output

if ($args[0] -contains "help") {
    Write-Output "`r`nRuns API Logic Project, using venv in:"
    Write-Output "   - project folder (no args)"
    Write-Output "   - calling folder (arg 1)`r`n"
    exit 0
}

# Write-Output "`r`nRunning at caller path: $PWD, with $($args.Count) args"

if ($args.count -gt 0) { 
    # Write-Output "Using calling venv"
    .\venv\Scripts\activate
}

# change path to project
$prevPwd = $PWD; Set-Location -ErrorAction Stop -LiteralPath $PSScriptRoot
# Write-Output "PWD to project: $PWD"

try {
    if ($args.count -eq 0) { 
        # Write-Output "Using project venv: $PWD"
        .\venv\Scripts\activate
    }
    python api_logic_server_run.py
}
finally {
  $prevPwd | Set-Location
}
