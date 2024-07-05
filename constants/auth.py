from enum import IntEnum


class AuthResponse(IntEnum):
    ALREADY_LINKED = 0
    CREDENTIAL_MISMATCH = 1
    SUCCESS = 2
