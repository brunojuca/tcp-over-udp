from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("The server is ready to receive")

while True:
    print("Waiting...")

    message_1, clientAddress = serverSocket.recvfrom(2048)
    #message_2, clientAddress = serverSocket.recvfrom(2048)
    #message_3, clientAddress = serverSocket.recvfrom(2048)

    operation = str(message_1.decode())
    
    #first_number = eval(message_1.decode())
    #second_number = eval(message_3.decode())
    #operation = message_2.decode()
    #if operation == "+":
    #    result = first_number + second_number
    #elif operation == "-":
    #    result = first_number - second_number
    #elif operation == "*":
    #    result = first_number*second_number
    #else:
    #    result = first_number/second_number

    modifiedMessage = str(eval(operation))
    
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

    print("closing socket...")
    serverSocket.close()
