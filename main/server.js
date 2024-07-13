const express = require("express");
const http = require("http");
const { spawn } = require("child_process");
const app = express();
const PORT = 3001;   // Expressサーバーのポート番号
const SERVER_PORT = 8081;   // 起動するサーバーのポート番号（例: 8081に変更）

// サーバーを起動するエンドポイント
app.get("/:N/:M/:height/:width", (req, res) => {
  const { N, M, height, width } = req.params;

  const server = http.createServer(function (req, res) {
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
  });

  server.listen(SERVER_PORT, (error) => {
    if (error) {
      console.log("Something went wrong", error);
      res.send("Error starting the server");
    } else {
      console.log(`Server is listening on port ${SERVER_PORT}`);
      res.send(`Server started on port ${SERVER_PORT}`);
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});