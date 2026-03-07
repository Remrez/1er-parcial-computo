import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
icons = []      # parallel list: icon index (0-4) per client

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(2048)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            icon = icons[index]
            broadcast(f'[ICON:{icon}]{nickname} dejo el chat.'.encode('utf-8'))
            nicknames.remove(nickname)
            icons.remove(icon)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado con {str(address)}")

        # Ask for NICK (client responds with "nickname|icon_index")
        client.send("NICK".encode('ascii'))
        raw = client.recv(1024).decode('utf-8')

        # Parse "nickname|icon_index"
        if '|' in raw:
            nickname, icon_str = raw.rsplit('|', 1)
            try:
                icon = int(icon_str)
            except ValueError:
                icon = 0
        else:
            nickname = raw
            icon = 0

        nicknames.append(nickname)
        icons.append(icon)
        clients.append(client)

        print(f'Usuario: {nickname}  Icono: {icon}')
        broadcast(f'[ICON:{icon}]{nickname} se unio al chat!'.encode('utf-8'))
        client.send('Conectado al servidor'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("El servidor esta andando")
receive()