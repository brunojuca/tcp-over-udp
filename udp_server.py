from socket import *
from packet import *
import pickle
import numpy

ACK_SIZE = 1 # Byte
ACK_PAYLOAD = ""

def packet_was_lost(probability : float):
    result_arr = (numpy.random.choice([0, 1], size=1, p=[1-probability, probability]) == 1)
    return result_arr[0]

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("", serverPort))
    print("The server is ready to receive")

    while True:
        print("Waiting...")

        packet_dumped, clientAddress = serverSocket.recvfrom(2048)
        packet = pickle.loads(packet_dumped)
        
        if not packet_was_lost(0.0):
            ack = Packet(Header(packet.header.destination, packet.header.source, packet.header.seq_number, packet.header.window_size, True), ACK_SIZE, ACK_PAYLOAD)
            ack_dumped = pickle.dumps(ack)
            serverSocket.sendto(ack_dumped, clientAddress)
        else:
            print(f"Packet with sequence number {packet.header.seq_number} was lost")
            
        print("closing socket...")
        serverSocket.close()

if __name__ == "__main__":
    main()
    print("Done!")