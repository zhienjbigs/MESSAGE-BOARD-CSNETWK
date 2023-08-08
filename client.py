import json
import random
import socket
import sys
import threading
from cmd import Cmd
from typing import Union
from rich.panel import Panel
from rich.theme import Theme
from rich.console import Console
from rich.markdown import Markdown

# Create a UDP socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.settimeout(0.2)
username = None

# Create objects for rich customization
customTheme = Theme({'success': 'green', 'error': 'red', 'prompt': 'yellow'})
console = Console(theme=customTheme)

# Technically, this is not necessary for client but recvfrom() will complain without it.
# The program has functionality for user data persistence, meaning that if the server remained up and you ran the program and ended up with the same user port, you would be able to use the same registered user that is bound to the client.
client.bind(('localhost', random.randint(8000, 9000)))
# client.bind(('localhost', 8888))



# The intro is done outside since rich cannot render markdown within classes for some reason
intro = """
# Welcome to the Umi's Message Board System

- Type /help or /? to show a list of commands
- Type /quit to exit the program

"""

console.clear()
console.print(Panel(Markdown(f"{intro}",justify='center',style='light_pink1')),style='plum1',end="\n",height=9)
# console.print(mk,soft_wrap=False, style='light_pink1', end="", justify='center')
console.print("")

class userClient(Cmd):
    
    prompt = ''
    
    # intro = '\nWelcome to the CSNETWK Message Board System.\nType /help or /? to list commands.\n\nTo exit the program, enter /quit.\n'

    server_address = ()
    
    # Normally, recvfrom() is expected to be after sendto().
    # However, because we may receive messages at any time, not just after sending data, we need to run it in a separate thread.
    # That's because recvfrom() is blocking. If we run it in the main thread, the program will not be able to accept user input.
    def _receive(self):
        while True:
            # Note: Modifying outside variables in this thread may not be thread-safe.
            # print('waiting to receive message')
            
            try:
                data, address = client.recvfrom(1024)
            except TimeoutError:
                continue
            except EnvironmentError:
                return userClient()
            
            # print('received %s bytes from %s' % (len(data), address))
            # print(data.decode())

            # Expect JSON
            response = json.loads(data.decode())

            # print(response)

            # Error and information
            if response['command'] == 'error':
                console.print(f"Error: {response['message']}",style='error')
                continue
            elif response['command'] == 'check_conn':
                pass
            elif response['command'] == 'info':
                console.print(response['message'])
                continue
            elif response['command'] == 'sendSuccess':
                console.print(Panel(f"[yellow]{response['message']}",title=f"[To] {response['src']}",title_align='left',border_style='bright_cyan'))
                continue
            elif response['command'] == 'forceExit':
                return userClient()
                
            
            # Process receive chain of the commands
            if response['command'] == 'msg':
                console.print(Panel(f"[yellow]{response['message']}[/]",title=f"[FROM][light_pink1]{response['handle']}",title_align='left',border_style='light_pink1'))
            elif response['command'] == 'all':
                console.print(Panel(f"[yellow]{response['message']}[/]",title=f"[GLOBAL][light_steel_blue]{response['handle']}",title_align='left',border_style='light_steel_blue'))

    def validate_command(self, command_args: str, requierror_arg_count: int) -> Union[bool, list]:
        split = command_args.split(maxsplit=1)
        if not split:
            console.print("Error: No arguments passed in command", style='error')
            return False
        elif len(split) != requierror_arg_count:
            console.print("Error: Invalid number of arguments", style='error')
            return False

        return split
    
    def reverse_valcommand(self, command_args: str, requierror_arg_count: int) -> Union[bool, list]: #this is a separate checker that ignores maxsplit limits for command only validation
        split = command_args.split(maxsplit=-1)
        if (len(split) != requierror_arg_count):
            console.print("Error: Invalid number of arguments", style='error')
            return False
        return split
            

    def precmd(self, line: str) -> str:
        if line:
            if line[0] == '/':
                line = line[1:]
            else:
                console.print("Error: Command must start with '/'", style='error')
                line = ''

        return super().precmd(line)

    def emptyline(self) -> None:
        # https://docs.python.org/3/library/cmd.html#cmd.Cmd.emptyline
        # Do not repeat last command when user presses enter with no input
        pass
    
    def do_join(self, arg: str) -> None:
        """    [grey37]Join a Message Board Server[/]\n    [green]Syntax: /join <ip> <port>"""

        # Basic error checking
        args = self.validate_command(arg, 2)
        if not args:
            return
        
        try:
            self.server_address = (args[0], int(args[1]))
        except ValueError:
            console.print("Error: Invalid port number", style='error')
            return

        try:
            request = json.dumps({'command': 'join'})
            client.sendto(request.encode(), self.server_address)
        except EnvironmentError:
            console.print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", style='error')
        except OverflowError:
            console.print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", style='error')

        # try:
        #     request = json.dumps({'command': 'join'})
        #     client.sendto(request.encode(), self.server_address)
        # except ConnectionResetError:
        #     self.server_address = ()
        #     console.print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", style='error')
        #     return
        
        # check if you are already connected to the server // tried a method by checking this on the server side
        # try:
        #     request = json.dumps({'command': 'join'})
        #     client.sendto(request.encode(), self.server_address)
        # except ConnectionError:
        #     console.print("Error: Already connected to the server", style='error')
        #     return

        # Command specific error checking
        # if (self.server_address) :
        #     console.print("Error: Already connected to server", style='error')
        #     return            

        # Listens for any responses from the server, would timeout if it wouldn't receive anything

        
        # console.print('Connection to the Message Board Server is successful!')
        try:
            data, _ = client.recvfrom(1024)
        except TimeoutError:
            return userClient # calls the class and restarts closing all dead threads
        except ConnectionResetError:
            # self.server_address = ()
            console.print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.", style='error')
            self.server_address = (args[0], int(args[1]))
            return
        self.server_address = (args[0], int(args[1]))
        response = json.loads(data.decode())
        info = response.get('message')
        console.print(f"{info}\n")

        
        # Checks if your username is already bound to your address on the server, so joining a different message board would ask you to register again
        if (username != None):
            console.print("Prompt: You are already registered in the server", style='prompt')

        t = threading.Thread(target=self._receive)
        t.start()
        print(self.server_address)

    def do_leave(self, arg: None) -> None:
        """    [grey37]Leave the Message Board Server[/]\n    [green]Syntax: /leave"""

        args = self.reverse_valcommand(arg, 0)
        if (args is False):
            return
        
        # Command specific error checking
        if not self.server_address:
            console.print("Error: Not connected to a server.", style='error')
            return

        # Send data
        
        request = json.dumps({'command': 'leave'})
        client.sendto(request.encode(), self.server_address)

        self.server_address = ()

        # TODO: Stop the thread

    def do_register(self, arg: str) -> None:
        """    [grey37]Register a handle with the Message Board Server[/]\n    [green]Syntax: /register <handle>"""

        args = self.reverse_valcommand(arg, 1)
        if not args:
            return

        # Basic error checking
        if not arg:
            console.print("Error: No handle/alias passed in command", style='error')
            return

        # Command specific error checking
        if not self.server_address:
            console.print("Error: Not connected to server. Use '/join <ip> <port>'",style='error')
            return

        # Send data
        request = json.dumps({'command': 'register', 'handle': arg})
        username = arg
        client.sendto(request.encode(), self.server_address)

    def do_list(self, arg: None) -> None:
        """    [grey37]List all handles registed with the Message Board Server[/]\n   [green]Syntax: /list"""

        # Command specific error checking
        if not self.server_address:
            console.print("Error: Not connected to server. Use '/join <ip> <port>'", style='error')
            return

        # Send data
        request = json.dumps({'command': 'list'})
        client.sendto(request.encode(), self.server_address)

    def do_msg(self, arg: str) -> None:
        """    [grey37]Send a message to a specific handle[/]\n    [green]Syntax: /msg <handle> <message>"""

        # Basic error checking
        args = self.validate_command(arg, 2)
        if not args:
            return

        # Command specific error checking
        if not self.server_address:
            # This being the 2nd error check is okay
            console.print("Error: Not connected to server. Use '/join <ip> <port>'",style='error')
            return

        dest_handle, message = args[0], args[1]            

        # Send data
        request = json.dumps({'command': 'msg', 'handle': dest_handle, 'message': message})
        client.sendto(request.encode(), self.server_address)
        # console.print(f"[To {dest_handle}]: {message}")  # handled in receive() thread

    def do_all(self, arg: str) -> None:
        """    [grey37]Send a message to all clients (incl. unregisted ones)[/]\n    [green]Syntax: /all <message>"""

        # Basic error checking
        if not arg:
            console.print("Error: No message passed in command",style='error')
            return

        # Command specific error checking
        if not self.server_address:
            # This being the 2nd error check is okay
            console.print("Error: Not connected to server. Use '/join <ip> <port>'",style='error')
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
                        console.print(Panel(f"\n{getattr(self, name).__doc__}\n",title=f'[green]{name}',border_style='light_pink1'))
            console.print()
        else:
            return super().do_help(arg)

    # This is necessary because CTRL+C will not interrupt recvfrom() at least on Windows.
    def do_quit(self, arg: None) -> None:  # This is necessary 
        # close socket
        client.close()
        
        # TODO: gracefully handle thread exit

        # exit program
        sys.exit()
userClient().cmdloop()
