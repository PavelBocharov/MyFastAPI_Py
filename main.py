from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/") # декоратор
def read_root():
    html_content = "<h2>Hello, Marolok!</h2>"
    return HTMLResponse(content=html_content)