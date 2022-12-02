from flask import Flask, redirect, url_for, render_template
import requests
import requests_cache
import time

from constants import AEROAPI_KEY, AEROAPI_BASE_URL, DETROIT_CODE_ICAO, DELTA_CODE_ICAO
from utils import open_cache, save_cache, build_cache

app = Flask(__name__)
requests_cache.install_cache(
    './database/flight_data_cache', backend='sqlite', expire_after=300)


@app.route('/')
def home():
    # return "Hello, world!  This is the homepage."
    return render_template('data.html', content=getData())

def getData():
    payload = {'max_pages': 2}
    auth_header = {'x-apikey': AEROAPI_KEY}
    # url = AEROAPI_BASE_URL + f"airports/{DETROIT_CODE_ICAO}/flights"
    url = AEROAPI_BASE_URL + f"operators/{DELTA_CODE_ICAO}/flights"

    response = requests.get(url, params=payload, headers=auth_header)
    now = time.ctime(int(time.time()))
    print(f"Time: {now}, Used Cache: {response.from_cache}")

    build_cache(response)

    if response.status_code == 200:
        return response.json()
    else:
        print('Error -- unable to execute request')


if __name__ == "__main__":
    app.run(debug=True)
