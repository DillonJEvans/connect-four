from typing import Collection, Optional

from game_connection import GameConnection
from joinable_lobby import JoinableLobby, MAX_LOBBY_NAME_BYTES, MAX_USER_NAME_BYTES
from lobby_manager import LobbyManager


def text_lobby() -> Optional[GameConnection]:
    lobby_manager = LobbyManager()
    game_connection = None
    command = ''
    while command != 'exit' and game_connection is None:
        lobbies = lobby_manager.get_lobbies()
        print('\n')
        print_lobbies(lobbies)
        print()
        print('Enter "help" for help.')
        user_input = input('command> ')
        command = user_input.strip().lower()
        if command[:4] == 'join':
            try:
                lobby_number = int(command[4:])
                game_connection = lobbies[lobby_number].join()
            except:
                print('The "join" command needs to be followed by a lobby number.')
        elif command == 'host':
            pass
        elif command == 'help':
            print()
            print_commands()
        elif command == 'refresh' or command == 'exit':
            pass
        else:
            print('Unknown command. Try entering "help" for a list of commands.')
    lobby_manager.close()
    return game_connection


def print_commands() -> None:
    print('refresh  = Refreshes the list of lobbies.')
    print('join [n] = Joins the Nth lobby in the list.')
    print('host     = Hosts a lobby.')
    print('help     = Shows the different commands.')
    print('exit     = Exits the game.')


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
                lobby_name_len: int = MAX_LOBBY_NAME_BYTES,
                host_name_len: int = MAX_USER_NAME_BYTES,
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
