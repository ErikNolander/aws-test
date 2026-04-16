from flask import Flask, request, jsonify
import time

app = Flask(__name__)

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

@app.post("/prime-count")
def prime_count():
    start = time.time()

    body = request.get_json(silent=True) or {}
    limit = int(body.get("limit", 7920))

    result = heavy_compute(limit)

    end = time.time()
    execution_time = end - start

    print("execution_time:", execution_time)

    return jsonify({
        "prime_count": result,
        "execution_time": execution_time
    }), 200

@app.get("/health")
def health():
    return jsonify({"ok": True}), 200