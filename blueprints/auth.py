from quart import Blueprint, request

from constants.auth import AuthResponse
from objects.player import Player
from utilities.logging import Ansi, log

auth = Blueprint("auth", __name__)


# osu!stream auth connect
# this basically serves to link a device to a player; end result is to log in the player
@auth.route("/connect")
async def auth_connect_get():
    player = Player.from_connect(request.args)

    if not player:
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
# this basically serves to unlink a device from a player; end result is to log out the player
@auth.route("/disconnect")
async def auth_disconnect_get():
    player = Player.from_disconnect(request.args)

    if not player:
        return "fail: missing required arguments", 400

    log(f"({player.username}) disconnect...", Ansi.LCYAN, end=" ")
    match await player.disconnect():
        case AuthResponse.CREDENTIAL_MISMATCH:
            log(f"FAILED (hash)", Ansi.LRED, timestamp=False)
            return "fail: hash", 200
        case AuthResponse.SUCCESS:
            log(f"SUCCESS", Ansi.LGREEN, timestamp=False)
            return "success: ok", 200
