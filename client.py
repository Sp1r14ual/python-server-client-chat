import socket
import threading

HOST = input("Server IP address: ")
PORT = 2008

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    try:
        client.connect((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")
        raise SystemExit

    username = input("Type username: ")
    if username:
        client.sendall(username.encode())
    else:
        print("Username can not be empty")
        

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

def send_message():
    message = input()
    if message:
        client.sendall(message.encode())
    else:
        print("Message can not be empty")

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
        except:
            print("Server stopped running")
            raise SystemExit

        if ("disconnected" in message) or ("failed" in message):
            print(message)
            continue
        if message:
            username = message.split("~")[0]
            content = message.split('~')[1]

            print(f"[{username}] {content}")
            
        else:
            print("Received message is empty")

connect()
while True:
    send_message()
