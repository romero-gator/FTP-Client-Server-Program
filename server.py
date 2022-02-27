import socket
import os
import sys

HEADER = 64
FORMAT = 'utf-8'
BUFFER = 1024
PORT = 4007
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def sendmsg(message):
    message = message.encode(FORMAT)
    messageLen = len(message)
    sendLen = str(messageLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    connection.send(sendLen)
    connection.send(message)

def upload(connection):
    file_name_size = connection.recv(HEADER).decode(FORMAT)
    file_name = connection.recv(int(file_name_size)).decode(FORMAT)
    file_size_size = connection.recv(HEADER).decode(FORMAT)
    file_size = connection.recv(int(file_size_size)).decode(FORMAT)
    print(f"[{address}] Client uploading {file_name}")
    file_name = "new" + file_name
    file_size = int(file_size)

    output_file = open(file_name, "wb")
    bytes_recieved = 0
    print("Recieving...")
    while bytes_recieved < file_size:
        data = connection.recv(BUFFER)
        output_file.write(data)
        bytes_recieved += BUFFER
    output_file.close()
    print(f"Recieved file: {file_name}")
    return

def download(connection):
    file_name_size = connection.recv(HEADER).decode(FORMAT)
    file_name = connection.recv(int(file_name_size)).decode(FORMAT)
    print(f"[{address}] Client downloading {file_name}")

    if os.path.isfile(file_name):
        sendmsg("valid")
    else:
        print("Invalid file.")
        sendmsg("invalid")
        return

    sendmsg(str(os.path.getsize(file_name)))

    try:
        content = open(file_name, "rb")
        data = content.read(BUFFER)
        print("Sending file contents...")
        while data:
            connection.send(data)
            data = content.read(BUFFER)
        content.close()
        print("File sent")
    except:
        print("Error sending file.")
        return

    return

def quit(connection):
    print(f"[DISCONNECTING] Disconnected from {address}")
    connection.close()
    server.close()
    os.execl(sys.executable, sys.executable, *sys.argv)


print("[STARTING] Server is starting...")
server.listen()
print(f"[LISTENING] Server is listening on {SERVER}")       
connection, address = server.accept() 
print(f"[CONNECTING] Connection made to {address}")
connected = True
while connected:
    print("\nWaiting for instruction...")
    msg_len = connection.recv(HEADER).decode(FORMAT)
    if msg_len:
        msg_len = int(msg_len)
        msg = connection.recv(msg_len).decode(FORMAT)
        if msg == "quit":
            quit(connection)
            connected = False
        elif msg == "upload":
            upload(connection)
        elif msg == "get":
            download(connection)