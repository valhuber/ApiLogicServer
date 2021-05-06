echo on
echo 'Running... logic_logger works'

export PYTHONPATH="/Users/val/dev/servers/api_logic_server"
cd /Users/val/dev/ApiLogicServer
source venv/bin/activate
cd /Users/val/dev/servers/api_logic_server
python api_logic_server_run.py
