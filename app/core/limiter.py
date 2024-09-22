from slowapi import Limiter
from slowapi.util import get_remote_address

# Define the limiter with default rate limits
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])