from safrs import SAFRSAPI
import safrs
from database import models
import logging as logging

app_logger = logging.getLogger('api_logic_server_app')
app_logger.info("api/expose_api_models.py - endpoint for each table")
