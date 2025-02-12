from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

limiter = Limiter(get_remote_address, default_limits=["50 per hour"])
csrf = CSRFProtect()
