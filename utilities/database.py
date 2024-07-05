import databases

import settings
from utilities.logging import Ansi, log

DATABASE = databases.Database(settings.DB_DSN)


async def check_alive():
    try:
        await DATABASE.connect()
        await DATABASE.disconnect()
        return True
    except Exception as e:
        return False


CRASHES_COLUMNS = ["id", "device", "version", "exception"]
PLAYER_COLUMNS = ["id", "username", "username_safe", "hash", "device_id", "device_type"]
SCORES_COLUMNS = [
    "id",
    "player_id",
    "_date",  # NOTE: 'date' is a reserved keyword in SQL
    "guest",
    "_rank",  # NOTE: 'rank' is a reserved keyword in SQL
    "count_300",
    "count_100",
    "count_50",
    "count_miss",
    "max_combo",
    "spinner_bonus_score",
    "combo_bonus_score",
    "accuracy_bonus_score",
    "hit_score",
    "difficulty",
    "hit_offset",
    "filename",
    "hash",
]


async def check_structure():
    async with DATABASE as db:
        for table in ["crashes", "players", "scores"]:
            if table == "crashes":
                columns = CRASHES_COLUMNS
            elif table == "players":
                columns = PLAYER_COLUMNS
            elif table == "scores":
                columns = SCORES_COLUMNS

            try:
                await db.execute(f"SELECT {', '.join(columns)} FROM {table} LIMIT 1")
            except Exception as e:
                return False
        return True
