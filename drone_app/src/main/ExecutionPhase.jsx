import React from 'react';
import { useParams } from 'react-router-dom';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function ExecutionPhase() {
  const { N, M, height, width } = useParams();
  console.log({ N, M, height, width });

  // ボタンを押すとサーバーを起動する
  const handleButtonClick = async () => {
    try {
      // const response = await fetch(`http://localhost:3001/${N}/${M}/${height}/${width}`);
      const response = await fetch(`http://localhost:3001`);   // test用
      const data = await response.text();
      console.log(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Home"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
          <div style={{ fontFamily: '"Abel", sans-serif' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
              <div style={{ fontSize: '59px' }}>Execution Phase</div>
            </div>
            <div style={{ fontSize: '30px' }}>
              <div>➀server.jsのフォルダに移動してください</div>
              <div>➁node server.jsする</div>
              <div>➂TelloWifiと繋げてください</div>
            </div>
          </div>
          <button onClick={handleButtonClick} style={{ height: '120px', width: '300px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '20px', border: 'none', cursor: 'pointer' }}>server start</button>
        </div>
      </div>
    </div>
  );
}

export default ExecutionPhase;