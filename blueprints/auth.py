from quart import Blueprint, request

auth = Blueprint("auth", __name__)


# osu!stream auth connect
# this basically serves to link a device to a player; end result is to log in the player
@auth.route("/connect")
async def auth_get():
    # args
    device_id = request.args.get("udid")
    username = request.args.get("username")
    hash = request.args.get("cc")

    print(f"{device_id} | {username} | {hash}")

    # return 'fail: hash', 200 # NOTE: return this for both username check and hash check

    return "success: ok", 200


# osu!stream auth disconnect
# this basically serves to unlink a device from a player; end result is to log out the player
@auth.route("/disconnect")
async def auth_disconnect_get():
    # args
    device_id = request.args.get("udid")
    hash = request.args.get("cc")

    # TODO: remove device_id from player in database

    print(f"{device_id} | {hash}")
    return "success: ok", 200
