from socket import *
from packet import *

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    print("The server is ready to receive")

    while True:
        print("Waiting...")

        message_1, clientAddress = serverSocket.recvfrom(2048)

        operation = str(message_1.decode())
        
        modifiedMessage = str(eval(operation))
        
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)

        print("closing socket...")
        serverSocket.close()

if __name__ == "__main__":
    main()
    print("Done!")