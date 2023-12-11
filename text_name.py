from network_settings import (MAX_USERNAME_LENGTH, MAX_LOBBY_NAME_LENGTH,
                              NAME_ENCODING)


def accept_username() -> str:
    prompt = 'Please enter your desired username: '
    username = input(prompt)
    while not is_valid_username(username):
        username = input(prompt)
    return username


def accept_lobby_name() -> str:
    prompt = 'Lobby name: '
    lobby_name = input(prompt)
    while not is_valid_lobby_name(lobby_name):
        lobby_name = input(prompt)
    return lobby_name


def username_command(user_input: str, username: str) -> str:
    if user_input.lower() == 'username':
        print(f'Your username is "{username}".')
        return username
    new_username = user_input[len('username') + 1:]
    if is_valid_username(new_username):
        print(
            'Your username has been changed from '
            f'"{username}" to "{new_username}".'
        )
        username = new_username
    return username


def lobby_name_command(user_input: str, lobby_name: str) -> str:
    if user_input.lower() == 'lobby':
        print(f'The lobby name is "{lobby_name}".')
        return lobby_name
    new_lobby_name = user_input[len('lobby') + 1:]
    if is_valid_lobby_name(new_lobby_name):
        print(
            'The lobby name has been changed from '
            f'"{lobby_name}" to "{new_lobby_name}".'
        )
        lobby_name = new_lobby_name
    return lobby_name


def is_valid_username(username: str,
                      max_length: int = MAX_USERNAME_LENGTH,
                      encoding: str = NAME_ENCODING) -> bool:
    return is_valid_name(username, 'Your username', max_length, encoding)


def is_valid_lobby_name(lobby_name: str,
                        max_length: int = MAX_LOBBY_NAME_LENGTH,
                        encoding: str = NAME_ENCODING) -> bool:
    return is_valid_name(lobby_name, 'The lobby name', max_length, encoding)


def is_valid_name(name: str,
                  name_description: str,
                  max_length: int,
                  encoding: str = NAME_ENCODING) -> bool:
    # Check the length of the name.
    if len(name) > max_length:
        print(
            f'{name_description} cannot be more than '
            f'{max_length} characters long.'
        )
        return False
    # Check the encoding of the name.
    try:
        name.encode(encoding)
    except UnicodeError as e:
        print(
            f'{name_description} must contain only {encoding.upper()} characters. '
            f'{name[e.start]} is not a valid {encoding.upper()} character.'
        )
        return False
    return True
