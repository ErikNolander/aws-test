const express = require('express');
const app = express();

app.get('/', (req, res) => {
    const start = Date.now();

    let result = 0;
    for (let i = 1; i <= 100000; i++) {
        result += 1000 / i;
    }

    const end = Date.now();

    res.json({
        result: result,
        executionTimeMs: end - start
    });
});

app.listen(3000, () => {
    console.log("Service running on port 3000");
});