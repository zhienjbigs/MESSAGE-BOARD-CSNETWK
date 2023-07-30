
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
