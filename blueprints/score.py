import time
import urllib.parse as urlparse

from quart import Blueprint, request

from objects.score import Score, Difficulty, Rank

score = Blueprint('score', __name__)

# osu!stream score leadboard retrieve
@score.route('/retrieve.php', methods=['POST'])
async def score_leaderboard_retrieve_post():
    data = (await request.get_data()).decode('utf-8')
    
    # args (osu!stream sends URL args as POST data???)
    device_id = data.split('&')[0].split('=')[1] # i think this is used as some sort of auth identifier for making the request
    filename = urlparse.unquote(data.split('&')[1].split('=')[1]) # spaces are denoted as + in the filename
    period = data.split('&')[2].split('=')[1] # always 0? (probably for future leaderboard implementations)
    difficulty = Difficulty(int(data.split('&')[3].split('=')[1])) # difficulty (-1: None, 0: Easy, 1: Normal, 2: Hard, 3: Expert)
    
    # check for required args
    if not device_id or not filename or not period or not difficulty:
        return 'fail: missing required arguments', 400
    
    # TODO: do some sort of check on unique_device_id
    
    # TODO: check if the beatmap exists in the database (filename, difficulty)
    # return 'message: There are no rankings for this beatmap', 200
    
    # return a list of scores (score\nscore\nscore\n...)
    # score: id|leadboard_position|username|hit_score|combo_bonus_score|spinner_bonus_score|count_300|count_100|count_50|count_miss|max_combo|date|guest
    # 1|1|Yoru|200000|200000|200000|1|0|0|0|1|1719974569|0 (SS; example)
    return '1|1|Yoru|200000|200000|200000|1|0|0|0|1|1719974569|0\n1|1|peppy|200000|200000|200000|1|0|0|0|1|1719974569|0', 200

# osu!stream score submit
@score.route('/submit.php', methods=['POST'])
async def score_submit_post():
    data = (await request.get_data()).decode('utf-8')
    
    # args
    device_id = data.split('&')[0].split('=')[1] # unique device id
    device_type = int(data.split('&')[1].split('=')[1]) # device type (usually 0 if not iOS device.)
    username = data.split('&')[2].split('=')[1] # username
    user_hash = data.split('&')[3].split('=')[1] # twitter user hash
    twitter_id = data.split('&')[4].split('=')[1] # twitter id
    
    count_300 = int(data.split('&')[5].split('=')[1]) # hit 300s
    count_100 = int(data.split('&')[6].split('=')[1]) # hit 100s
    count_50 = int(data.split('&')[7].split('=')[1]) # hit 50s
    count_miss = int(data.split('&')[8].split('=')[1]) # hit misses
    max_combo = int(data.split('&')[9].split('=')[1]) # max combo
    spinner_bonus = int(data.split('&')[10].split('=')[1]) # spinner bonus
    combo_bonus = int(data.split('&')[11].split('=')[1]) # combo bonus
    accuracy_bonus = int(data.split('&')[12].split('=')[1]) # accuracy bonus
    hit_score = int(data.split('&')[13].split('=')[1]) # hit score
    rank = Rank(int(data.split('&')[14].split('=')[1])) # rank
    difficulty = Difficulty(int(data.split('&')[15].split('=')[1])) # difficulty
    hit_offset = float(data.split('&')[16].split('=')[1]) # average hit offset (i have no clue how i can calculate this from the score data provided by the game; likely a placeholder for future implementations.)
    
    filename = urlparse.unquote(data.split('&')[17].split('=')[1]) # beatmap filename
    score_hash = data.split('&')[18].split('=')[1] # score hash
    
    # check for required args
    if not device_id or not count_300 or not count_100 or not count_50 or not count_miss or not max_combo or not spinner_bonus or not combo_bonus or not accuracy_bonus or not hit_score or not rank or not filename or not user_hash or not score_hash or not difficulty or not username or not twitter_id or not device_type or not hit_offset:
        return 'fail: missing required arguments', 400
    
    # TODO: check if user exists in the database and validate user hash
    
    # TODO: check if user shares a device id with another user (most likely deny submissions from the same device id if the user is different to prevent leaderboard manipulation)
    
    # TODO: check if beatmap exists in the database
    
    # score
    score = Score(
        username=username,
        count300=count_300,
        count100=count_100,
        count50=count_50,
        countMiss=count_miss,
        maxCombo=max_combo,
        spinnerBonusScore=spinner_bonus,
        comboBonusScore=combo_bonus,
        hitScore=hit_score)
    score.ranking = rank
    score.date = int(time.time())
    
    # validate score hash
    if not score.validate_score_hash(
        device_id=device_id,
        device_type=device_type,
        filename=filename,
        difficulty=difficulty,
        
        score_hash=score_hash
    ):
        return 'fail: invalid score hash', 403
    
    # TODO: save score to the database
    
    # TODO: score submission successful; new high score
    # return 'message: You set a new high score!', 200
    
    # score submission successful; no new high score
    return '', 200