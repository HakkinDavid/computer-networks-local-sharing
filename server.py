import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python client.py <PORT>")
    sys.exit(1)

# Configuración del servidor
HOST = '0.0.0.0'  # Escucha en todas las interfaces
PORT = int(sys.argv[1])
DIRECTORY = "server_files"  # Carpeta donde se guardarán los archivos

import os
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

def handle_client(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        if data == "LIST":
            files = "\n".join(os.listdir(DIRECTORY))
            conn.send(files.encode())
        elif data.startswith("DOWNLOAD "):
            filename = data.split(" ")[1]
            filepath = os.path.join(DIRECTORY, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    conn.sendall(f.read())
            else:
                conn.send(b"ERROR: File not found")
        elif data.startswith("UPLOAD "):
            filename = data.split(" ")[1]
            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, "wb") as f:
                f.write(conn.recv(1024))
            conn.send(b"UPLOAD SUCCESS")
        elif data == "EXIT":
            break
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    handle_client(conn)