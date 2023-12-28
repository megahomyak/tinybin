from typing import Annotated
import secrets
from fastapi import FastAPI, Form, status
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from argparse import ArgumentParser
from pathlib import Path

parser = ArgumentParser()
parser.add_argument("--host", required=True)
parser.add_argument("--port", type=int, required=True)
args = parser.parse_args()

TEXTS_DIR = Path("texts").resolve()

api = FastAPI()

def new_name():
    return secrets.token_urlsafe(nbytes=16)

@api.get("/")
def send_root():
    return HTMLResponse("index.html")

@api.post("/texts/")
def share(text: Annotated[str, Form()]):
    name = new_name()
    with open(TEXTS_DIR/name, "w", encoding="utf-8") as f:
        f.write(text)
    return RedirectResponse(
        url=f"/texts/{name}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )

@api.get("/texts/{name}")
def get_text(name: str):
    file_path = (TEXTS_DIR/name).resolve()
    if file_path.parent != TEXTS_DIR:
        return PlainTextResponse(
            "403 Forbidden",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    try:
        with open(file_path, encoding="utf-8") as f:
            return PlainTextResponse(f.read())
    except FileNotFoundError:
        return PlainTextResponse(
            "404 Not Found",
            status_code=status.HTTP_404_NOT_FOUND,
        )