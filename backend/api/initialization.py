"""This module initializes the FastAPI application and registers the api."""

from fastapi import FastAPI

from api.service import register_api

app = FastAPI(docs_url="/v0/docs", redoc_url=None)

register_api(app)
