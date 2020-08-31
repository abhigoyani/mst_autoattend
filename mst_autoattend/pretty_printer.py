from datetime import now
from os import environ

SUPPORTED_TYPES = ["DEBUG", "INFO", "ERROR", "WARNING"]

def print_msg(msg, type):
    if type not in SUPPORTED_TYPES:
        raise Exception("Unsupported type of message")
    if type == "DEBUG" and not environ.get("DEBUG"):
        return
    print('{date} | {type} : {msg}'.format(
        type=type,
        date=now(),
        msg=msg
        )
    )
