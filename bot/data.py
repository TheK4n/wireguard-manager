from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
ADMINS = env.list("ADMINS")
WG_MANAGER_PATH = env.str("WG_MANAGER_PATH")


MESSAGES = {
    "MENU": "WireGuard Manager bot menu",
    "HELP": "WireGuard Manager bot\n\nGithub: https://github.com/thek4n/wireguard-manager",
    "START": "Hello, Access allowed to {name}",
}
