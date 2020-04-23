# Day 09 ~ 10.
import os
import requests
import traceback
from flask import Flask, render_template, request

root_dir = os.path.abspath(os.path.dirname(__file__))

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id: str) -> str:
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine", template_folder=f'{root_dir}/templates')


def get_news_list_data(order_by: str) -> None:
    global db
    list_url = popular
    if order_by == 'new':
        list_url = new
    response = requests.get(list_url)
    data_dict = response.json()

    db[order_by] = data_dict['hits']


def get_news_details_data(id: str) -> None:
    global db
    detail_url = make_detail_url(id)
    response = requests.get(detail_url)
    data_dict = response.json()

    detail = {
        'title': data_dict['title'],
        'points': data_dict['points'],
        'author': data_dict['author'],
        'url': data_dict['url'],
        'children': data_dict['children'],
    }
    db['details'][id] = detail


@app.route('/', methods=['GET'])
def get_news_list():
    order_by: str = request.args.get('order_by', str)
    order_by = 'new' if order_by == 'new' else 'popular'

    if not db.get(order_by, None):
        get_news_list_data(order_by)

    articles = db[order_by]
    return render_template('index.html', order_by=order_by, articles=articles)


@app.route('/<string:id>', methods=["GET"])
def get_news_details(id: str):
    if not db.get('details', None):
        db['details'] = {}

    if not db['details'].get(id, None):
        get_news_details_data(id)

    detail = db['details'][id]

    title = detail['title']
    points = detail['points']
    author = detail['author']
    url = detail['url']
    children = detail['children']
    return render_template(
        'detail.html', title=title, points=points, author=author, url=url, children=children
    )


app.run(host="0.0.0.0")
