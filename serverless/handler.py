import json
import time

# Cold start marker. This is True only for the first invocation after a new container starts.
cold_start = True

print("Lambda init: cold_start=True")


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
    global cold_start
    invocation_start = time.time()
    request_id = getattr(context, 'aws_request_id', 'unknown')
    arrival_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

    print(json.dumps({
        'type': 'invocation_start',
        'request_id': request_id,
        'cold_start': cold_start,
        'arrival_time': arrival_time,
        'event_keys': list(event.keys()) if isinstance(event, dict) else None
    }))

    try:
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        limit = int(body.get('limit', 1000))
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({
            'type': 'invocation_error',
            'request_id': request_id,
            'error': str(exc)
        }))
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid input: limit must be an integer'})
        }

    compute_start = time.time()
    result = heavy_compute(limit)
    compute_end = time.time()

    invocation_end = time.time()
    print(json.dumps({
        'type': 'invocation_end',
        'request_id': request_id,
        'cold_start': cold_start,
        'limit': limit,
        'compute_time': compute_end - compute_start,
        'total_time': invocation_end - invocation_start
    }))

    cold_start = False

    return {
        'statusCode': 200,
        'body': json.dumps({
            'prime_count': result,
            'compute_time': compute_end - compute_start,
            'total_time': invocation_end - invocation_start,
            'cold_start': False
        })
    }
