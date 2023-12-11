import socket
import struct
from typing import Optional

from accept_thread import AcceptThread
from game_connection import GameConnection
from joinable_lobby import JoinableLobby
from looping_thread import LoopingThread
from network_settings import ADVERTISING_ADDRESS, ADVERTISING_WAIT_TIME


class HostedLobby:
    def __init__(self, lobby_name: str, host_name: str) -> None:
        # Create the server socket.
        self.server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.server_socket.bind(('', 0))
        self.server_socket.listen(1)
        # Create the advertising socket.
        self.advertising_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        # self.advertising_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, struct.pack('!i', 5))
        # Create the lobby info that will be advertised.
        self.info = JoinableLobby('', self.server_socket.getsockname()[1], lobby_name, host_name)
        self.advertising_thread: Optional[LoopingThread] = None
        self.accepting_thread: Optional[AcceptThread] = None

    def start_advertising(self,
                          wait_time: float = ADVERTISING_WAIT_TIME) -> None:
        if self.advertising_thread:
            return
        self.advertising_thread = LoopingThread(target=self.advertise, wait=wait_time)
        self.advertising_thread.start()

    def stop_advertising(self) -> None:
        if self.advertising_thread is None:
            return
        self.advertising_thread.stop()
        self.advertising_thread = None

    def advertise(self) -> None:
        self.advertising_socket.sendto(self.info.serialize(), ADVERTISING_ADDRESS)

    def start_accepting(self) -> None:
        if self.accepting_thread:
            return
        self.accepting_thread = AcceptThread(self.server_socket)
        self.accepting_thread.start()

    def stop_accepting(self) -> None:
        if self.accepting_thread is None:
            return
        self.accepting_thread.stop()
        self.accepting_thread = None

    def accepted_connection(self) -> Optional[GameConnection]:
        if not self.accepting_thread.connected():
            return None
        return GameConnection(self.accepting_thread.connected_socket)

    def close(self) -> None:
        self.stop_advertising()
        self.stop_accepting()
        self.server_socket.close()
        self.advertising_socket.close()


if __name__ == '__main__':
    lobby = HostedLobby('Lobby 2!', 'Other Person')
    print(lobby.info)
    lobby.start_advertising()
    lobby.stop_advertising()
    lobby.close()
