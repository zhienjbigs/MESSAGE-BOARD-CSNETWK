# Implement a UDP server
import json
import socket
import rich
from rich.theme import Theme
from rich.console import Console

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port

# for the interoperability test, you can run 2 instances of the same server by running a separate instance of the code itself but by having a different server address, to do this, simply uncomment one of the server addresses below and comment the other one, do not have them both uncommented at the same time for the sake of consistency.

# SERVER_ADDRESS = ('localhost', 8888)
# SERVER_ADDRESS = ('localhost', 9999) 
SERVER_ADDRESS = ('127.0.0.1', 12345)

# PS: in your code editor, press ALT + Z to wrap everything, this would make it easier for you to read long comments/syntaxes -inny

# localhost is essentially the abstraction of the call back address which is 127.0.0.1; it is essentially the assigned address of the host device, this is typically used to diagnose issues for large or small networks, since the server is hosted on the client device, in a real world scenario, pinging 127.0.0.1 would ping your own device.

# for documentation purposes, since this is not an actually connected to a network, the server cannot communicate with other devices hence why we are using UDP: remove this if you don't want this shown in the demo. :p  


print('starting up on %s port %s' % SERVER_ADDRESS)
server.bind(SERVER_ADDRESS)


# Create object from rich import for customization
# Objects that use rich modules
custom_theme = Theme({"success": "bold green", "error": "bold red"})
console = Console(theme=custom_theme)


# instatiate dict for clients
# saved clients name list
# this dict  would not be updated
clients = {}  # {address: handle}

# this dict would be updated
connClients = {}
# print = ('clients: ', clients)

while True:
	print('waiting to receive message')
	try:
		data, address = server.recvfrom(1024)
	except ConnectionResetError:
		continue
	
	print('received %s bytes from %s' % (len(data), address))
	print(data)
	
	# echo for debug
	# sent = server.sendto(data, address)
	# print('sent %s bytes back to %s' % (sent, address))

    # Responses to commands
	try:
		data_json = json.loads(data.decode())
	except json.decoder.JSONDecodeError:  # Will also catch empty string (bytes)
		console.print('Error: Invalid JSON', style="error")
		continue
	# Every valid JSON input should have a 'command' key. We will not check for its presence.
	else:
		# Note: Do not specify command syntax in error messages. The server doesn't know how the client parses commands.

		if data_json['command'] == 'join':
			# update clients
   			# for debug only
			# clients.update({address: None})
			# print('clients:', clients) 

			# TESTED USING RICH  FOR JSON

			# TEXT MODULE
			# connMsg = json.dumps(Text('Connection to the Message Board Server is successful! Please register.'))
			# connMsg.stylize("bod success", 0, 6)
   
			# CONSOLE API MODULE
			# inform sender of success
			# connMsg = console.print('Connection to the Message Board Server is successful! Please register', style="green bold")
			# convertedMsg = str(connMsg)
			# connMsg.stylize('bold green',0)
			
			# CONVERT TO JSON
   			# formatconnMsg = JSON(connMsg)
			# response = json.dumps({'command': 'info', 'message': connMsg})
   
			# PS: this method does not work because the rich module is not compatible with the socket module which handles the server and client side responses

			if (address in connClients.keys()):
				response = json.dumps({'command': 'info', 'message': f'[red]Already connected to the server.'})
			else:
				response = json.dumps({'command': 'info', 'message': f'[green]Connection to the Message Board Server is successful! Please register.'})
				server.sendto(response.encode(), address)
  
			if (clients.get(address) != None):
				# handle = list(clients.values()) # test
    	
     			# to cause an exception in the leave block, during the leave sequence the program attempts to get the handle of the user and if it returns an exception for the reason of not having a handle to begin with, the code returns an error message saying that there was an unregistered user that left the message board.
				connClients.update({address: clients[address]})
				response = json.dumps({'command': 'info', 'message': f'[green]Welcome back to the Message Board[/] [yellow]{clients[address]}'})
				server.sendto(response.encode(), address)
				response = json.dumps({'command': 'info', 'message': f'[yellow]{clients[address]}[/] [green]has rejoined the Message Board!'}).encode() #pre-encode response
				for client_address in clients:
					if (clients.get(address)):
						continue
					else:	
						server.sendto(response, client_address)
			# else:
			# 	response = json.dumps({'command': 'info', 'message': f'[green]Connection to the Message Board Server is successful! Please register.'})
			# 	server.sendto(response.encode(), address)
    
			print('connected clients:', connClients) 
			# for debugging | connClients is used for saved data, thus if the user rejoins the registered username for that address should be saved.
			print('clients:', clients)


		elif data_json['command'] == 'leave':
      
			# PS: An exception occurs when the user leaves without registering, this is because there is no NULL value placed in the JSON by default, so the client states that it is just undefined, this can be bypassed by placing a NULL for each modifier value in the json to instantiate the attributes.

      
			# broadcast to all clients

			# if (clients.get(handle) is not None):
			# 	response = json.dumps({'command': 'info', 'message': f'{handle} left the chat'}).encode() #pre
			# 	for client in clients:
			# 		server.sendto(response, client)
			
			# else:
			# 	response = json.dumps({'command': 'info', 'message': 'An unregistered user left the chat'}) #pre
			# 	for client in clients:
			# 			server.sendto(response.encode(), client)
			# 	continue
   
			# try:
			# 	response = json.dumps({'command': 'info', 'message': f'[grey37]{connClients[address]} left the chat'}).encode() #pre
			# 	for client in clients:
			# 		server.sendto(response, client)
			# except:
			# 	response = json.dumps({'command': 'info', 'message': '[grey37]An unregistered user left the chat'}) #pre
			# 	for client in clients:
			# 		server.sendto(response.encode(), client)
			# 		continue
 
 
			if (connClients[address] is not None):
				response = json.dumps({'command': 'info', 'message': f'[grey37]{handle} left the chat'}).encode() #pre
				for client in clients:
					server.sendto(response, client)
			else:
				response = json.dumps({'command': 'info', 'message': '[grey37]An unregistered user left the chat'}) #pre
				for client in clients:
					server.sendto(response.encode(), client)
					continue	
				
			# response = json.dumps({'command': 'info', 'message': f'{handle} left the chat'}).encode() #pre
			# for client in clients:
			# 	server.sendto(response, client)

			# update clients
			connClients.pop(address)  # will remove regardless of whether handle is registered
			print('conneted clients', connClients)
			print('clients:', clients)
   

			# debug clients list
			# print('client: ', clients)


			# inform sender of success
			response = json.dumps({'command': 'info', 'message': '[grey37]You have left the Message Board Server.'})
			server.sendto(response.encode(), address)
			response = json.dumps({'command': 'forceExit'})
			server.sendto(response.encode(), address)
			

		elif data_json['command'] == 'register':
			handle = data_json['handle']

			if clients.get(address) is not None:
				print('Error: Already registered')
				# inform sender of error
				response = json.dumps({'command': 'error', 'message': 'Already registered.'})
				server.sendto(response.encode(), address)
				continue

			# check if handle already exists
			if handle in clients.values():
				print('Error: Handle already exists')
				# inform sender of error
				response = json.dumps({'command': 'error', 'message': 'Registration failed. Handle is taken.'})
				server.sendto(response.encode(), address)
				continue

			# update clients
			clients.update({address: handle})
			connClients.update({address: handle})
			print('connected clients:' , connClients)
			print('clients:', clients)

			# broadcast to all clients
			response = json.dumps({'command': 'info', 'message': f'[light_pink1]{handle} joined the chat'}).encode() #pre-encode response
			for client_address in clients:
				server.sendto(response, client_address)

			# inform sender of success
			response = json.dumps({'command': 'info', 'message': f"[yellow1]Welcome[/][light_pink1] {handle}![/]"})
			server.sendto(response.encode(), address)

		# below this line, handle must be registered
		# error check if not registered
		elif clients.get(address) is None:
			print('Error: Not registered')
			# inform sender of error
			response = json.dumps({'command': 'error', 'message': 'Not registered.'})
			server.sendto(response.encode(), address)
			continue

		elif data_json['command'] == 'list':
			# get list of handles
			handle_list = list(clients.values())
			
			# send list of handles
			response = json.dumps({'command': 'info', 'message': f"[bright_cyan]List of users: {', '.join(handle_list)}"})
			server.sendto(response.encode(), address)

		elif data_json['command'] == 'msg':
			# Note: Allow the sender to send a message to themselves

			destination_handle = data_json['handle']
			print('destination_handle:', destination_handle)
			try:
				destination_addr = list(clients.keys())[list(clients.values()).index(destination_handle)]
			except ValueError:
				destination_addr = None
			print('destination_addr:', destination_addr)
			source_handle = clients.get(address)
			print('source_handle:', source_handle)

			# error check if handle exists
			if not destination_addr:
				print('Error: Invalid handle')
				# inform sender of error
				response = json.dumps({'command': 'error', 'message': 'Handle not found'})
				server.sendto(response.encode(), address)
				continue

			# change handle to source handle and send to destination
			data_json.update({'handle': source_handle})
			response = json.dumps(data_json)
			server.sendto(response.encode(), destination_addr)

			# inform sender of success
			response = json.dumps({'command': 'sendSuccess', 'src': f"[bright_cyan]{destination_handle}[/]",'message':f"[yellow]{data_json['message']}[/]"})
			server.sendto(response.encode(), address)
			
		elif data_json['command'] == 'all':
			# Note: Unlike 'msg' where the sender can only send to registered clients, 
			# 		'all' will the sender can send to all clients (including unregistered clients)
			#       This behavior is okay.

			print('destination_addr:', "ALL")
			source_handle = clients.get(address)
			print('source_handle:', source_handle)

			# change handle to source handle and send to All destinations
			data_json.update({'handle': source_handle})
			response = json.dumps(data_json).encode() #pre-encode response
			for client_address in clients:
				server.sendto(response, client_address)

			# sender was already informed of success in the above loop
