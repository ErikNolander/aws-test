exports.handler = async (event) => {
    const start = Date.now();

    let result = 0;
    for (let i = 1; i <= 100000; i++)
    {
        result += 1000 / i;
    }

    const end = Date.now();

    return {
        statusCode: 200,
        body: JSON.stringify({
            result: result,
            executionTimeMs: end - start
        })
    };
};
