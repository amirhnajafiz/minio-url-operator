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
paths = []

# choosing the migration type
if sys.argv[1] == "up":
    paths = [
        "up-migration-object_urls-001.sql",
        "up-migration-address_column-002.sql",
        "up-migration-enable_column-003.sql",
        "up-migration-"
    ]
else:
    paths = [
        "down-migration-enable_column-003.sql",
        "down-migration-address_column-002.sql",
        "down-migration-object_urls-001.sql"
    ]

queries = []

# read migration
for path in paths:
    with open(f'database/sql/{path}', 'r') as file:
        query = file.read()
        queries.append(query)

        logging.info(f'migrating: {path}')

logging.info(f'migration started: {sys.argv[1]}')

# execute migration
for query in queries:
    cursor.execute(query)

logging.info("migration completed")
