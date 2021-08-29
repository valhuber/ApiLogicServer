# runs ApiLogicServer basic web app:
# python ui/basic_web_app/run.py

# Export PYTHONPATH, to enable python ui/basic_web_app/run.py
import os, sys
from pathlib import Path
current_path = Path(os.path.abspath(os.path.dirname(__file__)))
current_path = current_path.parent.absolute()  # ui
current_path = current_path.parent.absolute()  # project
project_dir = str(current_path)
sys.path.append(project_dir)

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
