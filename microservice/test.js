import http from 'k6/http';
import { check } from 'k6';

export const options = {
  scenarios: {
    low_load: {
      executor: 'constant-arrival-rate',
      rate: 100,          // 100 requests
      timeUnit: '1m',     // per minut
      duration: '1m',
      preAllocatedVUs: 10,
      maxVUs: 50,
    },
  },
};

export default function () {
  const url = 'http://13.61.184.112:8080/prime-count';

  const payload = JSON.stringify({
    limit: 7920,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const res = http.post(url, payload, params);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

// kolla min ip:    (Invoke-RestMethod -Uri "https://checkip.amazonaws.com").Trim()