from datetime import datetime, timedelta
from typing import List

from dateutil.parser import parse
from pydantic import BaseModel
from twint import Config, run, tweet
from flask import Flask, request
import xml.etree.ElementTree as ET

app = Flask(__name__)

DEFAULT_SINCE_DAYS = 7


class RemoteHostException(Exception):
    pass


class DeserializeException(Exception):
    pass


def now():
    return datetime.now()


class Tweet(BaseModel):
    id: int
    published_at: datetime
    hashtags: List[str]
    link: str
    tweet: str
    likes_count: int
    name: str
    replies_count: int
    retweets_count: int
    thumbnail: str

    class Config:
        orm_mode = True


@app.route('/tweets/rss')
def get_tweets_rss():
    pass


@app.route('/tweets')
def get_tweets():
    username = request.args.get('username', None)
    if not username:
        return {"message": "Parameter 'username' is required"}, 400

    since_days = int(request.args.get('since-days', DEFAULT_SINCE_DAYS))
    since = now() - timedelta(days=since_days)
    try:
        tweets = fetch_tweets(username, since)
    except (RemoteHostException, DeserializeException):
        return {"error": "Tweets could not be fetched for this username"}, 500

    if request.args.get('format') and request.args.get('format') == 'atom':
        return render_atom(tweets, username), 200, {'Content-Type': 'application/atom+xml; charset=utf-8'}

    data = []
    for t in tweets:
        data.append(t.dict())

    return {'tweets': data}


def fetch_tweets(username: str, since: datetime) -> List[Tweet]:
    deserialized_tweets = []

    try:
        raw_tweets = _fetch_raw_tweets(username, since)
    except Exception as e:
        app.logger.error(f'[tweets_fetch] Error fetching tweets for username {username} with message {str(e)}')
        raise RemoteHostException()

    for t in raw_tweets:
        try:
            t.published_at = parse(t.datetime)
            deserialized_tweets.append(Tweet.from_orm(t))
        except Exception as e:
            app.logger.error(
                f'[tweet_deserialize] Error deserializing tweet for username {username} with message {str(e)}')
            raise DeserializeException()

    return deserialized_tweets


def _fetch_raw_tweets(username: str, since: datetime) -> List[tweet.tweet]:
    # https://github.com/twintproject/twint#more-examples
    raw_tweets = []
    c = Config()
    c.Username = username
    c.Store_object = True
    c.Store_object_tweets_list = raw_tweets
    c.Since = since.strftime("%Y-%m-%d %H:%M:%S")
    run.Search(c)

    return raw_tweets


# https://en.wikipedia.org/wiki/Atom_(Web_standard)
def render_atom(tweets: List[Tweet], username: str) -> str:
    root = ET.Element("feed", attrib={'xmlns': "https://www.w3.org/2005/Atom"})
    ET.SubElement(root, "title").text = f'{username} (Twipeater)'
    ET.SubElement(root, "id").text = f'twipeater_tweets_{username}'
    for tw in tweets:
        entry = ET.SubElement(root, "entry")
        ET.SubElement(entry, "title").text = tw.tweet
        ET.SubElement(entry, "description").text = tw.tweet
        ET.SubElement(entry, "link").text = tw.link
        ET.SubElement(entry, "published").text = tw.published_at.isoformat()

    return ET.tostring(root, encoding='utf8', method='xml')
