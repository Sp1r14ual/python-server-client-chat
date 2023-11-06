import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2008
LISTENER_LIMIT = 10
active_clients = []

def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
        except:
            err_message = f"{username} disconnected" + "\n" + f"Active users: {len(active_clients) - 1}"
            print(err_message)
            send_messages_to_all(err_message)
            break

        if message:
            final_msg = username + '~' + message
            print(final_msg)
            send_messages_to_all(final_msg)
        else:
            print(f"Message from {username} is empty")

def send_message_to_client(client, message):
    client[1].sendall(message.encode())
        
def send_messages_to_all(message):
    broken = None
    for user in active_clients:
        try:
            send_message_to_client(user, message)
        except:
            broken = user
            continue

    if broken:       
        active_clients.pop(active_clients.index(broken))
                


def client_handler(client, address):
    while True:
        try:
            username = client.recv(2048).decode('utf-8')
        except: 
            err_message = "Guest failed to connect to server" + "\n" + f"Active users: {len(active_clients)}"
            print(err_message)
            send_messages_to_all(err_message)
            return

        if username:
            active_clients.append((username, client))
            prompt_message = f"SERVER~{username} (IP {address}) joined the chat" + "\n" + f"Active users: {len(active_clients)}"
            print(prompt_message)
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server.bind((HOST, PORT))
    print(f"Running the server on {HOST} {PORT}")
except:
    print(f"Unable to bind to host {HOST} and port {PORT}")
    exit(1)

server.listen(LISTENER_LIMIT)

while True:
    client, address = server.accept()
    print(f"Successfully connected to client {address[0]} {address[1]}")

    threading.Thread(target=client_handler, args=(client, address)).start()
