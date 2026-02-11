import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import storage
from datetime import datetime, timedelta


# Rate-limit protection (fixed for version 4.1)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Load keys and links from .env
load_dotenv()


app = Flask(__name__)


# FIXED limiter (new syntax)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100/hour"]
)


# --- STATISTICS LOGIC ---
def get_stats(period='all'):
    """Calculates top users based on interactions for the leaderboard"""
    db = storage.load_json(storage.DB_FILE)
    purchases = storage.load_json(storage.PURCHASES_FILE)
    profiles = storage.load_json(storage.PROFILES_FILE)

    now = datetime.now()
    delta = None
    if period == 'day': delta = timedelta(days=1)
    elif period == 'week': delta = timedelta(weeks=1)
    elif period == 'month': delta = timedelta(days=30)


    user_buys = {}
    user_likes = {}
    user_shares = {}


    # 1. Process Purchases
    for wallet, p_list in purchases.items():
        count = 0
        for p in p_list:
            if isinstance(p, dict):
                p_time = datetime.fromisoformat(p['time'])
                if delta and p_time < now - delta: continue
                count += 1
            elif not delta:
                count += 1
        if count > 0: user_buys[wallet] = count


    # 2. Process Likes and Shares from database
    for card in db:
        for like in card.get('likes', []):
            l_time = datetime.fromisoformat(like['time'])
            if delta and l_time < now - delta: continue
            user_likes[like['wallet']] = user_likes.get(like['wallet'], 0) + 1

        for share in card.get('shares', []):
            s_time = datetime.fromisoformat(share['time'])
            if delta and s_time < now - delta: continue
            user_shares[share['wallet']] = user_shares.get(share['wallet'], 0) + 1


    def format_list(data_dict):
        result = []
        for wallet, count in data_dict.items():
            result.append({
                "wallet": wallet,
                "count": count,
                "x": profiles.get(wallet, None)
            })
        return sorted(result, key=lambda x: x['count'], reverse=True)[:10]


    return {
        "buyers": format_list(user_buys),
        "likers": format_list(user_likes),
        "sharers": format_list(user_shares)
    }


def format_forecast_date(iso_string):
    """Convert ISO timestamp to readable format: '10 Feb, 19:02'"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime('%d %b, %H:%M')
    except:
        return 'Just now'


# --- ROUTES ---


@app.route('/')
def index():
    """Main terminal page with assets from .env"""
    ui_assets = {
        "bg_video": os.getenv("BG_VIDEO_URL"),
        "logo": os.getenv("LOGO_URL"),
        "avatar": os.getenv("DEFAULT_AVATAR_URL"),
        "card_base": os.getenv("CARD_IMG_BASE_URL")
    }
    db = storage.load_json(storage.DB_FILE)
    sorted_forecasts = sorted(db, key=lambda x: x.get('createdAt', ''), reverse=True)

    # Add formatted date to each forecast
    for forecast in sorted_forecasts:
        forecast['created_at'] = format_forecast_date(forecast.get('createdAt', ''))

    return render_template('index.html', forecasts=sorted_forecasts, assets=ui_assets)


@app.route('/buy', methods=['POST'])
@limiter.limit("5/minute")
def buy():
    data = request.json
    tx = data.get('tx')
    storage.save_purchase(data.get('wallet'), data.get('card_id'), tx)

    if tx:
        print(f"✅ SOL TX: https://solscan.io/tx/{tx}?cluster=devnet")

    return jsonify({"status": "success"})


@app.route('/api/user_state/<wallet>')
def get_user_state(wallet):
    purchases_data = storage.load_json(storage.PURCHASES_FILE)
    user_purchases = [p['id'] for p in purchases_data.get(wallet, []) if isinstance(p, dict)]
    db = storage.load_json(storage.DB_FILE)
    user_likes = []
    for item in db:
        for like in item.get('likes', []):
            if like['wallet'] == wallet:
                user_likes.append(item['id'])
                break
    return jsonify({"unlocked": user_purchases, "liked": user_likes})


@app.route('/stats/<period>')
def stats(period):
    return jsonify(get_stats(period))


@app.route('/like', methods=['POST'])
@limiter.limit("10/minute")
def like():
    data = request.json
    storage.add_interaction(data['card_id'], data['wallet'], 'likes')
    return jsonify({"status": "success"})


@app.route('/share', methods=['POST'])
@limiter.limit("10/minute")
def share():
    data = request.json
    storage.add_interaction(data['card_id'], data['wallet'], 'shares')
    return jsonify({"status": "success"})


@app.route('/save_profile', methods=['POST'])
@limiter.limit("3/hour")
def save_profile():
    data = request.json
    handle = storage.save_user_profile(data.get('wallet'), data.get('x_handle', ''))
    return jsonify({"status": "success", "x": handle})


@app.route('/api/profile/<wallet>')
def get_profile(wallet):
    return jsonify({"x": storage.get_user_profile(wallet)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
