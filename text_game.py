from connect_four import ConnectFour, Player
from game_connection import GameConnection


def text_game(game_connection: GameConnection) -> None:
    game = ConnectFour()
    # Main game loop.
    while not game.is_over():
        print()
        # Get the player's move and send it to your opponent.
        if game.turn == game_connection.player:
            print(f'Your turn! ({player_to_str(game.turn)})')
            print(game)
            column = input(f'Enter a column (1-{game.columns}): ')
            try:
                column = int(column)
            except ValueError:
                print('Please enter a column number.')
                continue
            column -= 1
            if column < 0 or column >= game.columns:
                print(f'The column must be between 1 and {game.columns}.')
                continue
            if not game.can_place(column):
                print(f'Column {column} is full.')
                continue
            game.place(column)
            game_connection.send_column(column)
        # Wait for your opponent's move.
        else:
            print(
                f'{game_connection.opponent_username}\'s turn. '
                f'({player_to_str(game.turn)})'
            )
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
    elif winner == game_connection.player:
        print('You won!')
    else:
        print('You lost.')
    game_connection.disconnect()


def player_to_str(player: Player):
    if player == Player.ONE:
        return 'O'
    elif player == Player.TWO:
        return 'X'
    return ' '
