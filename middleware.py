from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import os

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")



limiter = Limiter(get_remote_address, default_limits=["50 per hour"], storage_uri=redis_url)
csrf = CSRFProtect()
