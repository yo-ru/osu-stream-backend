from __future__ import annotations

import hashlib
import time
import urllib.parse as urlparse
from enum import Enum
from enum import IntEnum
from enum import unique

from objects.player import Player


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
    HARD = 2
    EXPERT = 3


class Score:
    def __init__(self) -> None:
        self._id: int = 0
        self._player: Player = None
        self._date: int = int(time.time())
        self._guest: bool = False
        self._useAccuracyBonus: bool = True
        self._rank: Rank = Rank.N
        self._rankOnline: int = 0
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
        self._scoreHash: str = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value: Player):
        self._player = value

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
    def useAccuracyBonus(self):
        return self._useAccuracyBonus

    @useAccuracyBonus.setter
    def useAccuracyBonus(self, value: bool):
        self._useAccuracyBonus = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: Rank):
        self._rank = value

    @property
    def rankOnline(self):
        return self._rankOnline

    @rankOnline.setter
    def rankOnline(self, value: int):
        self._rankOnline = value

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
    def scoreHash(self):
        return self._scoreHash

    @scoreHash.setter
    def scoreHash(self, value: str):
        self._scoreHash = value

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
        return int(round(max(0, self.accuracy - 0.60) / 0.4 * ACCURACY_BONUS_AMOUNT))

    @accuracyBonusScore.setter
    def accuracyBonusScore(self, value: int):
        self._accuracyBonusScore = value

    @property
    def accuracy(self):
        return (
            (self.count50 * 1 + self.count100 * 2 + self.count300 * 4)
            / (self.totalHits * 4)
            if self.totalHits > 0
            else 0
        )

    @property
    def totalHits(self):
        return self.count50 + self.count100 + self.count300 + self.countMiss

    @property
    def totalSuccessfulHits(self):
        return self.count50 + self.count100 + self.count300

    def to_leaderboard(self) -> str:
        return f"{self.id}|{self.rankOnline}|{self.player.username}|{self.hitScore}|{self.comboBonusScore}|{self.spinnerBonusScore}|{self.count300}|{self.count100}|{self.count50}|{self.countMiss}|{self.maxCombo}|{self.date}|{int(self.guest)}"

    def score_hash(self, device_id: str, device_type: int) -> str:
        return hashlib.md5(
            f"moocow{device_id}{self.count100}{self.count300}{self.count50}{self.countMiss}{self.maxCombo}{self.spinnerBonusScore}{self.comboBonusScore}{self.accuracyBonusScore}{self.rank.name}{self.filename}{device_type}{self.hitScore}{self.difficulty}".encode(),
        ).hexdigest()

    def validate_score_hash(
        self,
        device_id: str,
        device_type: int,
        score_hash: str,
    ) -> bool:
        return score_hash == self.score_hash(device_id, device_type)

    @classmethod
    def from_submission(cls, data: str) -> Score:
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
        )  # ah yes peppy, encode spaces as + instead of %20
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
        s.scoreHash = score_hash
        s.date = int(time.time())

        return s


ACCURACY_BONUS_AMOUNT = 400000
MAX_SCORE = 1000000
HIT_PLUS_COMBO_BONUS_AMOUNT = MAX_SCORE - ACCURACY_BONUS_AMOUNT
