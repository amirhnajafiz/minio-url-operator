from config.config import Config


# load app configs
cfg = Config()
cfg.load()

print(cfg.port)
