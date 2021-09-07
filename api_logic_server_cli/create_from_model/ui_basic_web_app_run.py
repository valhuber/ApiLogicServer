# runs ApiLogicServer basic web app:
# python ui/basic_web_app/run.py

# Export PYTHONPATH, to enable python ui/basic_web_app/run.py
import os, sys, logging
from pathlib import Path

logger = logging.getLogger()

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')  # lead tag - '%(name)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = True

fab_logger = logging.getLogger("flask_appbuilder")
fab_logger.setLevel(logging.WARNING)

logic_logger = logging.getLogger("engine_logger")
logic_logger.setLevel(logging.WARNING)

logger.setLevel(logging.WARNING)  # use WARNING to reduce output

current_path = Path(os.path.abspath(os.path.dirname(__file__)))
current_path = current_path.parent.absolute()  # ui
current_path = current_path.parent.absolute()  # project
project_dir = str(current_path)
logger.info(f'ui/basic_web_app/run.py - project_dir: {project_dir}')
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
    logger.debug("\nui/basic_web_app/run.py - PYTHONPATH" + str(sys.path) + "\n")
    # e.g., /Users/val/dev/servers/api_logic_server/ui/basic_web_app
    from app import app
except Exception as e:
    logger.error("ui/basic_web_app/run.py - Exception importing app: " + str(e))

# args to avoid port conflicts, e.g., localhost 8080
host = sys.argv[1] if sys.argv[1:] \
    else "0.0.0.0"
port = sys.argv[2] if sys.argv[2:] \
    else "8080"

app.run(host=host, port=port, debug=True)
