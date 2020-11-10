<br />
<p align="center">
  <a href="https://github.com/nnadeau/plumes">
    <img src="https://raw.githubusercontent.com/nnadeau/plumes/master/media/feather.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">plumes</h3>

  <p align="center">
    Simple Twitter CLI for day-to-day social media hygiene
    <br />
    ·
    <a href="https://github.com/nnadeau/plumes/issues">Report Bug</a>
    ·
    <a href="https://github.com/nnadeau/plumes/issues">Request Feature</a>
  </p>
</p>

[![GitHub issues](https://img.shields.io/github/issues/nnadeau/plumes)](https://github.com/nnadeau/plumes/issues)
[![GitHub forks](https://img.shields.io/github/forks/nnadeau/plumes)](https://github.com/nnadeau/plumes/network)
[![GitHub stars](https://img.shields.io/github/stars/nnadeau/plumes)](https://github.com/nnadeau/plumes/stargazers)
[![GitHub license](https://img.shields.io/github/license/nnadeau/plumes)](https://github.com/nnadeau/plumes/blob/master/LICENSE)

[![PyPI Version](https://img.shields.io/pypi/v/plumes.svg)](https://pypi.python.org/pypi/plumes)
[![PyPI License](https://img.shields.io/pypi/l/plumes.svg)](https://pypi.python.org/pypi/plumes)
[![PyPI Wheel](https://img.shields.io/pypi/wheel/plumes.svg)](https://pypi.python.org/pypi/plumes)
[![PyPI Format](https://img.shields.io/pypi/format/plumes.svg)](https://pypi.python.org/pypi/plumes)
[![PyPI Pythons](https://img.shields.io/pypi/pyversions/plumes.svg)](https://pypi.python.org/pypi/plumes)
[![PyPI Implementation](https://img.shields.io/pypi/implementation/plumes.svg)](https://pypi.python.org/pypi/plumes)

[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Test](https://github.com/nnadeau/plumes/workflows/Test/badge.svg)](https://github.com/nnadeau/plumes/actions)
[![Release](https://github.com/nnadeau/plumes/workflows/Release/badge.svg)](https://github.com/nnadeau/plumes/actions)
[![Publish](https://github.com/nnadeau/plumes/workflows/Publish/badge.svg)](https://github.com/nnadeau/plumes/actions)

[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fnnadeau%2Fplumes)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fnnadeau%2Fplumes)

## Contents

- [Contents](#contents)
- [Overview](#overview)
- [Inspiration](#inspiration)
- [Installation](#installation)
- [Usage](#usage)
  - [Getting Started And Creating Your Authentication Config](#getting-started-and-creating-your-authentication-config)
  - [Export Friends](#export-friends)
  - [Export Followers](#export-followers)
  - [Export Tweets](#export-tweets)
  - [Audit Users](#audit-users)
  - [Prune Your Tweets](#prune-your-tweets)
- [Advanced Usage and Chaining](#advanced-usage-and-chaining)
  - [Extracting Screen Names of Retweeted Statuses](#extracting-screen-names-of-retweeted-statuses)
  - [Batch Follow Users of Retweeted Statuses](#batch-follow-users-of-retweeted-statuses)
- [Setting Up Authentication](#setting-up-authentication)
  - [Get Your Twitter API Tokens](#get-your-twitter-api-tokens)
  - [Configuring `plumes`](#configuring-plumes)
- [Contributing](#contributing)
- [Testing](#testing)

## Overview

`Plumes` is an open-source Python CLI app for day-to-day social media hygiene.
It was designed to provide a simple, clear, and concise interface to quickly explore and clean a personal Twitter account.

## Inspiration

[![panzer tweet](https://raw.githubusercontent.com/nnadeau/plumes/master/media/tweet-panzer.png)](https://twitter.com/panzer/status/943935357673861120)

[![chrisalbon tweet](https://raw.githubusercontent.com/nnadeau/plumes/master/media/tweet-chrisalbon.png)](https://twitter.com/chrisalbon/status/1295408107078615041)


## Installation

```bash
# python >=3.6.1 is required
pip install plumes
```

## Usage

### Getting Started And Creating Your Authentication Config

```bash
# create your config file
plumes init

# validate your config file
plumes check_config

# print your config file (watch out for sensitive tokens!)
plumes view_config
```

### Export Friends

[Extract friends](examples/SteveMartinToGo-friends.json) ordered in which they were added:

```bash
plumes friends <flags>

# e.g., get the friends of Steve Martin (see data in examples dir)
plumes friends SteveMartinToGo --limit 100
```

**Arguments**:

- `screen_name` _Optional[str], optional_ - Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
- `limit` _Optional[int], optional_ - Max number of users to fetch. Defaults to None.
- `output` _Optional[str], optional_ - Output path for JSON file. Defaults to None.

![Plumes friends gif](https://raw.githubusercontent.com/nnadeau/plumes/master/media/terminal-friends.gif)

### Export Followers

[Extract followers](examples/alyankovic-followers.json) ordered in which they were added:

```bash
plumes followers <flags>

# e.g., get the followers of Al Yankovic (see data in examples dir)
plumes followers alyankovic --limit 100
```

**Arguments**:

- `screen_name` _Optional[str], optional_ - Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
- `limit` _Optional[int], optional_ - Max number of users to fetch. Defaults to None.
- `output` _Optional[str], optional_ - Output path for JSON file. Defaults to None.

### Export Tweets

[Extract (and archive) tweets](examples/ConanOBrien-tweets.json) ordered in by most recent:

```bash
plumes tweets <flags>

# e.g., get the tweets of Conan O'Brien (see data in examples dir)
plumes tweets ConanOBrien --limit 100
```

**Arguments**:

- `screen_name` _Optional[str], optional_ - Target user's screen name (i.e., Twitter handle). If none is given, authenticated user is used. Defaults to None.
- `limit` _Optional[int], optional_ - Max number of users to fetch. Defaults to None.
- `output` _Optional[str], optional_ - Output path for JSON file. Defaults to None.

![Plumes tweet gif](https://raw.githubusercontent.com/nnadeau/plumes/master/media/terminal-tweets.gif)

### Audit Users

Audit and review users given criteria.
Use this to mass follow/unfollow many users.

```bash
plumes audit_users PATH <flags>

# e.g., follow 100 of Al Yankovic's followers
plumes followers alyankovic --limit 100
plumes audit_users alyankovic-followers.json --befriend

# e.g., prune (i.e., unfollow) current friends who have less than 100 followers AND haven't tweeted in the last 30 days
plumes friends --output "friends.json"
plumes audit_users "friends.json" --prune --min_followers 100 --days 30
```

**Arguments**:

- `path` _str_ - Path to JSON file of users (e.g., output of friends())
- `min_followers` _Optional[int], optional_ - Min number of followers. Defaults to None.
- `max_followers` _Optional[int], optional_ - Max number of followers. Defaults to None.
- `min_friends` _Optional[int], optional_ - Min number of friends. Defaults to None.
- `max_friends` _Optional[int], optional_ - Max number of friends. Defaults to None.
- `days` _Optional[int], optional_ - Days since last tweet. Defaults to None.
- `min_tweets` _Optional[int], optional_ - Min number of tweets. Defaults to None.
- `max_tweets` _Optional[int], optional_ - Max number of tweets. Defaults to None.
- `min_favourites` _Optional[int], optional_ - Min number of favourites. Defaults to None.
- `max_favourites` _Optional[int], optional_ - Max number of favourites. Defaults to None.
- `min_ratio` _Optional[float], optional_ - Min Twitter follower-friend (TFF) ratio. Defaults to None.
- `max_ratio` _Optional[float], optional_ - Max Twitter follower-friend (TFF) ratio. Defaults to None.
- `prune` _bool, optional_ - Unfollow identified users. Defaults to False.
- `befriend` _bool, optional_ - Follow identified users. Defaults to False.
- `bool_or` _bool, optional_ - Switch to boolean OR for conditions. Defaults to False.

### Prune Your Tweets

Audit and review tweets given criteria.
Use this to mass favourite or delete tweets.

```bash
plumes audit_tweets PATH <flags>

# e.g., delete your tweets that are older than 60 days AND that you didn't self-favourite
plumes tweets --output "tweets.json"
plumes audit_tweets "tweets.json" --prune --days 60 --self_favorited False

# e.g., export 100 of Conan O'Brien's tweets and favourite those that have a maximum of 10 likes and a minimum of 50 retweets
plumes tweets ConanOBrien --limit 100
plumes audit_tweets ConanOBrien-tweets.json --favorite --max_likes 10 --min_retweets 50
```

**Arguments**:

- `days` _Optional[int], optional_ - Days since tweeted. Defaults to None.
- `min_likes` _Optional[int], optional_ - Min number of favourites. Defaults to None.
- `max_likes` _Optional[int], optional_ - Max number of favourites. Defaults to None.
- `min_retweets` _Optional[int], optional_ - Min number of retweets. Defaults to None.
- `max_retweets` _Optional[int], optional_ - Max number of retweets. Defaults to None.
- `min_ratio` _Optional[float], optional_ - Min Twitter like-retweet ratio. Defaults to None.
- `max_ratio` _Optional[float], optional_ - Max Twitter like-retweet ratio. Defaults to None.
- `self_favorited` _Optional[bool], optional_ - Check if tweet is self-liked. Defaults to None.
- `prune` _bool, optional_ - Prune and destroy identified tweets. Defaults to False.
- `favorite` _bool, optional_ - Like identified tweets. Defaults to False.
- `bool_or` _bool, optional_ - Switch to boolean OR for conditions. Defaults to False.

## Advanced Usage and Chaining

Using the wonderful [`fx`](https://github.com/antonmedv/fx), we can filter and extract values from the JSON output of `plumes` to be reused and chained into other functions.

### Extracting Screen Names of Retweeted Statuses

```bash
fx tweets.json '.filter(x=>x.retweeted_status)' '.map(x=>x.retweeted_status.user.screen_name)'
```

- `fx tweets.json`: parse export of tweets
- `.filter(x=>x.retweeted_status)`: for each status (i.e., tweet), filter out non-retweeted statuses (`retweeted_status == null`)
- `.map(x=>x.retweeted_status.user.screen_name)`: for each status, extract `screen_name` of `user` in `retweeted_status`, creating a new array

### Batch Follow Users of Retweeted Statuses

```bash
for U in $(fx tweets.json '.filter(x=>x.retweeted_status)' '.map(x=>x.retweeted_status.user.screen_name)' '.join("\n")'); do plumes befriend_user $U; done
```

- `.join("\n")`: since `bash` likes line separators for for-loops, we join the array using a newline
- `for U in $(...); do ...; done`: for-loop that takes each user from the list provided
- `plumes befriend_user $U`: befriend the user stored in variable `$U`

## Setting Up Authentication

### Get Your Twitter API Tokens

- Navigate to the [Twitter Dev Portal](https://developer.twitter.com/en/apps)
- Click `Create an app`

  ![Twitter app link](https://raw.githubusercontent.com/nnadeau/plumes/master/media/2020-08-20-09-11-05.png)

- Fill out the forms
- Navigate to `Keys and tokens`

  ![Tokens link](https://raw.githubusercontent.com/nnadeau/plumes/master/media/2020-08-20-09-12-34.png)

- Copy the values for `API key`, `API secret key`, `Access token`, and `Access token secret`

  ![Keys and tokens](https://raw.githubusercontent.com/nnadeau/plumes/master/media/2020-08-20-09-13-24.png)

### Configuring `plumes`

The API tokens can either be set as environment variables (using the `PLUMES_` prefix; e.g., `export PLUMES_CONSUMER_KEY=xxxxx`) or configuration variables in `~/.plumes.toml`:

- CONSUMER_KEY = `<API key>`
- CONSUMER_SECRET = `<API secret key>`
- ACCESS_TOKEN = `<Access token>`
- ACCESS_TOKEN_SECRET = `<Access token secret>`

## Contributing

Please see [`CONTRIBUTING.md`](.github/CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) for how to contribute to the project

## Testing

- Please review the [`Makefile`](Makefile) for an overview of all available tests
- The most important tests and `make` commands are highlighted below:

```bash
# auto-format code
make format

# perform all static tests
make check
```

---

<div>Icons made by <a href="https://smashicons.com/" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
