import sys
from loguru import logger
from src.docmind.config.settings import settings


def setup_logger():
    logger.remove()

    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan> - <white>{message}</white>",
        colorize=True,
    )

    logger.add(
        "logs/docmind.log",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} - {message}",
        rotation="10 MB",
        retention="7 days",
    )

    return logger


logger = setup_logger()
