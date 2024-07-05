import os

import databases
from quart import Quart

import settings
import utilities.database as db
from utilities.logging import Ansi, log

app = Quart(__name__)
app.secret_key = os.urandom(32)
app.permanent_session_lifetime = 86400  # 1 day

# register blueprints
from blueprints.admin import admin

app.register_blueprint(admin, url_prefix="/admin")

from blueprints.score import score

app.register_blueprint(score, url_prefix="/score")

from blueprints.auth import auth

app.register_blueprint(auth, url_prefix="/auth")

from blueprints.avatar import avatar

app.register_blueprint(avatar, url_prefix="/avatar")


@app.before_serving
async def before_serving():
    log("=== osu!stream backend ===", Ansi.LMAGENTA)

    log("checking database connection...", col=Ansi.LCYAN, end=" ")
    if await db.check_alive():
        log("SUCCESS", Ansi.LGREEN, timestamp=False)
    else:
        log(f"FAILED", Ansi.LRED, timestamp=False)
        log("==========================", Ansi.LMAGENTA)
        await app.shutdown()
        os._exit(1)

    log("checking database structure...", col=Ansi.LCYAN, end=" ")
    if await db.check_structure():
        log("SUCCESS", Ansi.LGREEN, timestamp=False)
    else:
        log(f"FAILED", Ansi.LRED, timestamp=False)
        log("==========================", Ansi.LMAGENTA)
        await app.shutdown()
        os._exit(1)

    log("")

    log(
        f"debug mode... {f'{Ansi.LGREEN!r}ON' if settings.QUART_DEBUG else f'{Ansi.LRED!r}OFF'}",
        Ansi.LCYAN,
    )
    log(
        f"osu!stream backend serving on... {Ansi.LGREEN!r}{settings.QUART_HOST}:{settings.QUART_PORT}",
        Ansi.LCYAN,
    )

    log("==========================", Ansi.LMAGENTA)


if __name__ == "__main__":
    app.run(
        debug=settings.QUART_DEBUG,
        host=settings.QUART_HOST,
        port=settings.QUART_PORT,
    )
