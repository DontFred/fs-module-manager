"""Main module for the backend service.

This module initializes the backend service, loads environment variables,
and starts the Uvicorn server with the specified configuration.
"""

import os

import uvicorn
from dotenv import load_dotenv

from utils.logging.logger import logging


def main():
    """Main function to start the backend service."""
    logging.debug("Loading environment variables...")
    load_dotenv()
    port = int(os.getenv("BACKEND_PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    reload = True if environment == "development" else False
    logging.info(
        f"Starting backend service on port {port} in {environment} mode..."
    )
    config_path = os.path.join(
        os.path.dirname(__file__), "utils", "logging", "logging_config.json"
    )
    uvicorn.run(
        "api.initialization:app",
        host="127.0.0.1",
        port=port,
        reload=reload,
        log_config=config_path,
        reload_dirs=["api", "utils", "db", "v0"],
    )


if __name__ == "__main__":
    main()
