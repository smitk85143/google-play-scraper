import json
import requests
from google_play_scraper.constants.google_play import PLAY_STORE_BASE_URL

def suggest_keyword(keyword, **opts):
    if not keyword:
        raise ValueError('term missing')

    lang = opts.get('lang', 'en')
    country = opts.get('country', 'us')

    url = f"{PLAY_STORE_BASE_URL}/_/PlayStoreUi/data/batchexecute?rpcids=IJ4APc&f.sid=-697906427155521722&bl=boq_playuiserver_20190903.08_p0&hl={lang}&gl={country}&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=1065213"

    term = requests.utils.quote(keyword)
    body = f"f.req=%5B%5B%5B%22IJ4APc%22%2C%22%5B%5Bnull%2C%5B%5C%22{term}%5C%22%5D%2C%5B10%5D%2C%5B2%5D%2C4%5D%5D%22%5D%5D%5D"
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
    options = {
        'url': url,
        'data': body,
        'headers': headers,
    }
    options.update(opts.get('requestOptions', {}))

    html = requests.post(**options).text
    input_data = json.loads(html[5:])
    data = json.loads(input_data[0][2])
    if data is None:
        return []
    try:
        data =  [s[0] for s in data[0][0]]
        return data
    except:
        return []