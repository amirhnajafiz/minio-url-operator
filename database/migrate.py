import sys

from config.config import Config
from storage.sql import SQLConnector


# load app configs
cfg = Config()
cfg.load()

# open connection to storages
sqlC = SQLConnector(host=cfg.sql['host'])

if sys.argv[1] == "up":
    pass
else:
    pass
