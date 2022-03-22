from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
ADMINS = env.list("ADMINS")
WG_MANAGER_PATH = env.str("WG_MANAGER_PATH")
