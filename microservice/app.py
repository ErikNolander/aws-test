import json
import logging
import time
import uuid

from flask import Flask, request, jsonify

app = Flask(__name__)

logger = logging.getLogger("division-service")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)
logger.propagate = False

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)
werkzeug_logger.handlers = [handler]
werkzeug_logger.propagate = False

app.logger.handlers = [handler]
app.logger.propagate = False


def log_json(event_type, **kwargs):
    payload = {
        "service": "division-service",
        "event_type": event_type,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **kwargs,
    }
    logger.info(json.dumps(payload, separators=(",", ":"), sort_keys=True))


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def heavy_compute(limit):
    count = 0
    for num in range(2, limit):
        if is_prime(num):
            count += 1
    return count


@app.route("/process", methods=["POST"])
def process():
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    invocation_start = time.time()
    remote_addr = request.remote_addr
    user_agent = request.headers.get("User-Agent", "")

    log_json(
        "request_start",
        request_id=request_id,
        path=request.path,
        method=request.method,
        remote_addr=remote_addr,
        user_agent=user_agent,
    )

    try:
        data = request.get_json(force=True)
        limit = int(data.get("limit", 100))
    except Exception as exc:
        log_json(
            "request_error",
            request_id=request_id,
            path=request.path,
            method=request.method,
            error=str(exc),
            status=400,
        )
        return jsonify({"message": "Invalid input: limit must be an integer"}), 400

    compute_start = time.time()
    result = heavy_compute(limit)
    compute_end = time.time()

    invocation_end = time.time()
    total_time = invocation_end - invocation_start
    compute_time = compute_end - compute_start

    log_json(
        "request_end",
        request_id=request_id,
        path=request.path,
        method=request.method,
        limit=limit,
        status=200,
        compute_time=round(compute_time, 6),
        total_time=round(total_time, 6),
    )

    return jsonify({
        "prime_count": result,
        "compute_time": compute_time,
        "total_time": total_time,
        "request_id": request_id,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)

