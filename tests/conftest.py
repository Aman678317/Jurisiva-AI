import sys
import os

# Add services/api to sys.path so 'app' module can be imported cleanly in tests
api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services", "api"))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)
