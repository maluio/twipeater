import datetime
from unittest import mock

from twipeater import fetch_tweets


def test_fetch_tweets(client, make_raw_tweet):
    with mock.patch('twipeater._fetch_raw_tweets') as fetch_raw:
        tw1 = make_raw_tweet

        fetch_raw.return_value = [tw1]

        result = fetch_tweets('foo', datetime.datetime(2020, 3, 4, 0, 0, 0))

        assert len(result) == 1
        assert result[0]['']
