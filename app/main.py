# Jurisiva AI Main Application Gateway
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_current_dir)
_api_dir = os.path.join(_root_dir, "services", "api")

if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

from services.api.app.main import (
    app,
    FastAPIBackendServer,
    backend_server,
    HAS_FASTAPI
)

__all__ = ["app", "FastAPIBackendServer", "backend_server", "HAS_FASTAPI"]
