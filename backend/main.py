# Copyright (c) 2025 Frederik Grimm & Morgan Fritzsche
# This source code is licensed under the CC BY-NC-SA 4.0 license found in the
# LICENSE file in the root directory of this source tree.
# NOT ALLOWED FOR COMMERCIAL USE.

"""Main module for the backend service.

This module initializes the backend service, loads environment variables,
and starts the Uvicorn server with the specified configuration.
"""

import os

import uvicorn
from dotenv import load_dotenv

from db.initialization import setup_database
from utils.logging.initialization import logger


def main():
    """Main function to start the backend service."""
    logger.debug("Loading environment variables...")
    load_dotenv()
    port = int(os.getenv("BACKEND_PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    reload = True if environment == "development" else False
    logger.debug("Setting up the database...")
    setup_database()
    logger.info(
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
        reload_dirs=["api", "utils", "db"],
    )


if __name__ == "__main__":
    main()
