"use strict";

const api = require("zacks-api");

async function main() {
    const ticker = process.argv[2];

    if (!ticker) {
        console.error("Usage: node index.js <ticker>");
        process.exit(1);
    }

    try {
        const result = await api.getData(ticker);

        console.log(JSON.stringify(result));

        process.exit(0);
    } catch (error) {
        console.error("Error fetching data:", error);
        
        process.exit(1);
    };
}

main();