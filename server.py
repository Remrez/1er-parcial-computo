import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
icons = []
lock = threading.Lock()      #Lock para los arreglos

def broadcast(message):
    with lock:
        targets = list(clients)   
    for c in targets:
        try:
            c.send(message)
        except Exception:
            pass   

def handle(client):
    while True:
        try:
            message = client.recv(2048)
            if not message:          
                raise ConnectionResetError
            broadcast(message)
        except Exception:
            with lock:
                if client in clients:
                    index = clients.index(client)
                    nickname = nicknames[index]
                    icon = icons[index]
                    clients.pop(index)
                    nicknames.pop(index)
                    icons.pop(index)
                else:
                    return   
            try:
                client.close()
            except Exception:
                pass
            broadcast(f'[ICON:{icon}]{nickname} dejo el chat.'.encode('utf-8'))
            print(f'{nickname} desconectado.')
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado con {str(address)}")

        client.send("NICK".encode('ascii'))
        raw = client.recv(1024).decode('utf-8')

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