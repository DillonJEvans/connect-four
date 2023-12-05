import socket

import network_settings

from joinable_lobby import JoinableLobby


class HostedLobby:
    def __init__(self, lobby_name: str, host_name: str) -> None:
        self.info = JoinableLobby('', 0, lobby_name, host_name)
        addrinfo = socket.getaddrinfo(network_settings.ADVERTISING_HOST, None)[0]
        self.advertising_socket = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        # self.advertising_socket.bind((addrinfo[4][0], network_settings.ADVERTISING_PORT))

    def advertise(self) -> None:
        self.advertising_socket.sendto(self.info.serialize(), network_settings.ADVERTISING_ADDRESS)


from time import sleep

if __name__ == '__main__':
    lobby = HostedLobby('My Lobby!', 'Dillon')
    print(lobby.info)
    i = 1
    while True:
        print(f'Advertising {i}')
        i += 1
        lobby.advertise()
        sleep(1)
