# Jurisiva AI Root Level Main Entrypoint
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_api_dir = os.path.join(_current_dir, "services", "api")

if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

from services.api.app.main import app

__all__ = ["app"]
