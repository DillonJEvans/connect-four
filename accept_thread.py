import socket
from select import select
from threading import Event, Thread


class AcceptThread:
    def __init__(self, listening_socket: socket.socket) -> None:
        self.listening_socket = listening_socket
        self.thread = Thread(target=self.run)
        self.stop_event = Event()
        self.connected_socket = None

    def start(self) -> None:
        self.thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.thread.join()

    def is_stopped(self) -> bool:
        return self.stop_event.is_set()

    def connected(self) -> bool:
        return self.connected_socket is not None

    def run(self) -> None:
        ready = []
        while not self.is_stopped() and not ready:
            ready = select([self.listening_socket], [], [], 0)[0]
        if not ready:
            return
        self.connected_socket = self.listening_socket.accept()[0]
        self.stop_event.set()
