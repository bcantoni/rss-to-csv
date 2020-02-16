import azure.functions as func
import csv
import feedparser
import io
import logging
import os
import requests


def fetchRSSandOutputCSV(url):
    rss = feedparser.parse(url)
    if rss.status != 200:
        return func.HttpResponse(
            f"Error fetching {url}: {rss.status}\n", status_code=400
        )

    output = io.StringIO()
    headers = {
        "Content-Type": "text/csv; charset=utf-8",
        "Content-Disposition": "attachment; filename=\"export.csv\"",
        "Pragma": "no-cache"
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
        logging.info(f'Calling fetchRSSandOutputCSV for url: {url}')
        rc = fetchRSSandOutputCSV(url)
        if 'SLACK_WEBHOOK' in os.environ:
            # if configured send update to Slack room
            logging.info('Posting to Slack')
            slackmsg = f"feed: {url}\nheaders:\n"
            for key, value in req.headers.items():
                slackmsg += f"{key}: {value}\n"
            stat = requests.post(
                os.environ['SLACK_WEBHOOK'],
                json={'text': slackmsg}
            )
            logging.info(stat.status_code)
        return rc
    else:
        return func.HttpResponse(
             "Please pass a url on the query string or in the request body",
             status_code=400
        )
