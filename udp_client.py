from socket import *

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input operation: ")
clientSocket.sendto(message.encode(), (serverName, serverPort))

#message = input("Input operation: ")
#clientSocket.sendto(message.encode(), (serverName, serverPort))

#message = input("Input second number: ")
#clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())
clientSocket.close()
