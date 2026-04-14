import http from 'k6/http';

export let options = {
  scenarios: {
    constant_rate: {
      executor: 'constant-arrival-rate',
      rate: 100,        // 100 requests
      timeUnit: '1m',   // per minute
      duration: '1m',
      preAllocatedVUs: 10,
      maxVUs: 50,
    },
  },
};

export default function () {
  http.post("https://e57vw5uw6iff57qq5emhykchwe0nawgh.lambda-url.eu-north-1.on.aws/", JSON.stringify({
    limit: 10
  }), {
    headers: { "Content-Type": "application/json" },
  });
}