import hashlib

from enum import IntEnum, unique
from typing import Optional

@unique
class Rank(IntEnum):
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
    def __init__(self, 
                 username: str,
                 count100: int,
                 count300: int,
                 count50: int,
                 countMiss: int,
                 maxCombo: int,
                 spinnerBonusScore: int,
                 comboBonusScore: int,
                 hitScore: int) -> None:
        self.id: int = 0
        self.date: int = None # TODO: datetime object (unix timestamp)
        self.guest: bool = False
        self.useAccuracyBonus: bool = True
        self.ranking: Rank = Rank.N
        
        self.username: str = username
        self.count100: int = count100
        self.count300: int = count300
        self.count50: int = count50
        self.countMiss: int = countMiss
        self.maxCombo: int = maxCombo
        self.spinnerBonusScore: int = spinnerBonusScore
        self.comboBonusScore: int = comboBonusScore
        self.hitScore: int = hitScore

    @property
    def accuracyBonusScore(self):
        if not self.useAccuracyBonus:
            return 0
        return int(round(max(0, self.accuracy - 0.60) / 0.4 * ACCURACY_BONUS_AMOUNT))

    @property
    def totalScore(self):
        return self.spinnerBonusScore + self.hitScore + self.comboBonusScore + self.accuracyBonusScore

    @property
    def accuracy(self):
        return (self.count50 * 1 + self.count100 * 2 + self.count300 * 4) / (self.totalHits * 4) if self.totalHits > 0 else 0

    @property
    def totalHits(self):
        return self.count50 + self.count100 + self.count300 + self.countMiss

    @property
    def totalSuccessfulHits(self):
        return self.count50 + self.count100 + self.count300
    
    def to_leaderboard(self) -> str:
        return f'{self.id}|{self.onlineRank}|{self.username}|{self.hitScore}|{self.comboBonusScore}|{self.spinnerBonusScore}|{self.count300}|{self.count100}|{self.count50}|{self.countMiss}|{self.maxCombo}|{self.date}|{int(self.guest)}'
    
    def score_hash(self, device_id: str, device_type: int, filename: str, difficulty: Difficulty) -> str:
        return hashlib.md5(f'moocow{device_id}{self.count100}{self.count300}{self.count50}{self.countMiss}{self.maxCombo}{self.spinnerBonusScore}{self.comboBonusScore}{self.accuracyBonusScore}{self.ranking}{filename}{device_type}{self.hitScore}{difficulty}'.encode()).hexdigest()
    
    def validate_score_hash(self, device_id: str, device_type: int, filename: str, difficulty: Difficulty, score_hash: str) -> bool:
        return score_hash == self.score_hash(device_id, device_type, filename, difficulty)

ACCURACY_BONUS_AMOUNT = 400000
MAX_SCORE = 1000000
HIT_PLUS_COMBO_BONUS_AMOUNT = MAX_SCORE - ACCURACY_BONUS_AMOUNT