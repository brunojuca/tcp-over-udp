from socket import *
from struct import pack
from packet import *
import pickle
import numpy
import argparse

PACKET_LOSS_PROBABILITY = 0.0
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

    recv_data = ""

    print("The server is ready to receive")

    window_begin = 0 # The first packet to be sent in the pipeline
    window_end = window_begin + window_size # The last packet to be sent in the pipeline
    nextseqnum = 0  # Next sequence number to be received
    while True:
        packet_dumped, clientAddress = serverSocket.recvfrom(2048)
        packet = pickle.loads(packet_dumped)
        
        if not packet_was_lost(PACKET_LOSS_PROBABILITY):
            if packet.header.seq_number == nextseqnum:
                recv_data += packet.payload
                nextseqnum += 1
                print(f"Packet #{packet.header.seq_number} received, sending ACK...")
                ack = Packet(Header(packet.header.destination, packet.header.source, packet.header.seq_number, packet.header.window_size, True), ACK_SIZE, ACK_PAYLOAD)
                ack_dumped = pickle.dumps(ack)
                serverSocket.sendto(ack_dumped, clientAddress)
            if packet.header.end:
                print("Reached end packet, breaking listening loop...")
                break
        else:
            print(f"Packet with sequence number {packet.header.seq_number} was lost")
    
    print("Closing socket...")
    serverSocket.close()

    print("Writing file...")
    with open("received_file.txt", "w") as file:
        file.write(recv_data)

if __name__ == "__main__":
    main()
    print("Done!")