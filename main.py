from text_game import text_game
from text_lobby import text_lobby
from text_name import accept_username


def main():
    username = accept_username()
    game_connection = text_lobby(username)
    if not game_connection:
        return
    text_game(game_connection)


if __name__ == '__main__':
    main()
