# 1. Standard library
import sys
import uuid
from pathlib import Path
from contextvars import ContextVar

# 2. Third-party
from loguru import logger

# 3. Local imports
from .configuration import paths

request_id_var = ContextVar("request_id", default="-")


def set_request_id():
    rid = str(uuid.uuid4())
    request_id_var.set(rid)
    return rid


logger = logger.patch(
    lambda record: (
        record["extra"].setdefault("request_id", request_id_var.get()),
        record["extra"].setdefault("service", "-"),
    )
)


def get_logger(service: str = "bg"):
    if not service or service == "":
        service = "bg"

    return logger.bind(service=service)


def setup_logger(log_file_name: str = "app.log", level: str = "INFO"):
    logger.remove()

    log_dir = Path(paths.logs)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / log_file_name

    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{extra[request_id]}</cyan> | "
            "<magenta>{extra[service]}</magenta> | "
            "<white>{message}</white>"
        ),
    )

    logger.add(
        log_file,
        level=level,
        rotation="5 MB",
        retention="7 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    return logger
