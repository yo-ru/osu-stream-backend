import urllib.parse as urlparse

from quart import Blueprint, request

from constants.auth import AuthResponse
from constants.score import SubmissionResponse
from objects.player import Player
from objects.score import Difficulty, Score
from utilities.logging import Ansi, log

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

    # TODO: check if the beatmap exists in the database (filename, difficulty)
    # return 'message: There are no rankings for this beatmap', 200

    # TODO: return a scores from the database
    return "", 200


# osu!stream score submit
@score.route("/submit", methods=["POST"])
async def score_submit_post():
    data = (await request.get_data()).decode("utf-8")
    player = Player.from_submission(data)
    score = Score.from_submission(data)

    log(f"({player.username}) score submission...", Ansi.LCYAN, end=" ")
    match await player.submit_score(score):
        case AuthResponse.CREDENTIAL_MISMATCH:
            log(f"FAILED (hash)", Ansi.LRED, timestamp=False)
            return "fail: hash", 200
        case SubmissionResponse.INVALID_HASH:
            log(f"FAILED (score hash)", Ansi.LRED, timestamp=False)
            return "fail: score hash", 200
        case SubmissionResponse.SUCCESS_HIGHSCORE:
            log(f"SUCCESS (highscore)", Ansi.LGREEN, timestamp=False)
            return "success: highscore", 200
        case SubmissionResponse.SUCCESS:
            log(f"SUCCESS", Ansi.LGREEN, timestamp=False)
            return "success: ok", 200
