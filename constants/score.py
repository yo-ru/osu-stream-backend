from enum import IntEnum


class SubmissionResponse(IntEnum):
    SUCCESS = 3
    SUCCESS_HIGHSCORE = 4
    INVALID_HASH = 5
