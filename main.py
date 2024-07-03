import os

from quart import Quart, render_template, request

import settings

app = Quart(__name__)
app.secret_key = os.urandom(32)
app.permanent_session_lifetime = 86400 # 1 day

@app.before_serving
async def before_serving():
    print('osu!stream backend is starting...')

# register blueprints
from blueprints.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

from blueprints.score import score
app.register_blueprint(score, url_prefix='/score')

if __name__ == '__main__':
    app.run(
        debug=settings.QUART_DEBUG,
        host=settings.QUART_HOST,
        port=settings.QUART_PORT
    )