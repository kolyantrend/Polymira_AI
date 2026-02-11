import json
import os
import hashlib
from datetime import datetime

# === ABSOLUTE PATHS ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'forecasts.json')
PURCHASES_FILE = os.path.join(BASE_DIR, 'purchases.json')
PROFILES_FILE = os.path.join(BASE_DIR, 'profiles.json')

MAX_ENTRIES = 500 

def generate_id(title):
    return hashlib.md5(title.encode()).hexdigest()[:10]

def load_json(filename):
    if not os.path.exists(filename): 
        if 'purchases' in filename or 'profiles' in filename: return {}
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load {filename}: {e}")
        if 'purchases' in filename or 'profiles' in filename: return {}
        return []

def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Could not save {filename}: {e}")

# === PROFILES ===
def save_user_profile(wallet, x_handle):
    profiles = load_json(PROFILES_FILE)
    clean_handle = x_handle.replace('@', '').replace('https://x.com/', '').replace('https://twitter.com/', '').strip()
    profiles[wallet] = clean_handle
    save_json(PROFILES_FILE, profiles)
    return clean_handle

def get_user_profile(wallet):
    profiles = load_json(PROFILES_FILE)
    return profiles.get(wallet, None)

# === PURCHASES ===
def save_purchase(wallet, card_id, tx_signature=None):
    data = load_json(PURCHASES_FILE)
    if wallet not in data: data[wallet] = []
    
    # Duplicate check
    for item in data[wallet]:
        if isinstance(item, dict) and item.get('id') == card_id: return True
        if isinstance(item, str) and item == card_id: return True

    new_purchase = {
        "id": card_id,
        "time": datetime.now().isoformat(),
        "tx": tx_signature
    }
    data[wallet].append(new_purchase)
    save_json(PURCHASES_FILE, data)
    return True

# === LIKES AND SHARES (TOGGLE LOGIC) ===
def add_interaction(card_id, wallet, type='likes'):
    """Works as a toggle: if exists - removes, if not - adds"""
    db = load_json(DB_FILE)
    for item in db:
        if item.get('id') == card_id:
            if type not in item: item[type] = []
            
            # Check if this wallet already performed the action
            found_index = -1
            for i, action in enumerate(item[type]):
                if action['wallet'] == wallet:
                    found_index = i
                    break
            
            if found_index != -1:
                # ALREADY EXISTS -> REMOVE (Unlike/Unshare)
                item[type].pop(found_index)
            else:
                # NOT EXISTS -> ADD (Like/Share)
                item[type].append({"wallet": wallet, "time": datetime.now().isoformat()})
                
            break
            
    save_json(DB_FILE, db)

# === SAVE CARD ===
def save_to_database(new_entry):
    db = load_json(DB_FILE)
    new_entry['id'] = generate_id(new_entry['title'])
    new_entry['createdAt'] = datetime.now().isoformat()
    new_entry['likes'] = [] 
    new_entry['shares'] = [] 
    
    db.insert(0, new_entry)
    
    if len(db) > MAX_ENTRIES:
        purchases = load_json(PURCHASES_FILE)
        bought_ids = set()
        for wallet_data in purchases.values():
            for p in wallet_data: 
                if isinstance(p, dict): bought_ids.add(p.get('id'))
                elif isinstance(p, str): bought_ids.add(p)
        
        i = len(db) - 1
        while i >= MAX_ENTRIES:
            if db[i].get('id') not in bought_ids: db.pop(i)
            i -= 1
    
    save_json(DB_FILE, db)

def add_like(card_id, wallet):
    # This function is kept for compatibility, redirecting to add_interaction
    add_interaction(card_id, wallet, 'likes')

def is_duplicate(title):
    """Checks if a forecast with the same title already exists in the database"""
    db = load_json(DB_FILE)
    return any(item.get('title') == title for item in db)