import socket
from struct import Struct, pack, unpack
from typing import Optional

from connect_four import Player
from network_settings import (GAME_STRUCT, USERNAME_BYTES,
                              NAME_ENCODING, NAME_ERRORS)


class GameConnection:
    """Simplifies the process of playing Connect 4 across a network."""

    def __init__(self,
                 game_socket: socket.socket,
                 player: Player,
                 username: str,
                 opponent_username: str = '') -> None:
        """
        Wraps an existing socket to simplify the process of
        sending and receiving information to play a game of Connect 4.
        :param game_socket: The TCP socket already connected to your opponent.
        """
        game_socket.settimeout(None)
        self.game_socket: socket.socket = game_socket
        self.player: Player = player
        self.username: str = username
        self.opponent_username: str = opponent_username
        # Joining player, send username to the host.
        if self.opponent_username:
            self.send_username()
        # Hosting player, receive username from the joining player.
        else:
            self.opponent_username = self.receive_username()

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

    def send_username(self,
                      username: Optional[str] = None,
                      bytes_length: int = USERNAME_BYTES,
                      encoding: str = NAME_ENCODING,
                      errors: str = NAME_ERRORS) -> None:
        if username is None:
            username = self.username
        username_bytes = username.encode(encoding, errors)
        data = pack(f'!{bytes_length}s', username_bytes)
        self.game_socket.send(data)

    def receive_username(self,
                         bytes_length: int = USERNAME_BYTES,
                         encoding: str = NAME_ENCODING,
                         errors: str = NAME_ERRORS) -> str:
        data = self.game_socket.recv(bytes_length)
        username_bytes = unpack(f'!{bytes_length}s', data)[0]
        username = username_bytes.decode(encoding, errors).rstrip('\x00')
        return username

    def disconnect(self) -> None:
        """Disconnects from the game."""
        self.game_socket.close()
