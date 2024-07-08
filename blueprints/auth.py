from quart import Blueprint, request

from constants.auth import AuthResponse
from objects.player import Player
from utilities.logging import Ansi, log

auth = Blueprint("auth", __name__)


# osu!stream auth connect
@auth.route("/connect")
async def auth_connect_get():
    try:
        player = Player.from_connect(request.args)
    except:
        return "fail: missing required arguments", 400

    log(f"({player.username}) connect...", Ansi.LCYAN, end=" ")
    match await player.connect():
        case AuthResponse.CREDENTIAL_MISMATCH:
            log(f"FAILED (hash)", Ansi.LRED, timestamp=False)
            return "fail: hash", 200
        case AuthResponse.ALREADY_LINKED:
            log(f"FAILED (link)", Ansi.LRED, timestamp=False)
            return "fail: link", 200
        case AuthResponse.SUCCESS:
            log(f"SUCCESS", Ansi.LGREEN, timestamp=False)
            return "success: ok", 200


# osu!stream auth disconnect
@auth.route("/disconnect")
async def auth_disconnect_get():
    try:
        player = Player.from_disconnect(request.args)
    except:
        return "fail: missing required arguments", 400

    log(f"({player.username}) disconnect...", Ansi.LCYAN, end=" ")
    match await player.disconnect():
        case AuthResponse.CREDENTIAL_MISMATCH:
            log(f"FAILED (hash)", Ansi.LRED, timestamp=False)
            return "fail: hash", 200
        case AuthResponse.SUCCESS:
            log(f"SUCCESS", Ansi.LGREEN, timestamp=False)
            return "success: ok", 200
