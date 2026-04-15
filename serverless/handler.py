import json
import time

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

def handler(event, context):
    start = time.time()

    if "body" in event:
        body = json.loads(event["body"])
    else:
        body = event
    limit = body["limit"]

    result = heavy_compute(limit)

    end = time.time()

    print("execution_time:", end - start)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "prime_count": result,
            "execution_time": end - start
        })
    }
