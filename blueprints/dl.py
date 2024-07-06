from quart import Blueprint, request

dl = Blueprint("dl", __name__)

dl.route('/list')
async def dl_list_get():
    songs = """
Filename.osz2\t\tTitle - Title\t1.0
Filename.osz2\t\tTitle - Title\t1.0

PackID\tPackName
Filename.osz2\t\tTitle - Title\t1.0
Filename.osz2\t\tTitle - Title\t1.0
    """
    return songs, 200

dl.route('/')
async def dl_get():
    return "dl", 200