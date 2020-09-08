import json

import plumes.cli as pc


def test_check_config():
    pc.check_config()


def test_friends():
    pc.friends(limit=10)


def test_followers():
    pc.followers(limit=10)


def test_tweets():
    pc.tweets(limit=10)


def test_init(tmp_path):
    # test basic function
    pc.init()

    # test force with temp file
    path = tmp_path / "tmp.toml"
    pc.init(force=True, path=path)


def test_audit_users(users_path):
    # run basic
    pc.audit_users(path=users_path)

    # run complex
    pc.audit_users(
        path=users_path,
        min_followers=0,
        max_followers=0,
        min_friends=0,
        max_friends=0,
        min_favourites=0,
        max_favourites=0,
        days=1,
        min_tweets=0,
        max_tweets=0,
        min_ratio=0,
        max_ratio=0,
    )

    pc.audit_users(
        path=users_path,
        min_followers=float("inf"),
        min_friends=float("inf"),
        min_tweets=float("inf"),
        min_ratio=float("inf"),
    )


def test_audit_tweets(tweets_path):
    # run basic
    pc.audit_tweets(path=tweets_path)

    # run complex
    pc.audit_tweets(
        path=tweets_path,
        days=1,
        min_likes=0,
        max_likes=0,
        min_retweets=0,
        max_retweets=0,
        min_ratio=0,
        max_ratio=0,
        self_favorited=True,
    )

    pc.audit_tweets(
        path=tweets_path,
        min_likes=float("inf"),
        min_retweets=float("inf"),
        min_ratio=float("inf"),
        self_favorited=False,
    )


def test_view_user():
    users = ["EngNadeau", "ConanOBrien", "alyankovic", "SteveMartinToGo"]

    for u in users:
        pc.view_user(u)
