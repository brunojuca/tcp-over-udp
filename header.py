class Header:
    def __init__(self, source : int, destination : int, seq_number : int, window_size : int = 0, is_ack : bool = False, end : bool = False):
        self.source = source
        self.destination = destination
        self.is_ack = is_ack
        self.seq_number = seq_number
        self.window_size = window_size #if not is_ack else -1
        self.end = end
        