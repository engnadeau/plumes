from pathlib import Path
import pytest


RESOURCES_DIR = Path(__file__).parent / "resources"


@pytest.fixture
def friends_path():
    return RESOURCES_DIR / "test-friends.json"


@pytest.fixture
def tweets_path():
    return RESOURCES_DIR / "test-tweets.json"
