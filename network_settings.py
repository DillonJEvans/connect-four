from typing import Tuple

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
