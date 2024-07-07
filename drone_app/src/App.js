import React from 'react';

function App() {
  return (
    <div style={{
      height: '840px',
      width: '390px',
      display: 'flex',
      justifyContent: 'center', // 横方向の中央に配置
      alignItems: 'center', // 縦方向の中央に配置
      background: 'white'
    }}>
      <div style={{
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column', // 子要素を縦並びに
        justifyContent: 'center',
        alignItems: 'center'
      }}>
        <div style={{ fontSize: '20px' }}>auto</div>
        <div style={{ fontSize: '30px' }}>Tello</div>
      </div>
    </div>
  );
}

export default App;
