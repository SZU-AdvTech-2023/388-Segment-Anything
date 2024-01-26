var express = require("express");
const open = require("open");
var app = express();
const hostname = "localhost";
const port = 8080;
app.use(express.static("../dist/"));
app.listen(port, hostname, () => {
  console.log(`Server is running, ${hostname}:${port}`);
});

// 使用默认浏览器打开
open("http://localhost:8080/"); // 自动在默认浏览器打开
