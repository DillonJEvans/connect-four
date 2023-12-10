from struct import Struct
from typing import Tuple


"""Lobby settings"""

# How long usernames and lobby names can be.
# This isn't really a network setting, as it dictates how
# long names can be on user's local machines, however since
# those names will be transmitted over the network, it would
# be best to limit how long they can be before they are sent.
MAX_USERNAME_LENGTH: int = 32
MAX_LOBBY_NAME_LENGTH: int = 32

# How many bytes usernames and lobby names will be when sent over the network.
USERNAME_BYTES: int = 32
LOBBY_NAME_BYTES: int = 32

# Parameters for how usernames and lobby names will be encoded/decoded.
NAME_ENCODING = 'ascii'
NAME_ERRORS = 'ignore'

# The format that lobbies will be sent and received with.
#                   ! = Network (big) endian
#                   H = port       : unsigned short
# {LOBBY_NAME_BYTES}s = lobby_name : char[LOBBY_NAME_BYTES]
#   {USERNAME_BYTES}s = host_name  : char[USERNAME_BYTES]
#                   I = rows       : unsigned int
#                   I = columns    : unsigned int
#                   I = connect_n  : unsigned int
LOBBY_FORMAT: str = f'!H{LOBBY_NAME_BYTES}s{USERNAME_BYTES}sIII'
LOBBY_STRUCT: Struct = Struct(LOBBY_FORMAT)

# How many seconds without receiving an advertisement from a
# lobby before a listener will consider it to have timed out.
LOBBY_TIMEOUT: float = 5


"""Advertising Settings"""

# The IPv6 address that hosts advertise on (via multicast).
# ff00::/8  is the prefix for a multicast address.
# ff10::/12 is the prefix for a transient multicast address.
# ff15::/16 is the prefix for a transient site-local multicast address.
# The last 112-bits of the address are the group id (randomly generated).
ADVERTISING_HOST: str = 'ff15:2f3c:b5ab:1312:21cc:854d:a0bd:139e'

# The port number that hosts advertise on (randomly generated).
ADVERTISING_PORT: int = 18556

# The address (IPv6 address and port number) that hosts advertise on.
ADVERTISING_ADDRESS: Tuple[str, int] = (ADVERTISING_HOST, ADVERTISING_PORT)

# How many seconds that hosts will wait between advertising messages.
ADVERTISING_WAIT_TIME: float = 1


"""Joining settings"""

# How many seconds to wait before joining a lobby will fail.
JOINING_TIMEOUT: float = 5


"""Game settings"""

# The format that game messages (columns) will be sent and received with.
# ! = Network (big) endian
# I = column : unsigned int
GAME_FORMAT: str = f'!I'
GAME_STRUCT: Struct = Struct(GAME_FORMAT)
