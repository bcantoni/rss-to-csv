import json
import logging
import os
import re
import requests


def geoIP(ip):
    ''' convert IP address into location '''
    return 'N/A'
    matches = re.search(r"^(\d+\.\d+\.\d+\.\d+):", ip)
    if matches:
        ip = matches[1]
        logging.info(f"geoIP called for {ip}")
        if 'IPSTACK_ACCESS_KEY' in os.environ:
            access_key = os.environ['IPSTACK_ACCESS_KEY']
            url = f"http://api.ipstack.com/{ip}?access_key={access_key}&format=1"
            req = requests.get(url)
            if req.status_code != 200:
                return 'Error looking up IP address'
            logging.info(req.content.decode('utf-8'))
            data = json.loads(req.content.decode('utf-8'))
            msg = f"{data['city']}, {data['region_name']} ({data['country_code']})"
            return msg
        else:
            return ''
    else:
        return 'Bad IP address given'
