import time

from fastapi import Request
from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware


REQUEST_COUNT = Counter(
    "cloudtask_http_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status_code"],
)


REQUEST_LATENCY = Histogram(
    "cloudtask_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


class PrometheusMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start_time = time.perf_counter()

        response = await call_next(request)

        duration = time.perf_counter() - start_time

        REQUEST_COUNT.labels(
            method=request.method,
            path=request.url.path,
            status_code=str(response.status_code),
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            path=request.url.path,
        ).observe(duration)

        return response
