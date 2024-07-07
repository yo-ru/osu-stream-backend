import hashlib
import time
import urllib.parse as urlparse
from enum import Enum, IntEnum, unique

import databases

import settings


@unique
class Rank(Enum):
    N = 0
    D = 1
    C = 2
    B = 3
    A = 4
    S = 5
    SS = 6


@unique
class Difficulty(IntEnum):
    NONE = -1
    EASY = 0
    NORMAL = 1
    HARD = 2  # possibly unused
    EXPERT = 3


ACCURACY_BONUS_AMOUNT = 400000


class Score:
    def __init__(self) -> None:
        self._id: int = 0
        self._date: int = int(time.time())
        self._guest: bool = False
        self._rank: Rank = Rank.N
        self._count100: int = 0
        self._count300: int = 0
        self._count50: int = 0
        self._countMiss: int = 0
        self._maxCombo: int = 0
        self._spinnerBonusScore: int = 0
        self._comboBonusScore: int = 0
        self._hitScore: int = 0
        self._accuracyBonusScore: int = 0
        self._difficulty: Difficulty = Difficulty.NONE
        self._hitOffset: float = 0.0
        self._filename: str = ""
        self._hash: str = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value: int):
        self._date = value

    @property
    def guest(self):
        return self._guest

    @guest.setter
    def guest(self, value: bool):
        self._guest = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: Rank):
        self._rank = value

    @property
    def count100(self):
        return self._count100

    @count100.setter
    def count100(self, value: int):
        self._count100 = value

    @property
    def count300(self):
        return self._count300

    @count300.setter
    def count300(self, value: int):
        self._count300 = value

    @property
    def count50(self):
        return self._count50

    @count50.setter
    def count50(self, value: int):
        self._count50 = value

    @property
    def countMiss(self):
        return self._countMiss

    @countMiss.setter
    def countMiss(self, value: int):
        self._countMiss = value

    @property
    def maxCombo(self):
        return self._maxCombo

    @maxCombo.setter
    def maxCombo(self, value: int):
        self._maxCombo = value

    @property
    def spinnerBonusScore(self):
        return self._spinnerBonusScore

    @spinnerBonusScore.setter
    def spinnerBonusScore(self, value: int):
        self._spinnerBonusScore = value

    @property
    def comboBonusScore(self):
        return self._comboBonusScore

    @comboBonusScore.setter
    def comboBonusScore(self, value: int):
        self._comboBonusScore = value

    @property
    def hitScore(self):
        return self._hitScore

    @hitScore.setter
    def hitScore(self, value: int):
        self._hitScore = value

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value: Difficulty):
        self._difficulty = value

    @property
    def hitOffset(self):
        return self._hitOffset

    @hitOffset.setter
    def hitOffset(self, value: float):
        self._hitOffset = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value: str):
        self._filename = value

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value: str):
        self._hash = value

    @property
    def totalScore(self):
        return (
            self.spinnerBonusScore
            + self.hitScore
            + self.comboBonusScore
            + self.accuracyBonusScore
        )

    @property
    def accuracyBonusScore(self):
        return self._accuracyBonusScore

    @accuracyBonusScore.setter
    def accuracyBonusScore(self, value: int):
        self._accuracyBonusScore = value

    @property
    def totalHits(self):
        return self.count50 + self.count100 + self.count300 + self.countMiss

    @property
    def totalSuccessfulHits(self):
        return self.count50 + self.count100 + self.count300

    def to_leaderboard(self, username: str, rankOnline: int) -> str:
        return f"{self.id}|{rankOnline}|{username}|{self.hitScore}|{self.comboBonusScore}|{self.spinnerBonusScore}|{self.count300}|{self.count100}|{self.count50}|{self.countMiss}|{self.maxCombo}|{self.date}|{int(self.guest)}"

    def score_hash(self, device_id: str, device_type: int) -> str:
        return hashlib.md5(
            f"moocow{device_id}{self.count100}{self.count300}{self.count50}{self.countMiss}{self.maxCombo}{self.spinnerBonusScore}{self.comboBonusScore}{self.accuracyBonusScore}{self.rank.name}{self.filename}{device_type}{self.hitScore}{self.difficulty}".encode(),
        ).hexdigest()

    def validate_hash(
        self,
        device_id: str,
        device_type: int,
    ) -> bool:
        return self.hash == self.score_hash(device_id, device_type)

    @classmethod
    def from_row(cls, row: dict) -> "Score":
        s = cls()
        s.id = row["id"]
        s.date = row["_date"]
        s.guest = row["guest"]
        s.rank = Rank[row["_rank"]]
        s.count100 = row["count_100"]
        s.count300 = row["count_300"]
        s.count50 = row["count_50"]
        s.countMiss = row["count_miss"]
        s.maxCombo = row["max_combo"]
        s.spinnerBonusScore = row["spinner_bonus_score"]
        s.comboBonusScore = row["combo_bonus_score"]
        s.hitScore = row["hit_score"]
        s.accuracyBonusScore = row["accuracy_bonus_score"]
        s.difficulty = Difficulty(row["difficulty"])
        s.hitOffset = row["hit_offset"]
        s.filename = row["filename"]
        s.hash = row["hash"]
        return s

    @classmethod
    def from_submission(cls, data: str) -> "Score":
        count_300 = int(data.split("&")[1].split("=")[1])
        count_100 = int(data.split("&")[2].split("=")[1])
        count_50 = int(data.split("&")[3].split("=")[1])
        count_miss = int(data.split("&")[4].split("=")[1])
        max_combo = int(data.split("&")[5].split("=")[1])
        spinner_bonus_score = int(data.split("&")[6].split("=")[1])
        combo_bonus_score = int(data.split("&")[7].split("=")[1])
        accuracy_bonus_score = int(data.split("&")[8].split("=")[1])
        hit_score = int(data.split("&")[9].split("=")[1])
        rank = Rank[data.split("&")[10].split("=")[1]]
        filename = urlparse.unquote(data.split("&")[11].split("=")[1]).replace(
            "+",
            " ",
        )
        score_hash = data.split("&")[13].split("=")[1]
        difficulty = Difficulty(int(data.split("&")[14].split("=")[1]))
        hit_offset = float(data.split("&")[17].split("=")[1])

        s = cls()
        s.count100 = count_100
        s.count300 = count_300
        s.count50 = count_50
        s.countMiss = count_miss
        s.maxCombo = max_combo
        s.spinnerBonusScore = spinner_bonus_score
        s.comboBonusScore = combo_bonus_score
        s.accuracyBonusScore = accuracy_bonus_score
        s.hitScore = hit_score
        s.rank = rank
        s.difficulty = difficulty
        s.hitOffset = hit_offset
        s.filename = filename
        s.hash = score_hash
        s.date = int(time.time())

        return s


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

            score_objects = [Score.from_row(score) for score in scores]
            score_objects = sorted(
                score_objects,
                key=lambda score: score.totalScore,
                reverse=True,
            )

            leaderboard = ""
            for i, score in enumerate(score_objects):
                leaderboard += f"{score.to_leaderboard(scores[i]["username"], i + 1)}{"\n" if i < 99 else ""}"

            return leaderboard
