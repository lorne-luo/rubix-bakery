import logging
import os
from decimal import Decimal


# env vars are always str, need convert to bool

def env_bool(env_key, default=None):
    """
    get bool from env vars
    """
    bool_str = os.getenv(env_key, default)
    if bool_str is None:
        raise Exception(f'Env var {env_key} is not configured properly.')

    if isinstance(bool_str, str) and bool_str.lower() in ['false', '0', 'no', 'not']:
        return False

    return bool(bool_str)


def env_int(env_key, default=None):
    """
    get int from env vars
    """
    int_str = os.getenv(env_key, default)
    try:
        return int(int_str)
    except:
        raise Exception(f'Env var {env_key} is not configured properly.')


# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env_bool('DEBUG', default=False)

# LOG LEVEL SETTINGS
# ------------------------------------------------------------------------------
# according to DEBUG
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

logging.basicConfig(level=LOG_LEVEL)

# PRICE DECIMAL PLACES
# ------------------------------------------------------------------------------
# decimal is better type than float for currency due to fixed point
PRICE_DECIMAL_PLACES = env_int('PRICE_DECIMAL_PLACES', 2)  # 10 ** -2 = 0.01

PRICE_DECIMAL_UNIT = Decimal(str(10 ** (-1 * PRICE_DECIMAL_PLACES)))
