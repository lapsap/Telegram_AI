import requests, json, urllib
def init(input):
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    woeid_query = "select * from ugeo.geocode where text='%s' and appname='lapsap'" %(input)
    woeid_url = baseurl + urllib.parse.urlencode({'q':woeid_query}) + "&format=json"
    woeid_data = json.loads(requests.get(woeid_url).content.decode('utf-8'))
    locations = woeid_data['query']['results']['result']['locations']
    if 'woe' in locations :
        woeid = (locations['woe']['id'])
    else:
        woeid = (locations[0]['woe']['id'])
    weather_query = "select * from weather.forecast where woeid=%s and u='c' " %woeid 
    weather_url = baseurl + urllib.parse.urlencode({'q':weather_query}) + "&format=json"
    data = json.loads(requests.get(weather_url).content.decode('utf-8'))
    return data
def weather_now(input):
    data = init(input)
    weatherTitle = data['query']['results']['channel']['item']['title']
    t = "%s\n\n%s˚C %s" %(weatherTitle,data['query']['results']['channel']['item']['condition']['temp'], data['query']['results']['channel']['item']['condition']['text'])
    return t
def weather_forecast(input):
    data = init(input)
    weatherTitle = data['query']['results']['channel']['item']['title']
    t = weatherTitle + '\n'
    for i in data['query']['results']['channel']['item']['forecast']:
        t += "\n%s %s %s˚C~%s˚C %s" %(i['day'], i['date'], i['low'], i['high'], i['text'])
    return t

#weather_now("klang")
#weather_now("Hsinchu")
#weather_forecast("taipei")
