import datetime
import email.utils as eu
import json
import logging
import logging.config
import textwrap
from pathlib import Path
from typing import Optional

import fire
import toml
import tweepy

import plumes.utilities as pu
from plumes.config import settings, user_config_path

logging.config.dictConfig(settings.logging)
LOGGER = logging.getLogger("plumes")


def init(force: bool = False, path: Optional[str] = None):
    """Initialize your plumes configuration

    Args:
        force (bool, optional): Force overwrite of existing config file. Defaults to False.
    """

    if not path:
        path = user_config_path
    else:
        path = Path(path)

    # path exists and force option wasn't used
    if not force and path.exists():
        LOGGER.info(
            f"{path.resolve()} exists. Please use the `--force` flag if you want to overwrite."
        )
    else:
        LOGGER.info(f"Creating template config file: {path.resolve()}")
        with open(path, "w") as f:
            toml.dump(settings.default.config, f)
        LOGGER.info(
            (
                "Blank configuration created. "
                f"Please visit {settings.project_homepage} for more info. "
                f"Please visit {settings.twitter_dev_page} for your API tokens."
            )
        )


def check_config():  # pragma: no cover
    """Check and validate the current configuation.
    """
    # check env variables
    LOGGER.info("Checking config settings")
    is_valid_config = True
    for k in settings.default.config:
        if k in settings.as_dict():
            LOGGER.info(f"{k.upper()} found in settings")
        else:
            LOGGER.warning(f"{k.upper()} not found in settings!")
            is_valid_config = False

    # special message if a bad config is detected
    bad_config_message = (
        "Invalid configuration. "
        f"Please visit {settings.project_homepage} for more info. "
        f"Please visit {settings.twitter_dev_page} for your API tokens."
    )
    if not is_valid_config:
        LOGGER.warning(bad_config_message)
        return

    # check authentication
    LOGGER.info("Checking Twitter authentication")
    try:
        api = pu.get_api()
        me = api.me()
        LOGGER.info(f"Successfully authenticated as {me.screen_name}")
    except tweepy.error.TweepError:
        LOGGER.warning("Invalid authentication values!")
        LOGGER.warning(bad_config_message)


def view_config():  # pragma: no cover
    """Print the current configuration
    """
    print(
        json.dumps(
            settings.as_dict(),
            indent=4,
            sort_keys=True,
            default=lambda o: "<not serializable>",
        )
    )


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
    source_user = pu.get_user(screen_name=screen_name)

    # check limit for progress bar
    if not limit:  # pragma: no cover
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
    source_user = pu.get_user(screen_name=screen_name)

    # check limit for progress bar
    if not limit:  # pragma: no cover
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
    """Get JSON array of tweets

    Args:
        screen_name (Optional[str], optional): Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
        limit (Optional[int], optional): Max number of users to fetch. Defaults to None.
        output (Optional[str], optional): Output path for JSON file. Defaults to None.
    """
    # get api and user object
    api = pu.get_api()
    source_user = pu.get_user(screen_name=screen_name)

    # check limit for progress bar
    if not limit:  # pragma: no cover
        limit = source_user.statuses_count

    # ensure output location
    fname = f"{source_user.screen_name}-tweets.json"
    path = pu.set_output(fname=fname, path=output)

    # get tweets
    LOGGER.info(f"Fetching {limit} tweets")
    pu.get_tweepy_objects(
        func=api.user_timeline, screen_name=screen_name, output=path, total=limit
    )


def audit_users(  # noqa C901
    path: str,
    min_followers: Optional[int] = None,
    max_followers: Optional[int] = None,
    min_friends: Optional[int] = None,
    max_friends: Optional[int] = None,
    days: Optional[int] = None,
    min_tweets: Optional[int] = None,
    max_tweets: Optional[int] = None,
    min_favourites: Optional[int] = None,
    max_favourites: Optional[int] = None,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
    prune: bool = False,
    befriend: bool = False,
):
    """Audit and review users given criteria

    Args:
        path (str): Path to JSON file of users (e.g., output of friends())
        min_followers (Optional[int], optional): Min number of followers. Defaults to None.
        max_followers (Optional[int], optional): Max number of followers. Defaults to None.
        min_friends (Optional[int], optional): Min number of friends. Defaults to None.
        max_friends (Optional[int], optional): Max number of friends. Defaults to None.
        days (Optional[int], optional): Days since last tweet. Defaults to None.
        min_tweets (Optional[int], optional): Min number of tweets. Defaults to None.
        max_tweets (Optional[int], optional): Max number of tweets. Defaults to None.
        min_favourites (Optional[int], optional): Min number of favourites. Defaults to None.
        max_favourites (Optional[int], optional): Max number of favourites. Defaults to None.
        min_ratio (Optional[float], optional): Min Twitter follower-friend (TFF) ratio. Defaults to None.
        max_ratio (Optional[float], optional): Max Twitter follower-friend (TFF) ratio. Defaults to None.
        prune (bool, optional): Unfollow identified users. Defaults to False.
        befriend (bool, optional): Follow identified users. Defaults to False.
    """

    # load users data
    path = Path(path)
    with open(path) as f:
        users = json.load(f)
    LOGGER.info(f"Loaded {len(users)} users")

    # init list of users to prune
    identified_users = set()

    # iterate and identify prunable users
    for u in users:
        failed_clauses = []

        if min_followers is not None:
            failed_clauses.append(u["followers_count"] < min_followers)

        if max_followers is not None:
            failed_clauses.append(u["followers_count"] > max_followers)

        if min_friends is not None:
            failed_clauses.append(u["friends_count"] < min_friends)

        if max_friends is not None:
            failed_clauses.append(u["friends_count"] > max_friends)

        if days is not None:
            today = datetime.date.today()
            limit = today - datetime.timedelta(days=days)
            try:
                last_tweet = eu.parsedate_to_datetime(u["status"]["created_at"])
                failed_clauses.append(last_tweet.date() < limit)
            except KeyError:
                # no tweets
                failed_clauses.append(True)

        if min_tweets is not None:
            failed_clauses.append(u["statuses_count"] < min_tweets)

        if max_tweets is not None:
            failed_clauses.append(u["statuses_count"] > max_tweets)

        if min_favourites is not None:
            failed_clauses.append(u["favourites_count"] < min_favourites)

        if max_favourites is not None:
            failed_clauses.append(u["favourites_count"] > max_favourites)

        if min_ratio is not None:
            failed_clauses.append(
                pu.calculate_tff_ratio(
                    followers=u["followers_count"], friends=u["friends_count"]
                )
                < min_ratio
            )

        if max_ratio is not None:
            failed_clauses.append(
                pu.calculate_tff_ratio(
                    followers=u["followers_count"], friends=u["friends_count"]
                )
                > max_ratio
            )

        if len(failed_clauses) > 0 and all(failed_clauses):
            LOGGER.info(f"Identified {u['screen_name']}")
            identified_users.add(u["screen_name"])

    LOGGER.info(f"Identified {len(identified_users)} users")
    if prune:
        for u in identified_users:
            LOGGER.info(f"Unfollowing {u}")
            pu.get_api().destroy_friendship(u)
    if befriend:
        for u in identified_users:
            LOGGER.info(f"Following {u}")
            pu.get_api().create_friendship(u)


def audit_tweets(  # noqa C901
    path: str,
    days: Optional[int] = None,
    min_likes: Optional[int] = None,
    max_likes: Optional[int] = None,
    min_retweets: Optional[int] = None,
    max_retweets: Optional[int] = None,
    min_ratio: Optional[float] = None,
    max_ratio: Optional[float] = None,
    self_favorited: Optional[bool] = None,
    prune: bool = False,
    favorite: bool = False,
):
    """Audit and review tweets given criteria

    Args:
        days (Optional[int], optional): Days since tweeted. Defaults to None.
        min_likes (Optional[int], optional): Min number of favourites. Defaults to None.
        max_likes (Optional[int], optional): Max number of favourites. Defaults to None.
        min_retweets (Optional[int], optional): Min number of retweets. Defaults to None.
        max_retweets (Optional[int], optional): Max number of retweets. Defaults to None.
        min_ratio (Optional[float], optional): Min Twitter like-retweet ratio. Defaults to None.
        max_ratio (Optional[float], optional): Max Twitter like-retweet ratio. Defaults to None.
        self_favorited (Optional[bool], optional): Check if tweet is self-liked. Defaults to None.
        prune (bool, optional): Prune and destroy identified tweets. Defaults to False.
        favorite (bool, optional): Like identified tweets. Defaults to False.
    """
    # load data
    path = Path(path)
    with open(path) as f:
        tweets = json.load(f)
    LOGGER.info(f"Loaded {len(tweets)} tweets")

    # init set of users to prune
    identified_tweets = set()

    # iterate and identify prunable users
    for t in tweets:
        text = textwrap.shorten(t["text"], width=settings.textwrap_width)
        failed_clauses = []

        if days is not None:
            today = datetime.date.today()
            limit = today - datetime.timedelta(days=days)
            tweet_dt = eu.parsedate_to_datetime(t["created_at"])
            failed_clauses.append(tweet_dt.date() < limit)

        if min_likes is not None:
            failed_clauses.append(t["favorite_count"] < min_likes)

        if max_likes is not None:
            failed_clauses.append(t["favorite_count"] > max_likes)

        if min_retweets is not None:
            failed_clauses.append(t["retweet_count"] < min_retweets)

        if max_retweets is not None:
            failed_clauses.append(t["retweet_count"] > max_retweets)

        if min_ratio is not None:
            failed_clauses.append(
                pu.calculate_like_retweet_ratio(
                    likes=t["favorite_count"], retweets=t["retweet_count"]
                )
                < min_ratio
            )

        if max_ratio is not None:
            failed_clauses.append(
                pu.calculate_like_retweet_ratio(
                    likes=t["favorite_count"], retweets=t["retweet_count"]
                )
                > max_ratio
            )

        if self_favorited is not None:
            failed_clauses.append(t["favorited"] == self_favorited)

        if len(failed_clauses) > 0 and all(failed_clauses):
            LOGGER.info(f'Identified "{text}"')
            identified_tweets.add(t["id_str"])

    LOGGER.info(f"Identified {len(identified_tweets)} tweets")
    if prune:
        for t in identified_tweets:
            LOGGER.info(f"Deleting {t}")
            pu.get_api().destroy_status(t)
    if favorite:
        for t in identified_tweets:
            LOGGER.info(f"Favoriting {t}")
            pu.get_api().create_favorite(t)


def view_user(user: str):
    """View a user's raw JSON

    Args:
        user (str): User's screen name
    """
    user = pu.get_api().get_user(user)
    print(
        json.dumps(
            user._json,
            indent=4,
            sort_keys=True,
            default=lambda o: "<not serializable>",
        )
    )


def main():
    fire.Fire()
