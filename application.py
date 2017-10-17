import requests, json, giphypop
from threading import Thread
from flask import Flask, render_template, request


def googleReq(address):
    key='AIzaSyARvDzNmxTTcVfrn0o86aeqeI0ItlXmyOE'
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {'query': address,'key': key}
    req = requests.get(url, params=params, verify=False)
    if req.status_code == 200:
        return req.json()['results'][:20]
    return []


def giphyReqAsync(place,usedGifs):
    giphyKey = '3fnIrrGp6FRqCVS7tOGYoHl9JSGnzApD'
    notFoundGif = 'xTiN0L7EW5trfOvEk0'
    giphy = giphypop.Giphy(api_key=giphyKey)
    gifs = giphy.search(term=place['name'],limit=20)
    try:
        gif = next(gifs)['id']
        while gif in usedGifs:
            gif = next(gifs)['id']
        usedGifs.add(gif)
        place['gif'] = gif

    except StopIteration:
        place['gif'] = notFoundGif


application = Flask(__name__)


@application.route('/')
def home():
    return render_template("home.html")


@application.route('/address/', methods=['POST'])
def addressPost():
    
    address = json.loads(request.data.decode('utf-8'))['address']
    places = googleReq(address)
    usedGifs = set()

    # creating multiple threads to handle the requests (max 20) asynchronously
    # this threads will update the contents of the variables places and usedGifs
    threads = [None]*len(places)
    for i, place in enumerate(places):
        threads[i] = Thread(target=giphyReqAsync, args=(place,usedGifs))
        threads[i].start()
    for thread in threads:
        thread.join()

    return json.dumps(places)


if __name__ == "__main__":
    application.debug = False
    application.run()