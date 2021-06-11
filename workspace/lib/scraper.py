import backtrader as bt
import ccxt
import datetime


def __noop(*args):
    pass


def get_exchange(exchange_id, options=None):
    # Get list of exchanges with ccxt.exchanges, call this function to get an exchange
    default_options = {
        'enableRateLimit': True,
        'options': {
            'adjustForTimeDifference': True
        }
    }
    if options is not None:
        default_options.update(options)

    return getattr(ccxt, exchange_id)(default_options)


def __retry_fetch_OHLCV(exchange, pair, timeframe, since, max_retries=3):
    num_retries = 0
    OHLCV = None
    while OHLCV is None:
        try:
            num_retries += 1
            OHLCV = exchange.fetchOHLCV(pair, timeframe, since, 700)
            return OHLCV
        except Exception as e:
            if num_retries > max_retries:
                raise e


def get_candles(exchange, pair, timeframe, from_datetime, to_datetime, max_retries=3, logger=__noop
                ):
    logger('Fetching %s candles from %s for %s' % (timeframe, exchange, pair))
    since = from_datetime.timestamp() * 1000
    to = to_datetime.timestamp() * 1000
    candles = []

    milliseconds = {key: int(value) * 1000 for key,
                    value in exchange.timeframes.items()}
    last = milliseconds[timeframe]

    while since < to:
        OHLCV = __retry_fetch_OHLCV(exchange, pair, timeframe, since, max_retries)
        logger('%s candles obtained' % (len(OHLCV)))
        if not len(OHLCV):
            break
        candles += OHLCV
        since = candles[-1][0]
        if since >= (to - last):
            break

    return candles
