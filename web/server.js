const express = require("express");
const args = process.argv.slice(2);

if (!args[0]) {
    console.log("Usage: node server.js <directory> [port=80]");
    process.exit(1);
}

const app = express();
const port = args[1] ? parseInt(args[1], 10) : 80;
app.get('/collector', (req, res) => {
    console.log(`Collected: ${decodeURIComponent(req.originalUrl)}`);
    res.send("");
});

app.use(express.static(args[0]));
app.listen(port, () => {
    console.log(`Node static webserver hosting ${args[0]} at localhost:${port}`);
    console.log(`Collecting GET requests at localhost:${port}/collector`);
});
