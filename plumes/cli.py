import datetime
import email.utils as eu
import json
import logging
import logging.config
from pathlib import Path
from typing import Optional

import fire

import plumes.utilities as pu
from plumes.config import settings

logging.config.dictConfig(settings.logging)
LOGGER = logging.getLogger("plumes")


def check_config():
    print(json.dumps(settings.as_dict(), indent=4, sort_keys=True))


def friends(
    screen_name: Optional[str] = None,
    limit: Optional[int] = None,
    output: Optional[str] = None,
):
    """Get JSON array of friends

    Args:
        screen_name (Optional[str], optional): Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
        limit (Optional[int], optional): Max number of users to fetch. Defaults to None.
        output (Optional[str], optional): Output path for JSON file. Defaults to None.
    """
    # get api and user object
    api = pu.get_api()
    source_user = pu.get_user(screen_name=screen_name, api=api)

    # check limit for progress bar
    if not limit:
        limit = source_user.friends_count

    # ensure output location
    fname = f"{source_user.screen_name}-friends.json"
    path = pu.set_output(fname=fname, path=output)

    # get users
    LOGGER.info(f"Fetching {limit} friends")
    pu.get_tweepy_objects(
        func=api.friends, screen_name=screen_name, output=path, total=limit
    )


def followers(
    screen_name: Optional[str] = None,
    limit: Optional[int] = None,
    output: Optional[str] = None,
):
    """Get JSON array of followers

    Args:
        screen_name (Optional[str], optional): Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
        limit (Optional[int], optional): Max number of users to fetch. Defaults to None.
        output (Optional[str], optional): Output path for JSON file. Defaults to None.
    """
    # get api and user object
    api = pu.get_api()
    source_user = pu.get_user(screen_name=screen_name, api=api)

    # check limit for progress bar
    if not limit:
        limit = source_user.followers_count

    # ensure output location
    fname = f"{source_user.screen_name}-followers.json"
    path = pu.set_output(fname=fname, path=output)

    # get users
    LOGGER.info(f"Fetching {limit} followers")
    pu.get_tweepy_objects(
        func=api.followers, screen_name=screen_name, output=path, total=limit
    )


def tweets(
    screen_name: Optional[str] = None,
    limit: Optional[int] = None,
    output: Optional[str] = None,
):
    # get api and user object
    api = pu.get_api()
    source_user = pu.get_user(screen_name=screen_name, api=api)

    # check limit for progress bar
    if not limit:
        limit = source_user.statuses_count

    # ensure output location
    fname = f"{source_user.screen_name}-tweets.json"
    path = pu.set_output(fname=fname, path=output)

    # get tweets
    LOGGER.info(f"Fetching {limit} tweets")
    pu.get_tweepy_objects(
        func=api.user_timeline, screen_name=screen_name, output=path, total=limit
    )


def prune_friends(  # noqa C901
    path: str,
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    min_friends: Optional[int] = None,
    max_friends: Optional[int] = None,
    days: Optional[int] = None,
    min_tweets: Optional[int] = None,
    max_tweets: Optional[int] = None,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
    execute: bool = False,
):
    """Prune friends given criteria

    Args:
        path (str): Path to JSON file of users (e.g., output of friends())
        min_followers (Optional[int], optional): Min number of followers. Defaults to None.
        max_followers (Optional[int], optional): Max number of followers. Defaults to None.
        min_friends (Optional[int], optional): Min number of friends. Defaults to None.
        max_friends (Optional[int], optional): Max number of friends. Defaults to None.
        days (Optional[int], optional): Days since last tweet. Defaults to None.
        min_tweets (Optional[int], optional): Min number of tweets. Defaults to None.
        max_tweets (Optional[int], optional): Max number of tweets. Defaults to None.
        min_ratio (Optional[float], optional): Min Twitter follower-friend (TFF) ratio. Defaults to None.
        max_ratio (Optional[float], optional): Max Twitter follower-friend (TFF) ratio. Defaults to None.
        execute (bool, optional): Actually perform the unfollowing. If False, only a dry-run is performed. Defaults to False.
    """

    # load users data
    path = Path(path)
    with open(path) as f:
        users = json.load(f)
    LOGGER.info(f"Loaded {len(users)} users")

    # init list of users to prune
    prunable = set()

    # iterate and identify prunable users
    for u in users:
        if min_followers:
            if u["followers_count"] < min_followers:
                LOGGER.info(f"{u['screen_name']} has {u['followers_count']} followers")
                prunable.add(u["screen_name"])
        if max_followers:
            if u["followers_count"] > max_followers:
                LOGGER.info(f"{u['screen_name']} has {u['followers_count']} followers")
                prunable.add(u["screen_name"])
        if min_friends:
            if u["friends_count"] < min_friends:
                LOGGER.info(f"{u['screen_name']} has {u['friends_count']} friends")
                prunable.add(u["screen_name"])
        if max_friends:
            if u["friends_count"] > max_friends:
                LOGGER.info(f"{u['screen_name']} has {u['friends_count']} friends")
                prunable.add(u["screen_name"])
        if days:
            today = datetime.date.today()
            limit = today - datetime.timedelta(days=days)
            last_tweet = eu.parsedate_to_datetime(u["status"]["created_at"])
            if last_tweet.date() < limit:
                LOGGER.info(f"{u['screen_name']} last tweeted on {last_tweet}")
                prunable.add(u["screen_name"])
        if min_tweets:
            if u["statuses_count"] < min_tweets:
                LOGGER.info(f"{u['screen_name']} has {u['statuses_count']} tweets")
                prunable.add(u["screen_name"])
        if max_tweets:
            if u["statuses_count"] > max_tweets:
                LOGGER.info(f"{u['screen_name']} has {u['statuses_count']} tweets")
                prunable.add(u["screen_name"])
        if min_ratio:
            actual_ratio = u["followers_count"] / u["friends_count"]
            if actual_ratio < min_ratio:
                LOGGER.info(f"{u['screen_name']} has a TFF ratio of {actual_ratio}")
                prunable.add(u["screen_name"])
        if max_ratio:
            actual_ratio = u["followers_count"] / u["friends_count"]
            if actual_ratio > max_ratio:
                LOGGER.info(f"{u['screen_name']} has a TFF ratio of {actual_ratio}")
                prunable.add(u["screen_name"])

    LOGGER.info(f"Identified {len(prunable)} prunable users")
    if execute:
        for u in prunable:
            LOGGER.info(f"Unfollowing {u}")
            pu.get_twitter_api().destroy_friendship(u)


def prune_tweets(  # noqa C901
    path: str,
    days: Optional[int] = None,
    min_likes: Optional[int] = None,
    max_likes: Optional[int] = None,
    min_retweets: Optional[int] = None,
    max_retweets: Optional[int] = None,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
    protect_favorited: bool = False,
    execute: bool = False,
):
    """Prune tweets given criteria

    Args:
        days (Optional[int], optional): Days since tweeted. Defaults to None.
        min_likes (Optional[int], optional): Min number of favourites. Defaults to None.
        max_likes (Optional[int], optional): Max number of favourites. Defaults to None.
        min_retweets (Optional[int], optional): Min number of retweets. Defaults to None.
        max_retweets (Optional[int], optional): Max number of retweets. Defaults to None.
        min_ratio (Optional[float], optional): Min Twitter like-retweet ratio. Defaults to None.
        max_ratio (Optional[float], optional): Max Twitter like-retweet ratio. Defaults to None.
        protect_favorited (bool, optional): Protect and don't prune tweets that were self-liked. Defaults to False.
        execute (bool, optional): Actually perform the prune. If False, only a dry-run is performed. Defaults to False.
    """
    # load data
    path = Path(path)
    with open(path) as f:
        tweets = json.load(f)
    LOGGER.info(f"Loaded {len(tweets)} tweets")

    # init set of users to prune
    prunable = set()

    # iterate and identify prunable users
    for t in tweets:
        if days:
            today = datetime.date.today()
            limit = today - datetime.timedelta(days=days)
            tweet_dt = eu.parsedate_to_datetime(t["created_at"])
            if tweet_dt.date() < limit:
                LOGGER.info(f"\"{t['text']}\" tweeted on {tweet_dt}")
                prunable.add(t["id_str"])
        if min_likes:
            if t["favorite_count"] < min_likes:
                LOGGER.info(f"\"{t['text']}\" has {t['favorite_count']} likes")
                prunable.add(t["id_str"])
        if max_likes:
            if t["favorite_count"] > max_likes:
                LOGGER.info(f"\"{t['text']}\" has {t['favorite_count']} likes")
                prunable.add(t["id_str"])
        if min_retweets:
            if t["retweet_count"] < min_retweets:
                LOGGER.info(f"\"{t['text']}\" has {t['retweet_count']} retweets")
                prunable.add(t["id_str"])
        if max_retweets:
            if t["retweet_count"] > max_retweets:
                LOGGER.info(f"\"{t['text']}\" has {t['retweet_count']} retweets")
                prunable.add(t["id_str"])
        if min_ratio:
            actual_ratio = t["favorite_count"] / t["retweet_count"]
            if actual_ratio < min_ratio:
                LOGGER.info(f"\"{t['text']}\" has a TLR ratio of {actual_ratio}")
                prunable.add(t["id_str"])
        if max_ratio:
            actual_ratio = t["favorite_count"] / t["retweet_count"]
            if actual_ratio > max_ratio:
                LOGGER.info(f"\"{t['text']}\" has a TLR ratio of {actual_ratio}")
                prunable.add(t["id_str"])

        # must come last
        # pop pruneable tweets that are self-liked (i.e., favorited)
        if protect_favorited:
            if t["favorited"] and (t["id_str"] in prunable):
                LOGGER.info(f"\"{t['text']}\" is self-liked, protecting tweet")
                prunable.remove(t["id_str"])

    LOGGER.info(f"Identified {len(prunable)} prunable tweets")
    if execute:
        for t in prunable:
            LOGGER.info(f"Deleting {t}")
            pu.get_twitter_api().destroy_status(t)


def main():
    fire.Fire()


if __name__ == "__main__":
    pass
