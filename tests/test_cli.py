import plumes.cli as pc
import sys


def test_init(tmp_path):
    # test basic function
    pc.init()

    # test force with temp file
    path = tmp_path / "tmp.toml"
    pc.init(force=True, path=path)


def test_check_config():
    pc.check_config()


def test_friends():
    pc.friends(limit=10)


def test_followers():
    pc.followers(limit=10)


def test_tweets():
    pc.tweets(limit=10)


def test_prune_friends(friends_path):
    # run basic
    pc.prune_friends(path=friends_path)

    # run complex
    pc.prune_friends(
        path=friends_path,
        min_followers=0,
        max_followers=0,
        min_friends=0,
        max_friends=0,
        days=1,
        min_tweets=0,
        max_tweets=0,
        min_ratio=0,
        max_ratio=0,
    )

    pc.prune_friends(
        path=friends_path,
        min_followers=sys.maxsize,
        min_friends=sys.maxsize,
        min_tweets=sys.maxsize,
        min_ratio=sys.maxsize,
    )


def test_prune_tweets(tweets_path):
    # run basic
    pc.prune_tweets(path=tweets_path)

    # run complex
    pc.prune_tweets(
        path=tweets_path,
        days=1,
        min_likes=0,
        max_likes=0,
        min_retweets=0,
        max_retweets=0,
        min_ratio=0,
        max_ratio=0,
        protect_favorited=True,
    )

    pc.prune_tweets(
        path=tweets_path,
        min_likes=sys.maxsize,
        min_retweets=sys.maxsize,
        min_ratio=sys.maxsize,
        protect_favorited=False,
    )
