from quart import Blueprint, request

admin = Blueprint('admin', __name__)

# osu!stream crash reporting
@admin.route('/crash', methods=['POST'])
async def admin_crash_report_post():
    data = (await request.get_data()).decode('utf-8')
    
    # args
    exception = data.split('&')[0].split('=')[1]
    try:
        device = data.split('&')[1].split('=')[1]
        version = data.split('&')[2].split('=')[1]
    except IndexError:
        device, version = 'unknown', 'unknown'
    
    if not exception:
        return 'fail: missing required arguments', 400
    
    
    # TODO: store crash reports in database
    with open(f'crash-{device}-{version}.log', 'a+') as f:
        f.write(exception)
    
    return 'success: ok', 200