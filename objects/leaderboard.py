import urllib.parse as urlparse

import databases

import settings
from objects.score import Difficulty, Score


class Leaderboard:
    def __init__(self, data: str) -> None:
        _deviceId: str = data.split("&")[0].split("=")[1]
        self._filename: str = urlparse.unquote(
            data.split("&")[1].split("=")[1],
        ).replace(
            "+",
            " ",
        )
        self._period: int = int(
            data.split("&")[2].split("=")[1],
        )
        self._difficulty: Difficulty = Difficulty(
            int(data.split("&")[3].split("=")[1]),
        )

    async def to_stream(self) -> str:
        async with databases.Database(settings.DB_DSN) as db:
            scores = await db.fetch_all(
                "SELECT scores.*, players.username AS username FROM scores JOIN players ON scores.player_id = players.id WHERE filename = :filename AND difficulty = :difficulty LIMIT 100",
                {"filename": self._filename, "difficulty": self._difficulty},
            )

            if not scores:
                return ""

            # unpack scores into score objects; order by score.totalScore
            score_objects = [Score.from_row(score) for score in scores]
            score_objects = sorted(
                score_objects,
                key=lambda score: score.totalScore,
                reverse=True,
            )

            # format scores for osu!stream leaderboard
            leaderboard = ""
            for i, score in enumerate(score_objects):
                leaderboard += f"{score.to_leaderboard(scores[i]["username"], i + 1)}{"\n" if i < 99 else ""}"

            return leaderboard
