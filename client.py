import json
import random
import socket
import sys
import threading
from cmd import Cmd
from typing import Union

    def validate_command(self, command_args: str, required_arg_count: int) -> Union[bool, list]:
        split = command_args.split(maxsplit=1)
        if not split:
            print("Error: No arguments passed in command")
            return False
        elif len(split) != required_arg_count:
            print("Error: Invalid number of arguments")
            return False
