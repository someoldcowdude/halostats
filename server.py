from flask import Flask, jsonify, redirect, request, render_template, url_for
import sys,http.client, urllib.request,urllib.parse,urllib.error, base64, json

app = Flask(__name__) 
kill_data = {      
}
 
def count_kills():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '03b04056ea114947beaa40503aba4a55',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        match_id = "23c056aa-c05e-4ae7-99ae-d4a282e4530a"
        path = "/stats/h5/matches/" + match_id + "/events?" + params 
        conn.request("GET", path, "{body}", headers)
        response = conn.getresponse()
        rawdata = response.read()
        data = json.loads(rawdata.decode("utf-8"))
    except Exception as e:
        sys.stderr.write("ERROR: %sn" % str(e))
    
    kill_data["gunkills"] = countkills(data, "IsWeapon")
    kill_data["meleekills"] = countkills(data, "IsMelee")
    kill_data["assassinations"] = countkills(data, "IsAssassination")
    kill_data["groundpounds"] = countkills(data, "IsGroundPound")
    kill_data["shoulderbash"] = countkills(data, "IsShoulderBash")
    kill_data["headshots"] = countkills(data, "IsHeadshot")
    kill_data["total"] = countkills(data)
    
@app.route("/") 
def index():
    count_kills()
    return render_template('index.html', data = kill_data)

def countkills(data, type = None):
    count = 0
    if type:
        for kill in data["GameEvents"]:
            if kill[type]:
                count = count + 1
    else:
        count = len(data["GameEvents"])
    return count

if __name__ == "__main__": 
     app.debug = True
     app.run(host='0.0.0.0') 
