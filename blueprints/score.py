from quart import Blueprint, request

from constants.auth import AuthResponse
from constants.score import SubmissionResponse
from objects.player import Player
from objects.score import Leaderboard, Score
from utilities.logging import Ansi, log

score = Blueprint("score", __name__)


# osu!stream score leadboard retrieve
@score.route("/retrieve", methods=["POST"])
async def score_leaderboard_retrieve_post():
    data = (await request.get_data()).decode("utf-8")

    return await Leaderboard(data).to_stream(), 200


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
