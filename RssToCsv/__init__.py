'''
RSS to CSV serverless (Azure functions)

optional environment variables:
SLACK_WEBHOOK - if present, will send status message to Slack channel
IPSTACK_ACCESS_KEY - if present, will do geo ip lookup using api.ipstack.com
'''

import azure.functions as func
import csv
import feedparser
import io
import json
import logging
import os
import re
import requests
import time


def geoIP(ip):
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


def fetchRSSandOutputCSV(url):
    ''' fetch the specified RSS feed and return in CSV format '''

    # test mode: if 3-digit "url" provided, return as an HTTP status code
    matches = re.search(r"^(\d\d\d)$", url)
    if matches:
        statuscode = matches[1]
        return func.HttpResponse(
            f"Test mode, returning status {statuscode}\n",
            status_code=statuscode
        )

    if not re.search(r"^https?:\/\/", url):
        return func.HttpResponse(
             "Invalid 'url' parameter.\n",
             status_code=400
        )

    start = time.time()
    rss = feedparser.parse(url)
    delta = int((time.time() - start) * 1000)
    logging.info(f"time-feedparser: {delta} ms")
    if rss.status not in [200, 301, 302]:
        return func.HttpResponse(
            f"Error fetching {url}: {rss.status}\n", status_code=400
        )

    output = io.StringIO()
    headers = {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": "attachment; filename=\"export.csv\"",
        "Pragma": "no-cache",
        "URL-Actual": rss.href
    }
    csv_writer = csv.writer(
        output,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_ALL
    )

    csv_writer.writerow([
        'Title',
        'Link',
        'Description',
        'pubDate',
        'guid']
    )

    for item in rss.entries:
        csv_writer.writerow([
            item.get('title', 'No Title'),
            item.get('link', ''),
            item.get('summary', ''),
            item.get('published', ''),
            item.get('id', '')
        ])

    result = output.getvalue()
    output.close()
    return func.HttpResponse(result, headers=headers)


def main(req: func.HttpRequest) -> func.HttpResponse:
    ''' main function entry point from Azure '''

    logging.info('HTTP trigger function processed a request, calling rss2csv')

    url = req.params.get('url')
    if not url:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            url = req_body.get('url')

    if url:
        logmsg = f"Processing url: {url}\n"
        interesting = [
            'client-ip',
            'x-forwarded-for',
            'accept-language',
            'user-agent'
        ]
        for key, value in req.headers.items():
            if key in interesting:
                logmsg += f"{key}: {value}\n"
        logging.info(logmsg)

        rc = fetchRSSandOutputCSV(url)

        # if configured send update to Slack room
        if 'SLACK_WEBHOOK' in os.environ:
            slackmsg = f"Feed: {url}\n"
            if 'x-forwarded-for' in req.headers:
                ip = req.headers['x-forwarded-for']
                start = time.time()
                geo = geoIP(ip)
                delta = int((time.time() - start) * 1000)
                logging.info(f"time-geoip: {delta} ms")
                slackmsg += f"Geo: {geo}\n"
            start = time.time()
            stat = requests.post(
                os.environ['SLACK_WEBHOOK'],
                json={'text': slackmsg}
            )
            delta = int((time.time() - start) * 1000)
            logging.info(f"time-slack: {delta} ms")
            logging.info(f"response code from Slack: {stat.status_code}")
        return rc
    else:
        return func.HttpResponse(
             "Please pass 'url' parameter in query request or body.\n",
             status_code=400
        )
