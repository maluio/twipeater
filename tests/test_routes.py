import datetime
from unittest import mock

import feedparser
from twint.tweet import tweet

from twipeater import RemoteHostException, Tweet


def test_404(client):
    r = client.get('/fooobaar')

    assert r.status_code == 404


def test_no_username_404(client):
    r = client.get('/tweets')

    assert r.status_code == 404


def test_unsupported_method(client):
    r = client.post('/tweets/foo.json')

    assert r.status_code == 405


def test_unsupported_suffix(client):
    r = client.get('/tweets/foo.bar')

    assert r.status_code == 400


def test_non_existing_username(client):
    r = client.get('/tweets/username.json')

    assert len(r.json['tweets']) == 0


def test_get_tweets(client, make_tweet):
    tw1 = make_tweet

    with mock.patch('twipeater.fetch_tweets') as fetch_tweets:
        fetch_tweets.return_value = [
            tw1
        ]

        r = client.get('/tweets/foo.json')
        fetch_tweets.assert_called_with('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))

        assert r.json['tweets'][0]['id'] == 1
        assert r.json['tweets'][0]['link'] == 'https://twitter.com/12345'


def test_get_tweets_error(client, make_tweet):
    with mock.patch('twipeater.fetch_tweets') as fetch_tweets:
        fetch_tweets.side_effect = RemoteHostException()

        r = client.get('/tweets/foo.json')

        assert r.json['error'] == 'Tweets could not be fetched for this username'


def test_get_atom(client):
    t = tweet()
    t.id = 1
    t.published_at = datetime.datetime(2020, 3, 4, 0, 0, 0)
    t.hashtags = []
    t.link = 'https://twitter.com/12345'
    t.tweet = 'I am the tweet content'
    t.likes_count = 1
    t.name = ''
    t.replies_count = 1
    t.retweets_count = 1
    t.thumbnail = ''

    t2 = tweet()
    t2.id = 2
    t2.published_at = datetime.datetime(2021, 3, 4, 0, 0, 0)
    t2.hashtags = []
    t2.link = 'https://twitter.com/555'
    t2.tweet = 'I am the second tweet content'
    t2.likes_count = 1
    t2.name = ''
    t2.replies_count = 1
    t2.retweets_count = 1
    t2.thumbnail = ''

    with mock.patch('twipeater.fetch_tweets') as fetch_tweets:
        fetch_tweets.return_value = [
            Tweet.from_orm(t),
            Tweet.from_orm(t2)
        ]

        r = client.get('/tweets/foo.atom')
        assert r.content_type == 'application/atom+xml; charset=utf-8'

        atom = r.data.decode("utf-8")
        fr = feedparser.parse(atom)
        items = fr.entries

        assert fr.feed.title == 'foo (Twipeater)'
        assert fr.feed.id == 'twipeater_tweets_foo'

        assert len(items) == 2

        assert items[0]['title'] == 'I am the tweet content'
        assert items[0]['link'] == 'https://twitter.com/12345'
        assert items[0]['description'] == 'I am the tweet content'
        assert items[0]['published'] == '2020-03-04T00:00:00'

        assert items[1]['title'] == 'I am the second tweet content'
        assert items[1]['link'] == 'https://twitter.com/555'
        assert items[1]['description'] == 'I am the second tweet content'
        assert items[1]['published'] == '2021-03-04T00:00:00'
