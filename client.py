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

def _receive(self):
        while True:
            # Note: Modifying outside variables in this thread may not be thread-safe.

            # print('waiting to receive message')
            data, address = client.recvfrom(1024)
            
            # print('received %s bytes from %s' % (len(data), address))
            # print(data.decode())

            # Expect JSON
            reply = json.loads(data.decode())
            # print(reply)

            # Error and information
            if reply['command'] == 'error':
                print(f"Error: {reply['message']}")
                continue
            if reply['command'] == 'info':
                print(reply['message'])
                continue
                
            # Process receive chain of the commands
            if reply['command'] == 'msg':
                print(f"[From {reply['handle']}]: {reply['message']}")
            elif reply['command'] == 'all':
                print(f"{reply['handle']}: {reply['message']}")
    
    def validate_command(self, command_args: str, required_arg_count: int) -> Union[bool, list]:
        split = command_args.split(maxsplit=1)
        if not split:
            print("Error: No arguments passed in command")
            return False
        elif len(split) != required_arg_count:
            print("Error: Invalid number of arguments")
            return False
