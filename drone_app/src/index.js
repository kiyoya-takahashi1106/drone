import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import Rooter from './routes/index'; // ここで Rooter をインポート

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Rooter />
  </React.StrictMode>
);

// サービスワーカーの関連コードを削除
reportWebVitals();
