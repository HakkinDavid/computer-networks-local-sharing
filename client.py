import socket
import sys

if len(sys.argv) != 3:
    print("Usage: python client.py <HOST> <PORT>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    
    while True:
        command = input("Enter command (LIST, DOWNLOAD <file>, UPLOAD <file>, EXIT): ")
        client.send(command.encode())
        
        if command == "LIST":
            data = client.recv(1024).decode()
            print("Files on server:\n" + data)
        elif command.startswith("DOWNLOAD "):
            filename = command.split(" ")[1]
            with open(filename, "wb") as f:
                f.write(client.recv(1024))
            print("Download completed")
        elif command.startswith("UPLOAD "):
            filename = command.split(" ")[1]
            with open(filename, "rb") as f:
                client.sendall(f.read())
            print("Upload completed")
        elif command == "EXIT":
            break
    client.close()

if __name__ == "__main__":
    client()
