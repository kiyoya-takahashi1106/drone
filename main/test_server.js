const express = require("express");
const { spawn } = require("child_process");
const wifi = require("node-wifi");
const cors = require("cors");
const app = express();
const PORT = 3001; // サーバーのポート番号

// CORSを有効にする
app.use(cors({
  origin: 'http://localhost:3000'
}));

// WiFiモジュールを初期化
wifi.init({
  iface: null // ネットワークインターフェース。nullに設定するとランダムなWiFiインターフェースが選ばれます。
});

// Telloネットワークに接続されているかを確認する関数
function checkTelloConnection() {
  return new Promise((resolve, reject) => {
    wifi.getCurrentConnections((error, currentConnections) => {
      if (error) {
        return reject(error);
      }
      console.log("現在の接続:", currentConnections); // デバッグ情報を追加
      const telloNetwork = currentConnections.find(connection =>
        (connection.mac && connection.mac.startsWith("TELLO-"))
      );
      if (telloNetwork) {
        console.log("Telloネットワークに接続されています:", telloNetwork.bssid || telloNetwork.mac);
      } else {
        console.log("Telloネットワークに接続されていません。");
      }
      resolve(!!telloNetwork);
    });
  });
}

// Telloネットワークに接続されている場合にtest.pyを実行するルート
app.get("/", async (req, res) => {
  try {
    const isConnectedToTello = await checkTelloConnection();
    if (isConnectedToTello) {
      const pyProg = spawn("python", ["test.py"]);

      pyProg.stdout.on("data", function (data) {
        res.write(data.toString());
      });

      pyProg.stderr.on("data", function (data) {
        res.write(data.toString());
      });

      pyProg.on("close", (code) => {
        res.end();
        console.log(`child process exited with code ${code}`);
      });
    } else {
      res.send("Not connected to Tello network.");
    }
  } catch (error) {
    res.status(500).send(error.toString());
  }
});

// サーバーを起動
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});