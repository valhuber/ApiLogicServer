# ApiLogicServer - export PYTHONPATH
import logic_bank_utils.util as logic_bank_utils
logic_bank_utils.add_python_path(project_dir="api_logic_server_project_directory", my_file=__file__)

import sys
from app import app

# args to avoid port conflicts, e.g., localhost 5008
host = sys.argv[1] if sys.argv[1:] \
    else "0.0.0.0"
port = sys.argv[2] if sys.argv[2:] \
    else "8080"

app.run(host=host, port=port, debug=True)
