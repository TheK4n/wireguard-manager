from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TOKEN")
ADMINS = env.list("ADMINS")
WG_MANAGER_PATH = env.str("WG_MANAGER_PATH")


class ReturnCodes:
    SystemFail = 1
    PeerNotExists = 10
    ValidationError = 11
    PeerAlreadyExists = 12
    SubnetError = 24


class Text:
    MENU = "WireGuard Manager bot menu"
    HELP = "WireGuard Manager bot\n\nGithub: https://github.com/thek4n/wireguard-manager"
    START = "Hello, Access allowed to {name}"
    CLIENTS = "Clients"
    CLIENT = "Client \"{client_name}\""
    CLIENT_ADDED = "Client \"{client_name}\" was added, here his QR code"
    CLIENT_DELETED = "Client \"{client_name}\" was deleted"
    CLIENT_DELETE_CONFIRM = "You really want to delete client \"{client_name}\"?"
    ASK_NAME = "Send me a name for a new client"
    ERROR_1 = "System fail, check logs"
    ERROR_11 = "Wrong name, you can use letters, numbers and \"-\", \"_\""
    ERROR_10 = "Client \"{client_name}\" does not exists"
    ERROR_12 = "Client \"{client_name}\" already exists"
    ERROR_24 = "24 net supports only 253 peers"


class ButtonText:
    ADD_CLIENT = "Add client"
    BACK_MENU = "<< Back to menu"
    GET_QR = "Get QR Code"
    GET_FILE = "Get file"
    GET_RAW = "Get raw"
    DELETE = "Delete"
    CONFIRM = "Confirm!"
    CLIENTS = "Clients"
