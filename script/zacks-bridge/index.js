"use strict";

const api = require("zacks-api");

async function main() {
    try {
        const tickers = JSON.parse(process.argv[2]);

        if (!tickers || !Array.isArray(tickers)) {
            console.error("Expected JSON array of tickers but didn't get one");
            process.exit(1);
        }


        // Use Promise.all to fetch data for all tickers concurrently
        // inner try catch enables individual error handling
        const results = await Promise.all(tickers.map(async (ticker) =>{
            try {
                const data = await api.getData(ticker);
                return {ticker, data, success: true};
            } catch (error) {
                return {ticker, error: error.message, success: false};
            }
        }));

        console.log(JSON.stringify(results));

        process.exit(0);


    } catch (error) {
        console.error("Error fetching data:", error);
        process.exit(1);
    }
}

main();