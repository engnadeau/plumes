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
        except tweepy.RateLimitError:
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

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        if path.is_dir():
            path / fname

    else:
        path = Path.cwd() / fname

    LOGGER.info(f"Output path: {path.resolve()}")

    return path


def get_connected_users(func, screen_name: str, output: Path, total: int):
    # get users
    LOGGER.info(f"Fetching {total} users")
    users = []
    with tqdm(total=total) as pbar:
        for f in rate_limit_handler(
            tweepy.Cursor(func, screen_name=screen_name).items(total)
        ):
            users.append(f)
            pbar.update(1)

    # dump output
    users_to_json(users=users, path=output)


def users_to_json(users: List[tweepy.User], path: Path):
    users = [u._json for u in users]
    with open(path, "w") as f:
        json.dump(users, f, indent=4)


def get_user(screen_name: Optional[str], api: tweepy.API):
    if screen_name:
        user = api.get_user(screen_name)
    else:
        user = api.me()
    return user
