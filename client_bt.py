import bluetooth
import sys
import os

DIRECTORY = "files"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

server_mac = sys.argv[1] if len(sys.argv) > 1 else input("Enter server MAC address: ")
port = sys.argv[2] if len(sys.argv) > 2 else input("Enter server port: ")

try:
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.connect((server_mac, int(port)))
    print("Connected to server")

    while True:
        command = input("Enter command (LIST, DOWNLOAD <file>, UPLOAD <file>, EXIT): ")
        client_sock.send(command.encode())

        if command == "LIST":
            data = client_sock.recv(1024).decode()
            print("Files on server:" + data)
        elif command.startswith("DOWNLOAD "):
            filename = command.split(" ")[1]
            with open(os.path.join(DIRECTORY, filename), "wb") as f:
                while True:
                    chunk = client_sock.recv(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print("Download completed")
        elif command.startswith("UPLOAD "):
            filename = command.split(" ")[1]
            if os.path.exists(os.path.join(DIRECTORY, filename)):
                with open(os.path.join(DIRECTORY, filename), "rb") as f:
                    while chunk := f.read(1024):
                        client_sock.send(chunk)
                print("Upload completed")
            else:
                print("File not found")
        elif command == "EXIT":
            break

except Exception as e:
    print(f"Error: {e}")
finally:
    client_sock.close()
