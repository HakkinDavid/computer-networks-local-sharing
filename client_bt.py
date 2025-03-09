import bluetooth
import sys

server_mac = sys.argv[1] if len(sys.argv) > 1 else input("Enter server MAC address: ")
port = sys.argv[2] if len(sys.argv) > 2 else input("Enter server port: ")

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
client_sock.connect((server_mac, int(port)))
print("Connected to server")

while True:
    command = input("Enter command (LIST, DOWNLOAD <file>, UPLOAD <file>, EXIT): ")
    client_sock.send(command.encode())
    
    if command == "LIST":
        data = client_sock.recv(1024).decode()
        print("Files on server:\n" + data)
    elif command.startswith("DOWNLOAD "):
        filename = command.split(" ")[1]
        with open(filename, "wb") as f:
            f.write(client_sock.recv(1024))
        print("Download completed")
    elif command.startswith("UPLOAD "):
        filename = command.split(" ")[1]
        with open(filename, "rb") as f:
            client_sock.send(f.read())
        print("Upload completed")
    elif command == "EXIT":
        break

client_sock.close()
