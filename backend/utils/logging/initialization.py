"""Logger initialization module.

This module sets up logging for the application, including log level,
format, and output file configuration. It uses environment variables
to determine the logging level.
"""

import json
import logging.config
import os


def setup_logging():
    """Set up logging configuration for the application.

    This function loads the logging configuration from a JSON file,
    adjusts the log level based on the environment, and applies the
    configuration to the logging system.
    """
    config_path = os.path.join(os.path.dirname(__file__), "logging_config.json")
    with open(config_path) as f:
        config = json.load(f)

    env = os.getenv("ENVIRONMENT", "Development")
    if env == "Production":
        config["root"]["level"] = "INFO"
    else:
        config["root"]["level"] = "DEBUG"

    logging.config.dictConfig(config)


setup_logging()
logger = logging.getLogger(__name__)
