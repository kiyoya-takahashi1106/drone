const http = require("http");
const PORT = 8080;
const { spawn } = require("child_process");

// Create a server object:
const server = http.createServer(function (req, res) {
  const urlParts = req.url.split("/");
  if (urlParts.length === 5) {
    const N = urlParts[1];
    const M = urlParts[2];
    const height = urlParts[3];
    const width = urlParts[4];

    // main.py を実行する
    const pyProg = spawn("python", ["main.py", N, M, height, width]);

    pyProg.stdout.on("data", function (data) {
      res.write(data.toString());
      res.end();
    });

    pyProg.stderr.on("data", function (data) {
      res.write(data.toString());
      res.end();
    });

    pyProg.on("close", (code) => {
      console.log(`child process exited with code ${code}`);
    });
  } else {
    res.end("Invalid endpoint");
  }
});

server.listen(PORT, (error) => {
  if (error) {
    console.log("Something went wrong", error);
  } else {
    console.log("Server is listening on port " + PORT);
  }
});