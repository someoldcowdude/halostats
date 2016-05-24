from flask import Flask, jsonify, redirect, request, render_template, url_for
from halopy import HaloPy
import sys,http.client, urllib.request,urllib.parse,urllib.error, base64, json

HALO_API_KEY = "03b04056ea114947beaa40503aba4a55"
app = Flask(__name__) 
halo = HaloPy(HALO_API_KEY, cache_backend='memory')

def get_latest_match_id():
    return "23c056aa-c05e-4ae7-99ae-d4a282e4530a"

def count_all_kills():
    kill_data = {      
    }

    params = urllib.parse.urlencode({
    })

    match_id = get_latest_match_id()
    path = "/stats/h5/matches/" + match_id + "/events?" + params 
    
    data = call_api(path)
    
    kill_data["gunkills"] = count_kills(data, "IsWeapon")
    kill_data["meleekills"] = count_kills(data, "IsMelee")
    kill_data["assassinations"] = count_kills(data, "IsAssassination")
    kill_data["groundpounds"] = count_kills(data, "IsGroundPound")
    kill_data["shoulderbash"] = count_kills(data, "IsShoulderBash")
    kill_data["headshots"] = count_kills(data, "IsHeadshot")
    kill_data["total"] = count_kills(data)
    return kill_data

def get_player_summary():
    gamertag = "someoldcowdude"
    result = halo.get_player_service_record(gamertag, game_mode='arena')
    return result

def get_weapons_meta_data():
    params = urllib.parse.urlencode({
        })
    path = "/metadata/h5/metadata/weapons?%s" % params 
    return call_api(path)

@app.route("/") 
def index():
    return render_template('index.html')

@app.route("/match/summary") 
def match_summary():
    kill_data = count_all_kills()
    return render_template('match/summary.html', data = kill_data)
 
@app.route("/player/summary")
def player_summary():
    alldata = get_player_summary()
    weaponstats = alldata.Result["ArenaStats"]["WeaponStats"]
    weapons = halo.get_weapons()

    return render_template('player/summary.html', data = alldata, weaponstats = weaponstats, weapons = weapons)



def count_kills(data, type = None):
    count = 0
    if type:
        for kill in data["GameEvents"]:
            try:
                if kill[type]:
                    count = count + 1
            except Exception as e:
                sys.stderr.write("ERROR: %sn" % str(e))
                
    else:
        # FIXME: incorrect count see issue #1
        count = len(data["GameEvents"])
    return count

if __name__ == "__main__": 
     app.debug = True
     app.run(host='0.0.0.0') 
