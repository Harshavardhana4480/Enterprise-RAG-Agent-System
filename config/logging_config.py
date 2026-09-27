import sys

from loguru import logger

logger.remove()

logger.add(\
    sys.stdout,
    level="INFO")

logger.add("logs/application.log", \
           rotation="10 MB", level="INFO", 
           retention="30 days", compression="zip")

