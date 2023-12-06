import socket

from typing import Tuple

from connect_four import ConnectFour, Player
from game_connection import GameConnection


PORT: int = 1903


def main() -> None:
    game_socket, player = get_socket()
    game_connection = GameConnection(game_socket)
    game = ConnectFour()
    # Main game loop.
    while not game.is_over():
        print()
        # Get the player's move and send it to your opponent.
        if game.turn == player:
            print(f'Your turn! ({player_to_str(game.turn)})')
            print(game)
            column = int(input('Enter a column (0-6): '))
            if not game.can_place(column):
                print(f'Column {column} is full.')
                continue
            game.place(column)
            game_connection.send_column(column)
        # Wait for your opponent's move.
        else:
            print(f'Their turn. ({player_to_str(game.turn)})')
            print(game)
            print('Waiting for their move...')
            column = game_connection.receive_column()
            game.place(column)
    # Print the final state of the game.
    print()
    print(game)
    # Print the winner.
    winner = game.winner()
    if winner is None:
        print('THe game ended in a draw.')
    elif winner == player:
        print('You won!')
    else:
        print('You lost.')
    game_connection.disconnect()


def get_socket() -> Tuple[socket.socket, Player]:
    game_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    if input('1 for host, 2 for joining player: ') == '1':
        game_socket.bind(('', PORT))
        game_socket.listen(1)
        connection, address = game_socket.accept()
        game_socket.close()
        return connection, Player.ONE
    else:
        game_socket.connect(('localhost', PORT))
        return game_socket, Player.TWO


def player_to_str(player: Player):
    if player == Player.ONE:
        return 'O'
    elif player == Player.TWO:
        return 'X'
    return ' '


if __name__ == '__main__':
    main()
