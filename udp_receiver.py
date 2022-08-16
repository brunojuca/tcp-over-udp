from socket import *
from packet import *
import pickle
import numpy
import argparse

PACKET_LOSS_PROBABILITY = 0.2
ACK_SIZE = 1 # Byte
ACK_PAYLOAD = ""
WINDOW_SIZE_REQUEST_CODE = "window_size"

def packet_was_lost(probability : float):
    result_arr = (numpy.random.choice([0, 1], size=1, p=[1-probability, probability]) == 1)
    return result_arr[0]

def send_window_size(window_size : int, serverSocket : socket):
    message_encoded, clientAddress = serverSocket.recvfrom(2048)
    if message_encoded.decode() == WINDOW_SIZE_REQUEST_CODE:
        print("Sending window size...")
        serverSocket.sendto(f"{window_size}".encode(), clientAddress)

def recv_data(serverSocket, window_size):
    recv_data = ""

    print("The server is ready to receive")

    n_packets_encoded, clientAddress = serverSocket.recvfrom(2048)
    n_packets = int(n_packets_encoded.decode())

    nextseqnum = 0  # Next sequence number to be received
    
    free_space = window_size
    
    while True:
        packet_dumped, clientAddress = serverSocket.recvfrom(2048)
        packet = pickle.loads(packet_dumped)
        print("next seq num: ", nextseqnum)
        
        if not packet_was_lost(PACKET_LOSS_PROBABILITY):
            
            
            if packet.header.seq_number == nextseqnum:
                recv_data += packet.payload
                nextseqnum += 1
                free_space -= 1
                if free_space == 0:
                    free_space = window_size
                print(f"Packet #{packet.header.seq_number} received, sending ACK...")
                if packet.header.seq_number == n_packets - 1:
                    print("Reached end packet, breaking listening loop...")
                    ack = Packet(Header(packet.header.destination, packet.header.source, packet.header.seq_number, free_space, True), ACK_SIZE, ACK_PAYLOAD)
                    ack_dumped = pickle.dumps(ack)
                    serverSocket.sendto(ack_dumped, clientAddress)
                    break
            
            ack = Packet(Header(packet.header.destination, packet.header.source, packet.header.seq_number, free_space, True), ACK_SIZE, ACK_PAYLOAD)
            ack_dumped = pickle.dumps(ack)
            serverSocket.sendto(ack_dumped, clientAddress)
            
        else:
            print(f"Packet with sequence number {packet.header.seq_number} was lost")
            nack = Packet(Header(packet.header.destination, packet.header.source, -1, packet.header.window_size, True), 0, '')
            nack_dumped = pickle.dumps(nack)
            serverSocket.sendto(nack_dumped, clientAddress)

    end_ack = Packet(Header(packet.header.destination, packet.header.source, -2, packet.header.window_size, True), 0, '')
    end_ack_dumped = pickle.dumps(end_ack)
    serverSocket.sendto(end_ack_dumped, clientAddress)
    print("Closing socket...")
    serverSocket.close()

    return recv_data

def main():
    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(("", serverPort))

    parser = argparse.ArgumentParser(description="receiver")
    parser.add_argument("--window_size", type=int, help="Window size", required=True)

    args = parser.parse_args()

    window_size = args.window_size if args.window_size > 10 else 10
    print(f"Window size: {window_size}")
    
    # Waiting for the client to ask the window size
    send_window_size(window_size, serverSocket)

    recv_data_str = recv_data(serverSocket, window_size)

    print("Writing file...")
    with open("received_file.txt", "w") as file:
        file.write(recv_data_str)

if __name__ == "__main__":
    main()
    print("Done!")
