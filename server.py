
import json
import socket

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
SERVER_ADDRESS = ('localhost', 9999)
print('starting up on %s port %s' % SERVER_ADDRESS)
server.bind(SERVER_ADDRESS)

clients = {}  # {address: handle}

while True:
    print('waiting to receive message')
    data, address = server.recvfrom(1024)
    
    print('received %s bytes from %s' % (len(data), address))
    print(data)
    
    # echo for debug
    # sent = server.sendto(data, address)
    # print('sent %s bytes back to %s' % (sent, address))

    # Resplies to commands
    try:
        data_json = json.loads(data.decode())
    except json.decoder.JSONDecodeError:  # Will also catch empty string (bytes)
        print('Error: Invalid JSON')
        continue
    # Every valid JSON input should have a 'command' key. We will not check for its presence.
    else:
        # Note: Do not specify command syntax in error messages. The server doesn't know how the client parses commands.
        if data_json['command'] == 'join':
            # update clients
            clients.update({address: None})
            print('clients:', clients)

            # inform sender of success
            reply = json.dumps({'command': 'info', 'message': 'Connection to the Message Board Server is successful! Please register.'})
            server.sendto(reply.encode(), address)

        elif data_json['command'] == 'leave':
            # broadcast to all clients
            reply = json.dumps({'command': 'info', 'message': f'{handle} left the chat'}).encode() #pre
            for client in clients:
                    server.sendto(reply, client)

 # update clients
            clients.pop(address)  # will remove regardless of whether handle is registered
            print('clients:', clients)

            # inform sender of success
            reply = json.dumps({'command': 'info', 'message': 'You have left the Message Board Server.'})
            server.sendto(reply.encode(), address)

        elif data_json['command'] == 'register':
            handle = data_json['handle']

            if clients.get(address) is not None:
                print('Error: Already registered')
                # inform sender of error
                reply = json.dumps({'command': 'error', 'message': 'Already registered.'})
                server.sendto(reply.encode(), address)
                continue

# check if handle already exists
			if handle in clients.values():
				print('Error: Handle already exists')
				# inform sender of error
				reply = json.dumps({'command': 'error', 'message': 'Registration failed. Handle is taken.'})
				server.sendto(reply.encode(), address)
				continue

 # update clients
            clients.update({address: handle})
            print('clients:', clients)

            # broadcast to all clients
            reply = json.dumps({'command': 'info', 'message': f'{handle} joined the chat'}).encode() #pre-encode reply
            for client_address in clients:
                server.sendto(reply, client_address) 

 # broadcast to all clients
            reply = json.dumps({'command': 'info', 'message': f'{handle} joined the chat'}).encode() #pre-encode reply
            for client_address in clients:
                server.sendto(reply, client_address) 

 # inform sender of success
            reply = json.dumps({'command': 'info', 'message': f"Welcome {handle}!"})
            server.sendto(reply.encode(), address)

# below this line, handle must be registered
# error check if not registered
	elif clients.get(address) is None:
		print('Error: Not registered')

# inform sender of error
			response = json.dumps({'command': 'error', 'message': 'Not registered.'})
			server.sendto(response.encode(), address)
			continue

		elif data_json['command'] == 'list':
