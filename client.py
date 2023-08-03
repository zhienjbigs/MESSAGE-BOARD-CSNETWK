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

    def precmd (self, line:str) -> str:
        if line:
            if line[0] == '/':
                line = line[1:]
            else:
                print("Error: Command must start with '/'")
                line = ''
        return super().precmd(line)

    def emptyline (self) -> None:
        # For program to not repeat last command when user presses enter without any input
        pass

    def do_join (self, arg:str) -> None:
        """ Join a Message Board Server\n (/join <ip> <port>"""

        args = self.validate_command (arg,2)
        if not args:
            return

        if self.server_adress:
            print ("Error: You are already connected to the server!")
            return

        try:
            self.server_adress:
        except ValueError:
            print ("Error: You have entered an invalid port number")
            return

        request = json.dumps({'command': 'join})
        client.sendto(request.encode(), self.server_address)

        try:
            data,  _ = client.recvfrom(1024)
        except ConnectionResetError
            self.server_address = ()
        print ("Error: Connection to the server has failed")
        return

         
        # print('Connection to the Message Board Server is successful!')

        reply = json.loads(data.decode())
        info = reply.get('message')
        print(info)

        t = threading.Thread(target=self._receive)
        t.start()

       def do_leave(self, arg: None) -> None:
        """    Leave the Message Board Server\n    Syntax: /leave"""

        # Command specific error checking
        if not self.server_address:
            print("Error: Not connected to a server.")
            return
            
        # TODO: Stop the thread

    def do_register(self, arg: str) -> None:
        """    Register a handle with the Message Board Server\n    Syntax: /register <handle>"""

        # Basic error checking
        if not arg:
            print("Error: No handle/alias passed in command")
            return

        # Command specific error checking
        if not self.server_address:
            print("Error: Not connected to server. Use '/join <ip> <port>'")
            return

        # Send data
        request = json.dumps({'command': 'register', 'handle': arg})
        client.sendto(request.encode(), self.server_address)

    def do_list(self, arg: None) -> None:
        """    List all handles registered with the Message Board Server\n    Syntax: /list"""

        # Command specific error checking
        if not self.server_address:
            print("Error: Not connected to server. Use '/join <ip> <port>'")
            return

        # Send data
        request = json.dumps({'command': 'list'})
        client.sendto(request.encode(), self.server_address)

    def do_msg(self, arg: str) -> None:
        """    Send a message to a specific handle\n    Syntax: /msg <handle> <message>"""

        # Basic error checking
        args = self.validate_command(arg, 2)
        if not args:
            return

        # Command specific error checking
        if not self.server_address:
            # This being the 2nd error check is okay
            print("Error: Not connected to server. Use '/join <ip> <port>'")
            return

        dest_handle, message = args[0], args[1]            

        # Send data
        request = json.dumps({'command': 'msg', 'handle': dest_handle, 'message': message})
        client.sendto(request.encode(), self.server_address)
        # print(f"[To {dest_handle}]: {message}")  # handled in receive() thread

    def do_all(self, arg: str) -> None:
        """    Send a message to all clients (incl. unregistered ones)\n    Syntax: /all <message>"""

        # Basic error checking
        if not arg:
            print("Error: No message passed in command")
            return

        # Command specific error checking
        if not self.server_address:
            # This being the 2nd error check is okay
            print("Error: Not connected to server. Use '/join <ip> <port>'")
            return

        message = arg   

        # Send data
        request = json.dumps({'command': 'all', 'message': message})
        client.sendto(request.encode(), self.server_address)

    def do_help(self, arg: str) -> bool | None:
        if not arg:
            names = self.get_names()
            names.sort()
            for name in names:
                if name[:3] == 'do_':
                    if getattr(self, name).__doc__:
                        print(f"\n{name[3:]}\n{getattr(self, name).__doc__}")
            print()
        else:
            return super().do_help(arg)

    # This is necessary because CTRL+C will not interrupt recvfrom() at least on Windows.
    def do_quit(self, arg: None) -> None:  # This is necessary 
        # close socket
        client.close()
        
        # TODO: gracefully handle thread exit

        # exit program
        sys.exit()

 
# t = threading.Thread(target=receive)
# t.start()
MBSClientShell().cmdloop()
