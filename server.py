from flask import Flask, jsonify, redirect, request, render_template, url_for
import sys,http.client, urllib.request,urllib.parse,urllib.error, base64, json

app = Flask(__name__) 
kill_data = {
	"gunkills":666,
	"meleekills":3,
	"assassinations":23,
	"groundpounds":1666,
	"shoulderbash":6663,
	"headshots":66623,
	"total":66631231
}
 

@app.route("/") 
def hello():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': '03b04056ea114947beaa40503aba4a55',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('www.haloapi.com')
        conn.request("GET", "/stats/h5/matches/23c056aa-c05e-4ae7-99ae-d4a282e4530a/events?%s" % params, "{body}", headers)
        response = conn.getresponse()
        rawdata = response.read()
        data = json.loads(rawdata.decode("utf-8"))
    except Exception as e:
        sys.stderr.write("ERROR: %sn" % str(e))
    
    gunkills = countkills(data, "IsWeapon")
    meleekills = countkills(data, "IsMelee")
    assassinations = countkills(data, "IsAssassination")
    groundpounds = countkills(data, "IsGroundPound")
    shoulderbash = countkills(data, "IsShoulderBash")
    headshots = countkills(data, "IsHeadshot")
    total = countkills(data)
    
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
