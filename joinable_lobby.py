import socket
from struct import Struct
from typing import Tuple, Optional

from connect_four import Player
from game_connection import GameConnection
from network_settings import (JOINING_TIMEOUT, LOBBY_STRUCT,
                              NAME_ENCODING, NAME_ERRORS)


class JoinableLobby:
    """Contains information about a lobby and how to join it."""

    def __init__(self,
                 ip_address: str,
                 port: int,
                 lobby_name: str,
                 host_name: str,
                 rows: int = 6,
                 columns: int = 7,
                 connect_n: int = 4) -> None:
        """
        Creates a lobby that can be joined.

        :param ip_address: The IP address of the lobbies host.
        :param port: The port of the lobbies host.
        :param lobby_name: The name of the lobby.
        :param host_name: The username of the host.
        :param rows: The number of rows for Connect 4.
        :param columns: The number of columns for Connect 4.
        :param connect_n: How many tiles in a row to win for Connect 4.
        """
        self.ip_address: str = ip_address
        self.port: int = port
        self.lobby_name: str = lobby_name
        self.host_name: str = host_name
        self.rows: int = rows
        self.columns: int = columns
        self.connect_n: int = connect_n

    def address(self) -> Tuple[str, int]:
        """
        Returns the address tuple.
        :return: The address tuple.
        """
        return self.ip_address, self.port

    def join(self,
             username: str,
             timeout: float = JOINING_TIMEOUT) -> Optional[GameConnection]:
        """
        Joins the lobby.
        :param timeout: How long to wait for the connection to succeed.
        :return: The GameConnection connected to the host,
                 or None if the connection failed or timed out.
        """
        game_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        game_socket.settimeout(timeout)
        try:
            game_socket.connect(self.address())
            return GameConnection(
                game_socket, Player.TWO, username, self.host_name)
        except TimeoutError:
            return None

    def serialize(self,
                  packing_struct: Struct = LOBBY_STRUCT,
                  encoding: str = NAME_ENCODING,
                  errors: str = NAME_ERRORS) -> bytes:
        """
        Serializes the object to bytes.

        This should be used before sending the object across the network.

        :param packing_struct: The Struct to pack the object with.
        :param encoding: The encoding to use for lobby_name and host_name.
        :param errors: The errors used when encoding lobby_name and host_name.
        :return: The bytes object that represents the object.
        """
        # Encode lobby_name and host_name
        lobby_name_bytes = self.lobby_name.encode(encoding, errors)
        host_name_bytes = self.host_name.encode(encoding, errors)
        # Pack everything in a string of bytes
        return packing_struct.pack(
            self.port, lobby_name_bytes, host_name_bytes,
            self.rows, self.columns, self.connect_n
        )

    @staticmethod
    def deserialize(ip_address: str,
                    source: bytes,
                    packing_struct: Struct = LOBBY_STRUCT,
                    encoding: str = NAME_ENCODING,
                    errors: str = NAME_ERRORS) -> 'JoinableLobby':
        """
        Deserializes the object from bytes.

        This should be used to reconstruct the object after receiving it from
        across the network.

        :param ip_address: The IP address of the lobbies host.
        :param source: The bytes to deserialize.
        :param packing_struct: The Struct to unpack the bytes with.
        :param encoding: The encoding used for lobby_name and host_name.
        :param errors: The errors used when encoding lobby_name and host_name.
        :return: The object that the bytes represented.
        """
        # Unpack the string of bytes
        unpacked_items = packing_struct.unpack(source)
        port = unpacked_items[0]
        lobby_name_bytes = unpacked_items[1]
        host_name_bytes = unpacked_items[2]
        rows = unpacked_items[3]
        columns = unpacked_items[4]
        connect_n = unpacked_items[5]
        # Decode lobby_name and host_name
        # strip to remove padding bytes from packing/unpacking
        lobby_name = lobby_name_bytes.decode(encoding, errors).rstrip('\x00')
        host_name = host_name_bytes.decode(encoding, errors).rstrip('\x00')
        # Create and return the joinable lobby object
        return JoinableLobby(
            ip_address, port, lobby_name, host_name,
            rows, columns, connect_n
        )
