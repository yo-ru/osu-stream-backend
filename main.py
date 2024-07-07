import os

import databases
from quart import Quart, request

import settings
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

from blueprints.dl import dl

app.register_blueprint(dl, url_prefix="/dl")


@app.before_serving
async def before_serving():
    log("=== osu!stream backend ===", Ansi.LMAGENTA)

    log("checking database connection...", col=Ansi.LCYAN, end="")
    try:
        db = databases.Database(settings.DB_DSN)
        await db.connect()
        await db.disconnect()
        log("SUCCESS", Ansi.LGREEN, timestamp=False)
    except Exception as e:
        log(f"FAILED", Ansi.LRED, timestamp=False)
        log("==========================", Ansi.LMAGENTA)
        await app.shutdown()
        os._exit(1)

    log("")

    log(
        f"debug mode...{f'{Ansi.LGREEN!r}ON' if settings.QUART_DEBUG else f'{Ansi.LRED!r}OFF'}",
        Ansi.LCYAN,
    )
    log(
        f"osu!stream backend serving on...{Ansi.LGREEN!r}{settings.QUART_HOST}:{settings.QUART_PORT}",
        Ansi.LCYAN,
    )

    log("==========================", Ansi.LMAGENTA)


if __name__ == "__main__":
    app.run(
        debug=settings.QUART_DEBUG,
        host=settings.QUART_HOST,
        port=settings.QUART_PORT,
    )
