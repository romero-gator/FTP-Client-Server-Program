import socket
import os

HEADER = 64
FORMAT = 'utf-8'
BUFFER = 1024
PORT = 4007
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendmsg(message):
    message = message.encode(FORMAT)
    messageLen = len(message)
    sendLen = str(messageLen).encode(FORMAT)
    sendLen += b' ' * (HEADER - len(sendLen))
    client.send(sendLen)
    client.send(message)

def connect():
    print("Attempting to connect to the server...")
    try:
        client.connect(ADDRESS)
        print("Connection successful")
    except:
        print("Connection unsuccessful")

def upload(file_name):
    print(f"Uploading {file_name}")
    try:
        content = open(file_name, "rb")
    except:
        print("Error opening file")
        return

    try:
        sendmsg("upload")
    except:
        print("Server request for upload failed")
        return

    try:
        sendmsg(file_name)
        sendmsg(str(os.path.getsize(file_name)))
    except:
        print("Error sending the file details")

    try:
        data = content.read(BUFFER)
        print("Sending file contents...")
        while data:
            client.send(data)
            data = content.read(BUFFER)
        content.close()
        print("File sent")
    except:
        print("Error sending file")
        return
    
    return

def download(file_name):
    print(f"Downloading {file_name}")
    try:
        sendmsg("get")
    except:
        print("Server request for download failed")
        return
    
    try:
        sendmsg(file_name)
        check_size = client.recv(HEADER).decode(FORMAT)
        check = client.recv(int(check_size)).decode(FORMAT)
        if check == "invalid":
            print("Invalid file")
            return
    except:
        print("Error checking file")

    try:
        file_name = "new" + file_name
        file_size_size = client.recv(HEADER).decode(FORMAT)
        file_size = client.recv(int(file_size_size)).decode(FORMAT)
        file_size = int(file_size)

        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print("Recieving...")
        while bytes_recieved < file_size:
            data = client.recv(BUFFER)
            output_file.write(data)
            bytes_recieved += BUFFER
        output_file.close()
        print(f"Recieved file: {file_name}")
    except:
        print("Error downloading file")
        return

    return

def quit():
    sendmsg("quit")
    client.close()
    print("Connection ended")
    return


print("Welcome! Please choose from the following list of commands:\nconnect\nget <filename>\nupload <filename>\nquit")
while True:
    user_input = input("\nEnter a command: ")
    if user_input == "connect":
        connect()
    elif user_input[:6] == "upload":
        upload(user_input[7:])
    elif user_input[:3] == "get":
        download(user_input[4:])
    elif user_input == "quit":
        quit()
        break
    else:
        print("Command not recognized. Please try again.")