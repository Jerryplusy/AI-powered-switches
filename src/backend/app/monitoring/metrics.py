from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
    Summary
)

# API Metrics
API_REQUESTS = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

API_LATENCY = Histogram(
    'api_request_latency_seconds',
    'API request latency',
    ['endpoint']
)

# Device Metrics
DEVICE_CONNECTIONS = Gauge(
    'network_device_connections',
    'Active device connections',
    ['vendor']
)

CONFIG_APPLY_TIME = Summary(
    'config_apply_seconds',
    'Time spent applying configurations'
)

# Error Metrics
CONFIG_ERRORS = Counter(
    'config_errors_total',
    'Configuration errors',
    ['error_type']
)

def observe_api_request(method: str, endpoint: str, status: int, duration: float):
    API_REQUESTS.labels(method, endpoint, status).inc()
    API_LATENCY.labels(endpoint).observe(duration)