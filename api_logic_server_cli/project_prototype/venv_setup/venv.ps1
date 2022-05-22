if($args.Count -eq 0) {

        Write-Output " "
        Write-Output "Installs virtual environment (as venv)"
        Write-Output " "
        Write-Output " IMPORTANT - Windows only, not required for docker-based projects"
        Write-Output " "
        Write-Output "Usage:"
        Write-Output "  cd ApiLogicProject  # your project directory"
        Write-Output "  bin/venv go"
        Write-Output " "
        exit 0
}

virtualenv venv
venv\Scripts\activate
pip install -r requirements.txt
