import datetime
from unittest import mock

import pytest

from twipeater import fetch_tweets, RemoteHostException, DeserializeException


def test_fetch_tweets(client, make_raw_tweet):
    with mock.patch('twipeater._fetch_raw_tweets') as fetch_raw:
        tw1 = make_raw_tweet

        fetch_raw.return_value = [tw1]

        result = fetch_tweets('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))

        assert len(result) == 1


def test_fetch_tweets_exception(client, make_raw_tweet):
    with mock.patch('twipeater._fetch_raw_tweets') as fetch_raw:
        fetch_raw.side_effect = Exception()

        with pytest.raises(RemoteHostException):
            fetch_tweets('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))


def test_tweet_deserialize_exception(client, make_raw_tweet):
    with mock.patch('twipeater._fetch_raw_tweets') as fetch_raw:
        tw1 = make_raw_tweet
        tw1.datetime = 'i am not a datetime string'
        fetch_raw.return_value = [tw1]

        with pytest.raises(DeserializeException):
            fetch_tweets('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))
