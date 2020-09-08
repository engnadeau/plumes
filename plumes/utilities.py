import json
import logging
import time
from pathlib import Path
from typing import List, Optional

import tweepy
from tqdm import tqdm

from plumes.config import settings

LOGGER = logging.getLogger("plumes")


def rate_limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:  # pragma: no cover
            LOGGER.info(f"Rate limit exceeded; sleeping for {settings.sleep_time}s")
            time.sleep(settings.sleep_time)
        except StopIteration:
            break


def get_api():
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    return api


def set_output(fname: str, path: Optional[str]):
    if path:
        path = Path(path)

        if not path.exists():  # pragma: no cover
            path.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            path / fname

    else:
        path = Path.cwd() / fname

    LOGGER.info(f"Output path: {path.resolve()}")

    return path


def get_tweepy_objects(
    func, screen_name: str, output: Path, total: int, count: int = 200
):
    # get users
    objs = []
    with tqdm(total=total) as pbar:
        for o in rate_limit_handler(
            tweepy.Cursor(func, screen_name=screen_name, count=count).items(total)
        ):
            objs.append(o)
            pbar.update(1)

    # dump output
    tweepy_to_json(models=objs, path=output)


def tweepy_to_json(models: List, path: Path):
    models = [m._json for m in models]
    with open(path, "w") as f:
        json.dump(models, f, indent=4)


def get_user(screen_name: Optional[str] = None):
    if screen_name:
        user = get_api().get_user(screen_name)
    else:
        user = get_api().me()
    return user


def calculate_like_retweet_ratio(likes: int, retweets: int) -> float:
    if likes == 0:
        ratio = 0
    elif retweets == 0:
        ratio = float("inf")
    else:
        ratio = likes / retweets

    return ratio


def calculate_tff_ratio(followers: int, friends: int) -> float:
    if followers == 0:
        ratio = 0
    elif friends == 0:
        ratio = float("inf")
    else:
        ratio = followers / friends

    return ratio
