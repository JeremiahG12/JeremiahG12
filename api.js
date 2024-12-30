// Ensure you're using ES module syntax
import fetch from 'node-fetch';
import { decompress } from 'compress-json';
import fs from 'fs';
import { parse } from 'json2csv';
import path from 'path';
import * as devalue from 'devalue'; // Correct import for devalue

(async () => {
  try {
    const backupFolder = 'D:/AHDATA'; // Specify backup folder

    // Ensure backup folder exists
    if (!fs.existsSync(backupFolder)) {
      fs.mkdirSync(backupFolder, { recursive: true });
    }

    // First API call to get the auction house data
    const response1 = await fetch('https://tldb.info/auction-house/__data.json', {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Node.js Fetch)' }
    });

    if (!response1.ok) {
      throw new Error(`Failed to fetch auction house data: ${response1.statusText}`);
    }

    const auctionDataJson = await response1.json();

    // Decompress and unflatten auction data
    const auctionData = devalue.unflatten(auctionDataJson.nodes.find((e) => e?.type === 'data').data);
    const auctionDataItems = decompress(auctionData['items']); // Array of auction items

    // Second API call to get the prices data
    const response2 = await fetch('https://tldb.info/api/ah/prices', {
      headers: { 'User-Agent': 'Mozilla/5.0 (compatible; Node.js Fetch)' }
    });

    if (!response2.ok) {
      throw new Error(`Failed to fetch prices: ${response2.statusText}`);
    }

    const apiData2 = await response2.json();
    let { list, regions } = apiData2;

    // Decompress and parse the list data
    Object.keys(list).forEach((server) => {
      list[server] = decompress(JSON.parse(list[server]));
    });

    // Prepare dataset for CSV (from the 'list' API data)
    const listArray = Object.entries(list).flatMap(([server, details]) =>
      Object.entries(details).map(([id, itemDetails]) => {
        // Find matching item in auction data using the 'num' property
        const auctionItem = auctionDataItems.find(item => item.num === parseInt(id));

        return {
          server,
          id,
          quantity: itemDetails.quantity,
          price: itemDetails.price,
          sales: JSON.stringify(itemDetails.sales),
          // Add the mapped name from auctionData if available
          auctionData: auctionItem ? auctionItem.name : 'No match'
        };
      })
    );

    // Convert JSON to CSV
    const listCsv = parse(listArray, { fields: ['server', 'id', 'quantity', 'price', 'sales', 'auctionData'] });

    // Define the file path for the output
    const fileName = 'sales_data.csv';

    // Write to main file
    fs.writeFileSync(fileName, listCsv);

    // Write to backup folder with the same file name
    fs.writeFileSync(path.join(backupFolder, fileName), listCsv);

    console.log('CSV file has been written successfully.');

    // If you want to log or save the auction house data as well, you can do so like this:
    const auctionHouseFileName = 'auction_house_data.json';
    fs.writeFileSync(auctionHouseFileName, JSON.stringify(auctionDataItems, null, 2));
    console.log('Auction house data has been saved successfully.');

  } catch (error) {
    console.error('Error:', error.message);
  }
})();
