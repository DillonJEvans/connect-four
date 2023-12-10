import socket
from struct import Struct

from network_settings import GAME_STRUCT


class GameConnection:
    """Simplifies the process of playing Connect 4 across a network."""

    def __init__(self, game_socket: socket.socket) -> None:
        """
        Wraps an existing socket to simplify the process of
        sending and receiving information to play a game of Connect 4.
        :param game_socket: The TCP socket already connected to your opponent.
        """
        self.game_socket: socket.socket = game_socket

    def send_column(self,
                    column: int,
                    packing_struct: Struct = GAME_STRUCT) -> None:
        """
        Sends the column you placed your tile in to your opponent.
        :param column: The column where your tile was placed.
        :param packing_struct: The Struct to pack the column with.
        """
        data = packing_struct.pack(column)
        self.game_socket.send(data)

    def receive_column(self, packing_struct: Struct = GAME_STRUCT) -> int:
        """
        Receives the column that your opponent placed their tile in.
        :param packing_struct: The Struct to unpack the received message with.
        :return: The column that your opponent placed their tile in.
        """
        data = self.game_socket.recv(packing_struct.size)
        return packing_struct.unpack(data)[0]

    def disconnect(self) -> None:
        """Disconnects from the game."""
        self.game_socket.close()
