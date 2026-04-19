import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 1,
  iterations: 1,
};

export default function () {
  const res = http.get('http://13.61.184.112:8080/health');

  console.log(`status=${res.status}`);
  console.log(`body=${res.body}`);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

// kolla min ip:    (Invoke-RestMethod -Uri "https://checkip.amazonaws.com").Trim()