import time
from fastapi import Request
from . import get_logger, set_request_id, request_id_var


async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()

    request_id = set_request_id()
    log = get_logger("api")

    status_code = 500
    response = None

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    except Exception:
        log.bind(
            event="request_exception",
            method=request.method,
            path=request.url.path,
        ).exception("Unhandled exception")
        raise

    finally:
        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        log.bind(
            event="http_request",
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=duration_ms,
            client=request.client.host if request.client else None,
        ).info("Request completed")

        if response:
            response.headers["X-Request-ID"] = request_id

        # cleanup context
        request_id_var.set("-")
