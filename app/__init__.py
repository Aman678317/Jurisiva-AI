# Jurisiva AI Root App Package
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_current_dir)
_api_app_dir = os.path.join(_root_dir, "services", "api", "app")
_api_dir = os.path.join(_root_dir, "services", "api")

if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

if os.path.exists(_api_app_dir) and _api_app_dir not in __path__:
    __path__.append(_api_app_dir)
