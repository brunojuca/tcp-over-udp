from header import Header

class Packet:
    def __init__(self, header : Header, size : int, payload : list):
        self.header = header
        self.size = size
        self.payload = payload
        