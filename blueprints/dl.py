import urllib.parse as urlparse

from quart import Blueprint, redirect, request

dl = Blueprint("dl", __name__)

# osu!stream beatmap pack list
@dl.route("/list")
async def dl_list_get():
    return redirect("https://www.osustream.com/dl/list3.php", 307)


# osu!stream thumbnail preview
@dl.route("/preview")
async def dl_preview_get():
    args = request.args
    pack_id = args.get("filename")
    format = args.get("format")  # unused (osu!stream only requests .jpg)
    
    params = urlparse.urlencode({"filename": pack_id, "format": format})
    return redirect(f"https://www.osustream.com/dl/preview.php{f"?{params}" if params else ""}", 307)


# osu!stream audio preview
@dl.route("/preview", methods=["POST"])
async def dl_preview_post():
    data = (await request.get_data()).decode("utf-8")
    pack_id = data.split("&")[0].split("=")[1]
    filename = data.split("&")[1].split("=")[1]
    format = data.split("&")[2].split("=")[1]
    
    return redirect("https://www.osustream.com/dl/preview.php", 307)


# osu!stream beatmap preview download
@dl.route("/download")
async def dl_download_get():
    args = request.args
    pack_id = args.get("pack")
    filename = args.get("filename")
    device_id = args.get("id")
    preview = args.get("preview")  # unused: osu!stream only uses GET for previews
    
    params = urlparse.urlencode({"pack": pack_id, "filename": filename, "id": device_id, "preview": preview})
    return redirect(f"https://www.osustream.com/dl/download2.php{f"?{params}" if params else ""}", 307)

# osu!stream beatmap download
@dl.route("/download", methods=["POST"])
async def dl_download_post():
    data = (await request.get_data()).decode("utf-8")
    pack_id = data.split("&")[0].split("=")[1]
    filename = data.split("&")[1].split("=")[1]
    device_id = data.split("&")[2].split("=")[1]
    receipt = data.split("&")[3].split("=")[1]
    
    try:
        updateChecksum = data.split("&")[4].split("=")[1]
    except IndexError:
        updateChecksum = None
    
    return redirect("https://www.osustream.com/dl/download2.php", 307)