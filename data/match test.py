import sys,http.client, urllib.request,urllib.parse,urllib.error, base64, json

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
    #print(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
    Gunkills = 0
    meleekills = 0
    assanations = 0
    groundpounds = 0
    total = 0
    
    print("gun kills")
    for kill in data["GameEvents"]:
        if kill["IsWeapon"]:
            Gunkills = Gunkills + 1
    print(Gunkills)
    print("====")

    print("melee kills")    
    for kill in data["GameEvents"]:
        if kill["IsMelee"]:
            meleekills = meleekills + 1
    print(meleekills)
    print("======")

    print("asassinations")
    for kill in data["GameEvents"]:
        if kill["IsAssassination"]:
            assanations = assanations + 1
    print(assanations)
    print("======")

    print("ground pounds")
    for kill in data["GameEvents"]:
        if kill["IsGroundPound"]:
            groundpounds = groundpounds + 1
    print(groundpounds)
    print("======")

    print("total deaths")
    for kill in data["GameEvents"]:
            total = total + 1
    print(total)
    print("======")

    if total != (Gunkills+meleekills+assanations+groundpounds):
        print ("FIXME: total kills is not = individual kill count (addin sholder bashes)")
    
    conn.close()
except Exception as e:
    sys.stderr.write("ERROR: %sn" % str(e))
    
