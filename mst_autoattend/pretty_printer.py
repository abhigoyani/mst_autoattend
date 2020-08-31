from datetime import now
from os import environ

SUPPORTED_TYPES = ["DEBUG", "INFO", "ERROR", "WARNING"]
PATH_TO_HELP = './static/help.txt'

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

def print_help():
    with open(PATH_TO_HELP, 'r') as f:
        help_text = f.read()
        print(help_text)