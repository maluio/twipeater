import datetime
from unittest import mock



def test_404(client):
    r = client.get('/fooobaar')

    assert r.status_code == 404


def test_no_username_error(client):
    r = client.get('/tweets')

    assert r.status_code == 400
    assert r.json['message'] == "Parameter 'username' is required"


def test_non_existing_username(client):
    r = client.get('/tweets?username=foo')

    assert len(r.json['tweets']) == 0


def test_get_tweets(client, make_tweet):
    tw1 = make_tweet

    with mock.patch('twipeater.fetch_tweets') as fetch_tweets:
        fetch_tweets.return_value = [
            tw1
        ]

        r = client.get('/tweets?username=foo')
        fetch_tweets.assert_called_with('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))

        assert r.json['tweets'][0]['id'] == 1
        assert r.json['tweets'][0]['link'] == 'https://twitter.com/12345'
