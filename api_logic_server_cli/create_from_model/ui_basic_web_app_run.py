# runs ApiLogicServer basic web app:
# python ui/basic_web_app/run.py

# Export PYTHONPATH, to enable python ui/basic_web_app/run.py
import logic_bank_utils.util as logic_bank_utils
logic_bank_utils.add_python_path(project_dir="api_logic_server_project_directory", my_file=__file__)

# args for help
import sys
if len(sys.argv) > 1 and sys.argv[1].__contains__("help"):
    print("")
    print("basic_web_app - run instructions (defaults are host 0.0.0.0, port 8080):")
    print("  python run.py [host [port]]")
    print("")
    sys.exit()

try:
    from app import app
except Exception as e:
    print("ui/basic_web_app/run.py - Exception importing app: " + e)

# args to avoid port conflicts, e.g., localhost 8080
host = sys.argv[1] if sys.argv[1:] \
    else "0.0.0.0"
port = sys.argv[2] if sys.argv[2:] \
    else "8080"

app.run(host=host, port=port, debug=True)
