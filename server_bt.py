import bluetooth
import os

DIRECTORY = "server_files"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]
bluetooth.advertise_service(server_sock, "FileTransferServer",
                            service_classes=[bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE])

print(f"Bluetooth server listening on port {port}")

client_sock, client_info = server_sock.accept()
print(f"Accepted connection from {client_info}")

def handle_client(sock):
    while True:
        data = sock.recv(1024).decode()
        if not data:
            break
        if data == "LIST":
            files = "\n".join(os.listdir(DIRECTORY))
            sock.send(files.encode())
        elif data.startswith("DOWNLOAD "):
            filename = data.split(" ")[1]
            filepath = os.path.join(DIRECTORY, filename)
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    sock.sendall(f.read())
            else:
                sock.send(b"ERROR: File not found")
        elif data.startswith("UPLOAD "):
            filename = data.split(" ")[1]
            filepath = os.path.join(DIRECTORY, filename)
            with open(filepath, "wb") as f:
                f.write(sock.recv(1024))
            sock.send(b"UPLOAD SUCCESS")
        elif data == "EXIT":
            break
    sock.close()

handle_client(client_sock)
server_sock.close()
