from __future__ import annotations

import random
import time
import urllib.parse as urlparse

from quart import Blueprint
from quart import request

from objects.player import Player
from objects.score import Difficulty
from objects.score import Rank
from objects.score import Score

score = Blueprint("score", __name__)


# osu!stream score leadboard retrieve
@score.route("/retrieve", methods=["POST"])
async def score_leaderboard_retrieve_post():
    data = (await request.get_data()).decode("utf-8")

    # args (peppy why...)
    device_id = data.split("&")[0].split("=")[
        1
    ]  # i think this is used as some sort of auth identifier for making the request
    filename = urlparse.unquote(
        data.split("&")[1].split("=")[1],
    )  # spaces are denoted as + in the filename
    period = data.split("&")[2].split("=")[
        1
    ]  # always 0? (probably for future leaderboard implementations)
    difficulty = Difficulty(
        int(data.split("&")[3].split("=")[1]),
    )  # difficulty (-1: None, 0: Easy, 1: Normal, 2: Hard, 3: Expert)

    # TODO: do some sort of check on unique_device_id

    # TODO: check if the beatmap exists in the database (filename, difficulty)
    # return 'message: There are no rankings for this beatmap', 200

    # TODO: return a scores from the database

    # generate random scores using score object for testing purposes
    random_scores = []
    for i in range(50):
        score = Score()
        score.rankOnline = i + 1
        score.player = Player()
        score.player.username = f"User{i+1}"
        score.count100 = random.randint(0, 100)
        score.count300 = random.randint(0, 100)
        score.count50 = random.randint(0, 100)
        score.countMiss = random.randint(0, 100)
        score.maxCombo = random.randint(0, 100)
        score.spinnerBonusScore = random.randint(0, 100000)
        score.comboBonusScore = random.randint(0, 100000)
        score.hitScore = random.randint(0, 100000)
        score.date = int(time.time())

        random_scores.append(score)

    # sort random_scores and update rankOnline
    random_scores.sort(key=lambda x: x.totalScore, reverse=True)
    for i, score in enumerate(random_scores):
        score.rankOnline = i + 1
    scores_sent = "\n".join([score.to_leaderboard() for score in random_scores])
    return scores_sent, 200


# osu!stream score submit
@score.route("/submit", methods=["POST"])
async def score_submit_post():
    data = (await request.get_data()).decode("utf-8")

    player = Player.from_submission(data)

    # TODO: check if user exists in the database and validate user hash

    # TODO: check if user shares a device id with another user (most likely deny submissions from the same device id if the user is different to prevent leaderboard manipulation)

    # TODO: check if beatmap exists in the database

    # score
    score = Score.from_submission(data)

    # validate score hash
    if not score.validate_score_hash(
        device_id=player.deviceId,
        device_type=player.deviceType,
        score_hash=score.scoreHash,
    ):
        return "fail: invalid score hash", 200

    # TODO: save score to the database if it is a new high score

    # TODO: score submission successful; new high score
    # return 'message: You set a new high score!', 200

    # TODO: score submission successful; no new high score
    return "", 200
