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
WINDOW_SIZE_REQUEST_CODE = "window_size"

def read_input(input_path : str):
    with open(input_path, "r") as f:
        lines = f.readlines()
        data_str = "".join(lines)
    
    return data_str

def calculate_n_packets(input_data : str):
    header_size = sys.getsizeof(Header(0, 0, 0, 0, False))
    input_size = sys.getsizeof(input_data)
    n_packets = math.ceil(input_size / (GREATER_PACKET_SIZE - header_size - 49)) # 49 is the size of the payload list empty
    return n_packets

def generate_buffer(input_data : str, window_size : int):
    buffer = []
    n_packets = calculate_n_packets(input_data)

    for i in range(n_packets):
        header = Header(SOURCE, DESTINATION, i, window_size)
        max_payload_size = GREATER_PACKET_SIZE - sys.getsizeof(header) - 49 # 49 is the size of the payload list empty
        payload = input_data[(i-1)*max_payload_size:i*max_payload_size] if i < n_packets-1 else input_data[(i-1)*max_payload_size:]
        packet_size = sys.getsizeof(payload) + sys.getsizeof(header)

        packet = Packet(header, packet_size, payload)
        buffer.append(packet)
    end_packet = Packet(Header(SOURCE, DESTINATION, n_packets, window_size, end = True), sys.getsizeof(header), "")
    buffer.append(end_packet)
    
    print(f"There are {n_packets} packets with 1024 bytes and a packet with {packet_size} bytes to be sent")

    return buffer

def ask_window_size():
    serverName = "localhost"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientSocket.sendto(WINDOW_SIZE_REQUEST_CODE.encode(), (serverName, serverPort))

    window_size_encoded, serverAddress = clientSocket.recvfrom(2048)
    window_size = int(window_size_encoded.decode())

    print(f"The receiver window size is: {window_size}")
    return window_size

def send_data(buffer : list, window_size : int):
    serverName = "localhost"
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    continue_option = False

    timeout = 0.1 # 1 second
    window_begin = 0 # The first packet to be sent in the pipeline
    window_end = window_begin + window_size # The last packet to be sent in the pipeline
    accumulative_ack = 0 # The last smallest ack received

    while True:   
        if window_begin == window_end:
            print("All packets were acked, stopping the process...")
            break

        # Sending all packets in the window through the pipeline
        print(f"Sending packets from {window_begin} to {window_end-1} that weren't acked yet")
        for packet_n in range(window_begin, window_end):           
            # Pickle the object and send it to the server
            packet_dumped = pickle.dumps(buffer[packet_n])
            clientSocket.sendto(packet_dumped, (serverName, serverPort))

            # Starting temporization
            if packet_n == window_begin:
                start_timer = time.time()

        while True:
            ack_dumped, serverAddress = clientSocket.recvfrom(2048)
            ack = pickle.loads(ack_dumped)
            print(f"ACK #{ack.header.seq_number} received")

            if ack.header.seq_number == accumulative_ack:
                accumulative_ack += 1
                #window_begin += 1
                #window_end += 1
                window_begin += ack.header.window_size
                window_end += ack.header.window_size

                print(f"Accumulative ACK increased to {accumulative_ack}")

                #if window_end-1 == len(buffer):
                if window_end > len(buffer):
                    window_end = len(buffer)

                break
            
            if not continue_option:
                option = input("")
                if option == "continue":
                    continue_option = True
            
            # Timeout verification
            current_time = time.time()
            if current_time - start_timer > timeout:
                break
        
    print("Closing socket...")
    clientSocket.close()

def main():
    parser = argparse.ArgumentParser(description="sender")
    parser.add_argument("--input_path", type=str, help="Input path", required=True)

    args = parser.parse_args()

    input_data = read_input(args.input_path)
    window_size = ask_window_size()
    buffer = generate_buffer(input_data, window_size)

    send_data(buffer, window_size)

if __name__ == "__main__":
    main()
    print("Done!")