"""This module initializes the FastAPI application and registers the api."""

from fastapi import FastAPI

from api.service import register_api

app = FastAPI(
    docs_url="/v0/docs",
    redoc_url=None,
    openapi_url="/v0/openapi.json",
    title="Module Manager API",
)

register_api(app)
