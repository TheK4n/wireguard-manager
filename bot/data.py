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
    "CLIENTS": "Clients",
    "SEND_NAME": "Send me a name for a new client",
    "CLIENT_ADDED": "Client \"{client_name}\" was added, here his QR code",
    "CLI_DEL_CONF": "You really want to delete client \"{client_name}\"?",
    "CLI_DEL": "Client \"{client_name}\" was deleted",
}
