const express = require("express");
const args = process.argv.slice(2);

if (!args[0]) {
    console.log("Usage: node server.js <directory>");
    process.exit(1);
}

const app = express();
app.get('/collector', (req, res) => {
    console.log(`Request received: ${decodeURIComponent(req.originalUrl)}`);
    res.send("");
});

app.use(express.static(args[0]));
app.listen(80, () => console.log("Collector listening on port 80!"));

