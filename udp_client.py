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

GREATER_PACKET_SIZE = 1024 # The greater size of the packets is 1024 bytes

def read_input(input_path : str):
    with open(input_path, "r") as f:
        lines = f.readlines()
        data_str = "".join(lines)
    
    return data_str

def generate_buffer(input_data : str, window_size : int):
    buffer = []
    n_packets = math.ceil(sys.getsizeof(input_data)/GREATER_PACKET_SIZE) # The greater size of the packets is 1024 bytes

    for i in range(1, n_packets+1):
        input_data_interval = input_data[(i-1)*GREATER_PACKET_SIZE:i*GREATER_PACKET_SIZE]
        buffer.append(Packet(Header(0, 1, i, window_size), sys.getsizeof(input_data_interval), input_data_interval))

    return buffer

def send_data(buffer : list):
    serverName = "localhost"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    timeout = 1 # 1 second
    while True:
        start_timer = time.time()
        for window_begin, data in enumerate(buffer):
            window_end = window_begin + data.header.window_size
            clientSocket.sendto(data.encode(), (serverName, serverPort))

            current_time = time.time()
            if current_time - start_timer > timeout:
                break

            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

            print(modifiedMessage.decode())

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
    print(f"There are {len(buffer)-1} packets in the buffer with size 1024 bytes and 1 with size {sys.getsizeof(input_data)%GREATER_PACKET_SIZE} bytes")

    send_data(buffer)


if __name__ == "__main__":
    main()
    print("Done!")