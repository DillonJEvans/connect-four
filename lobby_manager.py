import socket
import struct
import time
from select import select
from typing import Dict, List, Tuple

from joinable_lobby import JoinableLobby
from network_settings import (ADVERTISING_HOST, ADVERTISING_PORT,
                              LOBBY_STRUCT, LOBBY_TIMEOUT)


class LobbyManager:
    """Maintains a list of available lobbies."""

    def __init__(self) -> None:
        """Creates a LobbyManager with no lobbies."""
        self.lobbies: Dict[Tuple[str, int], TimedLobby] = {}
        # Create the socket.
        listening_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listening_socket.bind(('', ADVERTISING_PORT))
        # Join the multicast group.
        group = socket.inet_pton(
            socket.AF_INET6, ADVERTISING_HOST
        )
        multicast_request = group + struct.pack('!I', 0)
        listening_socket.setsockopt(
            socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, multicast_request
        )
        # Make the socket a data member.
        self.listening_socket: socket.socket = listening_socket

    def get_lobbies(self, timeout: float = LOBBY_TIMEOUT) -> List[JoinableLobby]:
        """
        A convenience method that calls receive_lobbies(),
        remove_timed_out_lobbies(), and then returns lobbies_list().
        :param timeout: The parameter for remove_timed_out_lobbies().
        :return: The updated list of available lobbies.
        """
        self.receive_lobbies()
        self.remove_timed_out_lobbies(timeout)
        return self.lobbies_list()

    def receive_lobbies(self) -> None:
        """
        Receives all incoming lobby messages,
        adding, updating, and removing lobbies accordingly.
        """
        # While there is a message available to the socket,
        # read it and either add, update, or remove a lobby.
        readable = select([self.listening_socket], [], [], 0)[0]
        while readable:
            received, sender = self.listening_socket.recvfrom(
                LOBBY_STRUCT.size
            )
            # The lobby has closed, remove it.
            if received[:2] == b'00':
                self.lobbies.pop(sender, None)
            # The lobby is still open, update or add it.
            else:
                lobby = JoinableLobby.deserialize(sender[0], received)
                self.lobbies[sender] = TimedLobby(lobby)
            readable = select([self.listening_socket], [], [], 0)[0]

    def remove_timed_out_lobbies(self, timeout: float = LOBBY_TIMEOUT) -> None:
        """
        Removes any lobbies that have timed out
        (have not received an update recently enough).
        :param timeout: How many seconds between updates before
                        a timeout is considered to have happened.
        """
        self.lobbies = {
            sender: lobby for sender, lobby in self.lobbies.items()
            if not lobby.has_timed_out(timeout)
        }

    def lobbies_list(self) -> List[JoinableLobby]:
        """
        Gets the list of available lobbies.
        :return: The list of available lobbies.
        """
        return [timed_lobby.lobby for timed_lobby in self.lobbies.values()]

    def close(self) -> None:
        """Closes the lobby manager."""
        self.listening_socket.close()


class TimedLobby:
    """A helper class for LobbyManager."""

    def __init__(self, lobby: JoinableLobby) -> None:
        """
        Creates what is effectively a tuple of the current time
        and the lobby given.
        :param lobby: The lobby.
        """
        self.time_received = time.monotonic()
        self.lobby = lobby

    def has_timed_out(self, timeout: float = LOBBY_TIMEOUT) -> bool:
        """
        Checks if the lobby has timed out.
        :param timeout: How many seconds between updates before
                        a timeout is considered to have happened.
        :return: True if the lobby has timed out, false otherwise.
        """
        return time.monotonic() - self.time_received > timeout


if __name__ == '__main__':
    manager = LobbyManager()
    lobbies = []
    while True:
        new_lobbies = manager.get_lobbies()
        if [lobby.address() for lobby in new_lobbies] != [lobby.address() for lobby in lobbies]:
            lobbies = new_lobbies
            print('New!')
            print('\n'.join(map(str, lobbies)))
            print()
