import json
import random
import socket
import sys
import threading
from cmd import Cmd
from typing import Union

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Technically, this is not necessary for client but recvfrom() will complain without it.
client.bind(('localhost', random.randint(8000, 9000)))

class MBSClientShell(Cmd):
    prompt = ''
    intro = '\nWelcome to the CSNETWK Message Board System.\nType /help or /? to list commands.\n\nTo exit the program, enter /quit.\n'
    
    server_address = ()

    def validate_command(self, command_args: str, required_arg_count: int) -> Union[bool, list]:
        split = command_args.split(maxsplit=1)
        if not split:
            print("Error: No arguments passed in command")
            return False
        elif len(split) != required_arg_count:
            print("Error: Invalid number of arguments")
            return False
