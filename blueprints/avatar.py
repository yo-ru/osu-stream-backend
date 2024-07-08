from quart import Blueprint, redirect

avatar = Blueprint("avatar", __name__)

# osu!stream avatar retrieve
@avatar.route("/<username>")
async def get_avatar(username):
    # return default avatar for now (/static/default.png)
    return redirect("/static/avatars/default.png")
