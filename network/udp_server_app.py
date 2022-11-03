import socket

server_port = 12000
server_socket = socket.socket(socket.AF_INET,
                              socket.SOCK_DGRAM  # UDP
                              )
server_socket.bind(('', server_port))
print("server is ready to receive")
while True:
    data, client_address = server_socket.recvfrom(
        2048)  # ? receive up to 2048 byte. recvfrom() returns data and client address
    message = data.decode("UTF-8")
    print(message)
    modified_message = message.upper()
    server_socket.sendto(modified_message.encode("UTF-8"),  # ? Data
                         client_address
                         )
