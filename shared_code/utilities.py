import json
import logging
import os
import re
import requests


def geoIP(ip):
    ''' convert IP address into location '''
    matches = re.search(r"^(\d+\.\d+\.\d+\.\d+):", ip)
    if matches:
        ip = matches[1]
        logging.info(f"geoIP called for {ip}")
        if 'IPGEO_ACCESS_KEY' in os.environ:
            access_key = os.environ['IPGEO_ACCESS_KEY']
            url = f"https://api.ipgeolocation.io/ipgeo?apiKey={access_key}&fields=geo&ip={ip}"
            req = requests.get(url)
            if req.status_code != 200:
                return 'Error looking up IP address'
            logging.info(req.content.decode('utf-8'))
            data = json.loads(req.content.decode('utf-8'))
            msg = f"{data['city']}, {data['state_prov']} ({data['country_name']})"
            return msg
        else:
            return ''
    else:
        return 'Bad IP address given'
