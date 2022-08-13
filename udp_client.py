"""
Example of usage:
    python3 udp_client.py --input_path defalt_input.txt --window_size 10
"""

from socket import *
import time
from packet import *
import argparse
import sys
import math
import pickle

GREATER_PACKET_SIZE = 1024 # The greater size of the packets is 1024 bytes
SOURCE = 0
DESTINATION = 1

def read_input(input_path : str):
    with open(input_path, "r") as f:
        lines = f.readlines()
        data_str = "".join(lines)
    
    return data_str

def calculate_n_packets(input_data : str):
    header_size = sys.getsizeof(Header(0, 0, 0, 0, False))
    input_size = sys.getsizeof(input_data)
    n_packets = math.ceil(input_size / (GREATER_PACKET_SIZE - header_size))
    return n_packets

def generate_buffer(input_data : str, window_size : int):
    buffer = []
    n_packets = calculate_n_packets(input_data)

    for i in range(1, n_packets+1):
        header = Header(SOURCE, DESTINATION, i, window_size)
        max_payload_size = GREATER_PACKET_SIZE - sys.getsizeof(header)
        payload = input_data[(i-1)*max_payload_size:i*max_payload_size]
        packet_size = sys.getsizeof(payload) + sys.getsizeof(header)
        print(packet_size)
        packet = Packet(header, packet_size, payload)
        buffer.append(packet)

    return buffer

def send_data(buffer : list, window_size : int):
    serverName = "localhost"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    timeout = 1 # 1 second
    window_begin = 0 # The first packet to be sent in the pipeline
    window_end = window_begin + window_size # The last packet to be sent in the pipeline
    accumulative_ack = -1 # The last smallest ack received
    while True:
        # Sending all packets in the window through the pipeline
        for packet_n in range(window_begin, window_end+1):
            # Pickle the object and send it to the server
            packet_dumped = pickle.dumps(buffer[packet_n])
            clientSocket.sendto(packet_dumped, (serverName, serverPort))

            # Starting temporization
            if packet_n == window_begin:
                start_timer = time.time()

        while True:
            ack_dumped, serverAddress = clientSocket.recvfrom(2048)
            ack = pickle.loads(ack_dumped)
            

            # Timeout verification
            current_time = time.time()
            if current_time - start_timer > timeout:
                break

        

    clientSocket.close()

    

def main():
    parser = argparse.ArgumentParser(description="main")
    parser.add_argument("--input_path", type=str, help="Input path", required=True)
    parser.add_argument("--window_size", type=int, help="Window size", required=True)

    args = parser.parse_args()

    window_size = args.window_size if args.window_size > 10 else 10
    print(f"Window size: {window_size}")

    input_data = read_input(args.input_path)
    buffer = generate_buffer(input_data, window_size)

    send_data(buffer, window_size)


if __name__ == "__main__":
    main()
    print("Done!")