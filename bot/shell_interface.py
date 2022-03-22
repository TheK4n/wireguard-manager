import subprocess
from io import BytesIO

from data import WG_MANAGER_PATH


def execute_command(command: str, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["bash", WG_MANAGER_PATH, command, args if args else ""], capture_output=True)


def get_clients_from_manager() -> list:
    return ["asdfasd", "adsasdv", "cvjadfivsad"]
    #return execute_command("ls").stdout.decode().split("\n")


def get_config_qrcode(client_name: str) -> bytes:
    return execute_command("get_tg", client_name).stdout


def get_config_raw(client_name: str) -> bytes:
    return execute_command("get_client", client_name).stdout


def add_client(client_name: str) -> bytes:
    return execute_command("add_tg", client_name).stdout


def delete_client(client_name: str):
    return execute_command("rm", client_name)


def put_bytes_to_file(file: bytes, client_name: str) -> BytesIO:
    bytes_file = BytesIO(file)
    bytes_file.seek(0)
    bytes_file.name = f"{client_name}.conf"
    return bytes_file
