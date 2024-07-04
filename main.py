import os
import databases

from quart import Quart

import settings

from log import log, Ansi

app = Quart(__name__)
app.secret_key = os.urandom(32)
app.permanent_session_lifetime = 86400 # 1 day

# register blueprints
from blueprints.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

from blueprints.score import score
app.register_blueprint(score, url_prefix='/score')

from blueprints.auth import auth
app.register_blueprint(auth, url_prefix='/auth')

@app.before_serving
async def before_serving():
    log('=== osu!stream backend ===', Ansi.LMAGENTA)
    
    # check if the database is accessible
    app.db = databases.Database(settings.DB_DSN)
    log('Connecting to the database...', col=Ansi.LCYAN, end=' ')
    try:
        await app.db.connect()
        await app.db.disconnect()
        log('SUCCESS', Ansi.LGREEN, timestamp=False)
    except Exception as e:
        log(f'FAILED', Ansi.LRED, timestamp=False)
        log(f'Error: {Ansi.RESET!r}{e}', Ansi.LRED)
        log('==========================', Ansi.LMAGENTA)
        os._exit(1)
    log('==========================', Ansi.LMAGENTA)
        
        
    

if __name__ == '__main__':
    app.run(
        debug=settings.QUART_DEBUG,
        host=settings.QUART_HOST,
        port=settings.QUART_PORT
    )