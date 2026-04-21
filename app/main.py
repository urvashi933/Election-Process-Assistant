from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

# 1. Mount your static files (CSS/JS)
# Make sure your style.css and script.js are in a folder called 'static'
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # This reads your index.html and sends it to the browser
    with open(os.path.join("static", "index.html"), "r") as f:
        return f.read()
