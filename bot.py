import datetime
import json

import pytz
from forecastiopy import ForecastIO
from mastodon import Mastodon


def get_toronto_weather(config):
    return ForecastIO.ForecastIO(config['dark_sky_key'],
                                 latitude=config['location']['latitude'],
                                 longitude=config['location']['longitude'],
                                 units='ca')


def post_toot(config, text):
    mastodon = Mastodon(**config['mastodon'])
    return mastodon.toot(text)


def main():
    with open('config.json') as fobj:
        config = json.loads(fobj.read())

    tz = pytz.timezone('America/Toronto')
    now_utc = datetime.datetime.now()
    now = tz.localize(now_utc)

    forecast = get_toronto_weather(config)

    if now.hour == 7:
        post_toot(config, forecast.daily['summary'])
    else:
        post_toot(config, forecast.hourly['summary'])


if __name__ == '__main__':
    main()
