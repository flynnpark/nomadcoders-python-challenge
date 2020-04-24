import os
import requests
from typing import List, Dict
from operator import itemgetter
from flask import Flask, render_template, request
from bs4 import BeautifulSoup

root_dir = os.path.abspath(os.path.dirname(__file__))
subreddit_url = "https://www.reddit.com/r/{subreddit}/top/?t=month"

"""
When you try to scrape reddit make sure to send the 'headers' on your request.
Reddit blocks scrappers so we have to include these headers to make reddit think
that we are a normal computer and not a python script.
How to use: requests.get(url, headers=headers)
"""

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
}


"""
All subreddits have the same url:
i.e : https://reddit.com/r/javascript
You can add more subreddits to the list, just make sure they exist.
To make a request, use this url:
https://www.reddit.com/r/{subreddit}/top/?t=month
This will give you the top posts in per month.
"""

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django",
]


def soup_subreddit_page(subreddit_name: str) -> BeautifulSoup:
    try:
        response = requests.get(subreddit_url.format(subreddit=subreddit_name), headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        return soup

    except Exception as e:
        print(e)


app = Flask("DayEleven", template_folder=f"{root_dir}/templates")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", subreddits=subreddits)


@app.route("/read", methods=["GET"])
def read():
    subreddit_names = request.args.to_dict()

    post_list = []
    for subreddit_name in subreddit_names:
        soup = soup_subreddit_page(subreddit_name)
        post_elements = soup.select("div.rpBJOHq2PR60pnwJlUyP0 > div")

        for post_element in post_elements:
            title = post_element.select_one(
                "div.y8HYJ-y_lTUHkQIc1mdCq._2INHSNB8V5eaWp4P0rY_mE"
            ).text
            url = post_element.select_one("a").get("href")
            votes = post_element.select_one("div._1rZYMD_4xY3gRcSS3p8ODO").text
            votes_count = (
                int(votes) if not "k" in votes else int(float(votes.replace("k", "")) * 1000)
            )

            post = {
                "subreddit_name": subreddit_name,
                "title": title,
                "url": url,
                "votes": votes,
                "votes_count": votes_count,
            }
            post_list.append(post)

    post_list = sorted(post_list, key=itemgetter("votes_count"), reverse=True)

    return render_template("read.html", subreddit_names=subreddit_names, post_list=post_list)


app.run(host="0.0.0.0", use_reloader=False)
