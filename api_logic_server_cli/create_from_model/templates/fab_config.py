
# begin patch to set db_url for sqlite (only)
#   since sqlite db is copied to created project, we can set db_url here
from pathlib import Path
import logging
running_at = Path(__file__)
project_abs_dir = running_at.parent.absolute()
project_abs_dir = project_abs_dir.parent.absolute()
project_abs_dir = project_abs_dir.parent.absolute()
# print(f'project_abs_dir: {project_abs_dir}')
db_loc = str(project_abs_dir) + "/database/db.sqlite"
db_url = "sqlite:///" + db_loc
logger = logging.getLogger()
logger.info(f'fab_config - db_url: {db_url}')
SQLALCHEMY_DATABASE_URI = db_url
# end patch to set db_url for sqlite (only)

