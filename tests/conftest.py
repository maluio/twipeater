import datetime

import pytest
from dateutil.parser import parse
from twint.tweet import tweet

from twipeater import app, Tweet

DEFAULT_PUBLISHED_AT = datetime.datetime(2020, 3, 11, 0, 0, 0)


@pytest.fixture()
def test_app():
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(test_app):
    return test_app.test_client()


@pytest.fixture()
def runner(test_app):
    return test_app.test_cli_runner()


@pytest.fixture(autouse=True)
def twint(monkeypatch):
    def mock_fetch_raw_tweets(username, since):
        return []

    monkeypatch.setattr('twipeater._fetch_raw_tweets', mock_fetch_raw_tweets)


@pytest.fixture(autouse=True)
def now(monkeypatch):
    def _now():
        return DEFAULT_PUBLISHED_AT
    monkeypatch.setattr('twipeater.now', _now)


def create_tweet():
    t = tweet()
    t.id = 1
    t.datetime = '2020-03-10 22:58:01 CET'
    t.hashtags = []
    t.link = 'https://twitter.com/12345'
    t.tweet = ''
    t.likes_count = 1
    t.name = ''
    t.replies_count = 1
    t.retweets_count = 1
    t.thumbnail = ''

    return t


@pytest.fixture()
def make_raw_tweet():
    return create_tweet()


@pytest.fixture()
def make_tweet():
    tw = create_tweet()
    tw.published_at = parse(tw.datetime)
    return Tweet.from_orm(tw)
