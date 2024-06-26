from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root(name: str):
    return f"<h1>Hello <span>{name}</span></h1>"
