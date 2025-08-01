# api/index.py
from app import create_app
from flask import Request

app = create_app()

def handler(request: Request, *args, **kwargs):
    return app(request.environ, start_response=lambda status, headers: None)
