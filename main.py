from text_lobby import text_lobby
from text_name import accept_username


def main():
    username = accept_username()
    game_connection = text_lobby(username)


if __name__ == '__main__':
    main()
