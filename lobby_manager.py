import socket
from select import select

import network_settings

from joinable_lobby import JoinableLobby, PACKING_STRUCT

import struct


class LobbyManager:
    def __init__(self):
        # self.lobbies = []
        addrinfo = socket.getaddrinfo(network_settings.ADVERTISING_HOST, None)[0]
        self.listening_socket = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
        self.listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_socket.bind(('', network_settings.ADVERTISING_PORT))
        group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
        mreq = group_bin + struct.pack('@I', 0)
        self.listening_socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    def get_lobbies(self):
        readable, writeable, errorred = select([self.listening_socket], [], [])
        while readable:
            received, source = self.listening_socket.recvfrom(PACKING_STRUCT.size)
            lobby = JoinableLobby.deserialize(source[0], received)
            print(lobby)


if __name__ == '__main__':
    manager = LobbyManager()
    while True:
        manager.get_lobbies()
