class Header:
    def __init__(self, source : int, destination : int, sequence : int, window_size : int = 0, is_ack : bool = False):
        self.source = source
        self.destination = destination
        self.is_ack = is_ack
        self.sequence = sequence
        self.window_size = window_size if not is_ack else -1
        