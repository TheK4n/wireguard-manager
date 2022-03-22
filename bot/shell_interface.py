import subprocess
from io import BytesIO

from data import WG_MANAGER_PATH


def execute_command(command: str, *args) -> subprocess.CompletedProcess:
    command_ = ["bash", WG_MANAGER_PATH, command]
    for i in args:
        command_.append(i)
    command_.append("")
    return subprocess.run(command_, capture_output=True)


def get_clients_from_manager() -> list:
    return execute_command("ls").stdout.decode().split("\n")


def get_config_qrcode(client_name: str) -> bytes:
    return execute_command("get_tg", client_name).stdout


def get_config_raw(client_name: str) -> bytes:
    return execute_command("get_file", client_name).stdout


def add_client(client_name: str) -> bytes:
    return execute_command("add_tg", client_name).stdout


def delete_client(client_name: str):
    return execute_command("rm", client_name)


def put_bytes_to_file(file: bytes) -> BytesIO:
    bytes_file = BytesIO(file)
    bytes_file.seek(0)
    return bytes_file
