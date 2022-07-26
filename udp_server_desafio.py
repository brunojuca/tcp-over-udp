from socket import *
import time
from random import seed, random

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("The server is ready to receive")

tempo = time.time()
buffer = []
count = 0
seed(1)
while True:
    subtract = time.time()
    diff = subtract - tempo

    if diff >= 30:        
        tempo = time.time()
        buffer = []
        count = 0

    print("Waiting...")

    message_1, clientAddress = serverSocket.recvfrom(2048)
    
    number = int(message_1.decode())
    
    buffer.append(number)
    count += 1

    if count == 10:
        message = "O buffer esta cheio!!!".encode()
        serverSocket.sendto(message, clientAddress)
        random_position = random()%10
        buffer[random_position] = number

    message= (f"Mensagem `{message_1.decode()}` recebida!")
    serverSocket.sendto(message.encode(), clientAddress)
