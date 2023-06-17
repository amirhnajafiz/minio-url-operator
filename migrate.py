import sys
import logging

from config.config import Config
from storage.sql import SQLConnector


logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
)

# load app configs
cfg = Config()
cfg.load()

# open connection to storages
sqlC = SQLConnector(host=cfg.sql['host'])

cursor = sqlC.get_cursor()
path = ""

# choosing the migration type
if sys.argv[1] == "up":
    path = "up-migration-object_urls-001.sql"
else:
    path = "down-migration-object_urls-001.sql"

# read migration query
with open(f'database/sql/{path}', 'r') as file:
    query = file.read()

logging.info(f'migration started: {sys.argv[1]}')

# execute migration
cursor.execute(query)

logging.info("migration completed")
