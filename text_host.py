from typing import Tuple, Optional

from game_connection import GameConnection
from hosted_lobby import HostedLobby
from text_name import accept_lobby_name


def text_host(username: str,
              lobby_name: str = '') -> Tuple[str, Optional[GameConnection]]:
    # Ask the user for a lobby name if one wasn't provided.
    if not lobby_name:
        lobby_name = accept_lobby_name()
    # Create the lobby.
    hosted_lobby = HostedLobby(lobby_name, username)
    hosted_lobby.start_advertising()
    hosted_lobby.start_accepting()
    # Wait for a connection.
    print('Waiting for a player to join...')
    hosted_lobby.accepting_thread.stop_event.wait()
    # Get the updated username and the new game connection.
    username = hosted_lobby.info.host_name
    game_connection = hosted_lobby.accepted_connection()
    # Cleanup and return.
    hosted_lobby.close()
    return username, game_connection
