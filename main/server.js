const express = require("express");
const http = require("http");
const { spawn } = require("child_process");
const app = express();
const PORT = 3002;   // Expressサーバーのポート番号

// サーバーを起動するエンドポイント
app.get("/:N/:M/:height/:width", (req, res) => {
  const { N, M, height, width } = req.params;
  console.log(`Received request with parameters: N=${N}, M=${M}, height=${height}, width=${width}`);

  // サーバーのインスタンスを作成
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

  // 動的に空いているポートを見つけてサーバーをリッスンする
  server.listen(0, () => {
    const address = server.address();
    console.log(`Server is listening on port ${address.port}`);
    res.send(`Server started on port ${address.port}`);
  });

  // エラーハンドリング
  server.on("error", (err) => {
    console.error("Server error:", err);
    res.status(500).send("Server error");
  });
});

app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
