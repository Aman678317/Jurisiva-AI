# Jurisiva AI Root Level Main Entrypoint
import os
import sys

_current_dir = os.path.dirname(os.path.abspath(__file__))
_api_dir = os.path.join(_current_dir, "services", "api")

if _api_dir not in sys.path:
    sys.path.insert(0, _api_dir)

from services.api.app.main import app
from fastapi.responses import HTMLResponse, FileResponse

@app.get("/", response_class=HTMLResponse)
@app.get("/app", response_class=HTMLResponse)
@app.get("/trust", response_class=HTMLResponse)
@app.get("/workspace", response_class=HTMLResponse)
def root_index_page():
    candidates = [
        os.path.join(_current_dir, "apps", "web", "index.html"),
        os.path.join(_current_dir, "index.html"),
        os.path.join(os.getcwd(), "apps", "web", "index.html"),
        os.path.join(os.getcwd(), "index.html"),
        "apps/web/index.html",
        "index.html",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    return HTMLResponse(content=f.read(), status_code=200)
            except Exception:
                return FileResponse(c, media_type="text/html")
    return HTMLResponse("<h1>Jurisiva AI</h1><p>Application loading...</p>", status_code=200)

__all__ = ["app"]
