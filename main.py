from connect_four import ConnectFour, Player


def player_to_str(player: Player):
    if player == Player.ONE:
        return 'O'
    elif player == Player.TWO:
        return 'X'
    return ' '


if __name__ == '__main__':
    game = ConnectFour()
    # Main game loop.
    while not game.is_over():
        print(f'Turn: {player_to_str(game.turn)} ({game.turn})')
        print(game)
        column = int(input('Enter a column (0-6): '))
        if not game.can_place(column):
            print(f'Column {column} is full.')
            continue
        game.place(column)
        print()
    # Print the final state of the game.
    print(game)
    # Print the winner.
    winner = game.winner()
    if winner == Player.ONE:
        print('Player 1 (O\'s) won!')
    elif winner == Player.TWO:
        print('Player 2 (X\'s) won!')
    else:
        print('The game ended in a draw.')