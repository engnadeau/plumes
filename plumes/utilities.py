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


def get_tweepy_objects(func, screen_name: str, output: Path, total: int):
    # get users
    objs = []
    with tqdm(total=total) as pbar:
        for o in rate_limit_handler(
            tweepy.Cursor(func, screen_name=screen_name).items(total)
        ):
            objs.append(o)
            pbar.update(1)

    # dump output
    tweepy_to_json(models=objs, path=output)


def tweepy_to_json(models: List, path: Path):
    models = [m._json for m in models]
    with open(path, "w") as f:
        json.dump(models, f, indent=4)


def get_user(screen_name: Optional[str], api: tweepy.API):
    if screen_name:
        user = api.get_user(screen_name)
    else:
        user = api.me()
    return user
