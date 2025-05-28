from prometheus_client import Counter, Histogram
from fastapi import Request

REQUESTS = Counter(
    'api_requests_total',
    'Total API Requests',
    ['method', 'endpoint']
)

LATENCY = Histogram(
    'api_request_latency_seconds',
    'API Request Latency',
    ['endpoint']
)


async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    latency = time.time() - start_time

    REQUESTS.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()

    LATENCY.labels(
        endpoint=request.url.path
    ).observe(latency)

    return response