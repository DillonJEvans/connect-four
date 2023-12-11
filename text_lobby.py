from time import sleep
from typing import Collection, List, Optional

from game_connection import GameConnection
from joinable_lobby import JoinableLobby
from lobby_manager import LobbyManager
from network_settings import MAX_LOBBY_NAME_LENGTH, MAX_USERNAME_LENGTH, ADVERTISING_WAIT_TIME
from text_host import text_host
from text_name import is_valid_lobby_name, username_command


def text_lobby(username: str) -> Optional[GameConnection]:
    lobby_manager = LobbyManager()
    game_connection = None
    command = ''
    # Wait enough time for existing lobbies to advertise to us.
    print('Looking for lobbies...')
    sleep(ADVERTISING_WAIT_TIME + 0.1)
    while command != 'exit' and game_connection is None:
        lobbies = lobby_manager.get_lobbies()
        print('\n')
        print_lobbies(lobbies)
        print()
        print('Enter "help" for help.')
        user_input = input('command> ')
        command = user_input.strip().lower()
        # Join
        if is_command(command, 'join'):
            game_connection = join(command, lobbies, username)
        # Host
        elif is_command(command, 'host'):
            lobby_name = user_input[len('host') + 1:]
            if not lobby_name or is_valid_lobby_name(lobby_name):
                username, game_connection = text_host(
                    username, lobby_name
                )
        # Username
        elif is_command(command, 'username'):
            username = username_command(user_input, username)
        # Help
        elif is_command(command, 'help'):
            print()
            print_commands()
        # Refresh and Exit
        elif not command or is_command(command, 'refresh') or is_command(command, 'exit'):
            pass
        # Unknown
        else:
            print('Unknown command. Try entering "help" for a list of commands.')
    lobby_manager.close()
    return game_connection


def join(command: str,
         lobbies: List[JoinableLobby],
         username: str) -> Optional[GameConnection]:
    lobby_number = command[len('join') + 1:]
    # Make sure there is at least one lobby to join.
    if not lobbies:
        print('There are currently no lobbies to join.')
        return None
    # Check if a lobby number was provided.
    if not lobby_number:
        print('The "join" command needs to be followed by a lobby number.')
    # Make sure the lobby number is a number.
    try:
        lobby_number = int(lobby_number)
    except ValueError:
        print(f'{lobby_number} is not a lobby number.')
        return None
    # 0-index the lobby number.
    lobby_number -= 1
    # Make sure the provided lobby number is in range.
    if lobby_number < 0 or lobby_number >= len(lobbies):
        print(
            f'{lobby_number + 1} is not a valid lobby number. '
            f'Currently there are lobbies 1 to {len(lobbies)}.'
        )
        return None
    # Try and join the specified lobby.
    return lobbies[lobby_number].join(username)


def print_commands() -> None:
    print('refresh          =  Refreshes the list of lobbies.')
    print('join [n]         =  Joins the Nth lobby in the list.')
    print('host             =  Hosts a lobby.')
    print('username [name]  =  Changes your username.')
    print('help             =  Shows the different commands.')
    print('exit             =  Exits the game.')


def print_lobbies(lobbies: Collection[JoinableLobby]) -> None:
    if not lobbies:
        print('No lobbies were found nearby.')
        print('Use the "refresh" command to try again.')
        print('Use the "host" command to host your own lobby.')
        return
    lobby_number_len = len(str(len(lobbies)))
    lobby_name_len = max(map(len, (lobby.lobby_name for lobby in lobbies)))
    lobby_name_len = max(lobby_name_len, 5)
    host_name_len = max(map(len, (lobby.host_name for lobby in lobbies)))
    host_name_len = max(host_name_len, 4)
    print(
        f'{"#":>{lobby_number_len}} | '
        f'{"Lobby":<{lobby_name_len}} | '
        f'{"Host":<{host_name_len}} | '
        'Rows | Columns | Gamemode'
    )
    for lobby_number, lobby in enumerate(lobbies, 1):
        print_lobby(lobby_number, lobby, lobby_number_len, lobby_name_len, host_name_len)


def print_lobby(lobby_number: int,
                lobby: JoinableLobby,
                lobby_number_len: int = 1,
                lobby_name_len: int = MAX_LOBBY_NAME_LENGTH,
                host_name_len: int = MAX_USERNAME_LENGTH,
                rows_len: int = len('Rows'),
                columns_len: int = len('Columns')) -> None:
    print(
        f'{lobby_number:>{lobby_number_len}} | '
        f'{lobby.lobby_name:<{lobby_name_len}} | '
        f'{lobby.host_name:<{host_name_len}} | '
        f'{lobby.rows:>{rows_len}} | '
        f'{lobby.columns:>{columns_len}} | '
        f'Connect {lobby.connect_n}'
    )


def is_command(string: str, command: str):
    return string[:len(command)] == command
