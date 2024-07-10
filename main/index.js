//index.js

const http = require("http");
const port = 8080;

// Create a server object:
const server = http.createServer(function (req, res) {
  // /endo の時endo返す
  if (req.url === "/endo") {
    // main.py を実行する
    const { spawn } = require("child_process");
    const pyProg = spawn("python", ["main.py"]);

    pyProg.stdout.on("data", function (data) {
      console.log(data.toString());
    });
    res.end("Python script executed");
  } else {
    res.end("Invalid endpoint");
  }
});


server.listen(port, (error) => {
  if (error) {
    console.log("Something went wrong", error);
  } else {
    console.log("Server is listening on port " + port);
  }
});
