# runs ApiLogicServer basic web app:
# python ui/basic_web_app/run.py

# Export PYTHONPATH, to enable python ui/basic_web_app/run.py
import os, sys, logging
from pathlib import Path

logger = logging.getLogger()

current_path = Path(os.path.abspath(os.path.dirname(__file__)))
current_path = current_path.parent.absolute()  # ui
current_path = current_path.parent.absolute()  # project
project_dir = str(current_path)
sys.path.append(project_dir)

import ui.basic_web_app.config as config
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)  # DEBUG, INFO, <default> WARNING, ERROR, CRITICAL
auto_log_narrow = True
if auto_log_narrow and config.SQLALCHEMY_DATABASE_URI.endswith("db.sqlite"):
    formatter = logging.Formatter('%(message).120s')  # lead tag - '%(name)s: %(message)s')
else:
    formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = True

fab_logger = logging.getLogger("flask_appbuilder")
fab_logger.setLevel(logging.WARNING)

logic_logger = logging.getLogger("logic_logger")
logic_logger.setLevel(logging.INFO)

logger.setLevel(logging.WARNING)  # WARNING to reduce output, INFO for more
logger.info(f'ui/basic_web_app/run.py - project_dir: {project_dir}')

# args for help
import sys
if len(sys.argv) > 1 and sys.argv[1].__contains__("help"):
    print("")
    print("basic_web_app - run instructions (defaults are host 0.0.0.0, port 5002):")
    print("  python run.py [host [port]]")
    print("")
    sys.exit()

try:
    logger.debug("\nui/basic_web_app/run.py - PYTHONPATH" + str(sys.path) + "\n")
    # e.g., /Users/val/dev/servers/api_logic_server/ui/basic_web_app
    from app import app  # ui/basic_web_app/app/__init__.py activates logic
except Exception as e:
    logger.error("ui/basic_web_app/run.py - Exception importing app: " + str(e))

# args to avoid port conflicts, e.g., localhost 8080
host = sys.argv[1] if sys.argv[1:] \
    else "api_logic_server_default_host"  # docker uses 0.0.0.0, local install uses localhost
port = sys.argv[2] if sys.argv[2:] \
    else "5002"

app.run(host=host, port=port, debug=True)
