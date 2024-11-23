import json
import cryption
import random as rd

randId = rd.randint(1000000, 9999999)
normalConfig = {
    "mode": "r", 
    "mqtt": {
        "broker": "broker.emqx.io",
        "port": 1883,
        "topic": f"tks/callyou/pymqtt/TKCU{randId}",
        "client_id": f"PYTKCU-r-TKCU{randId}",
        "username": "emqx",
        "password": "**********"
    },
    "performance": {
        "refresh_time": 5000
    },
    "show": {
        "stay_time": 10000
    },
    "key": cryption.randkey(16)
}

def load_json(file_path: str):
    try:
        with open(file_path, "r") as f:
            data = json.loads(f.read())
            return data
    except:
        save_json(file_path, normalConfig)
        return normalConfig
    
def save_json(file_path: str, content: dict|list):
    with open(file_path, "w") as f:
        f.write(json.dumps(content))
