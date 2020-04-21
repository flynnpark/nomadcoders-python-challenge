# Day 09 ~ 10.
import os
import requests
from flask import Flask, render_template, request

root_dir = os.path.abspath(os.path.dirname(__file__))

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine", template_folder=f'{root_dir}/templates')


def get_news_list(order_by: str) -> None:
    global db
    url = popular
    if order_by == 'new':
        url = new
    response = requests.get(url)
    data_dict = response.json()
    articles = data_dict['hits']

    db[order_by] = articles


@app.route('/', methods=['GET'])
def get_news():
    order_by: str = request.args.get('order_by', str)
    order_by = 'new' if order_by == 'new' else 'popular'

    if not db.get(order_by, None):
        get_news_list(order_by)

    articles = db[order_by]

    return render_template('index.html', order_by=order_by, articles=articles)


app.run(host="0.0.0.0")
