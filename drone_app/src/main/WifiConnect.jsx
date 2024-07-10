import React from 'react';
// import { useState } from 'react';
// import { Link } from 'react-router-dom';
// import Desk from '../Components/Desk';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function TelloSetting() {
    const handleButtonClick = async () => {
        try {
          const response = await fetch('http://localhost:3001/start-server');
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
                            <div style={{ fontSize: '59px' }}>Connct to Wifi</div>
                        </div>
                        <div style={{ fontSize: '30px' }}>
                            <div>➀このブラウザを手動で閉じてください</div>
                            <div>➁閉じた後TelloWifiと繋げてください</div>
                        </div>
                    </div>
                    <button onClick={handleButtonClick } style={{ height: '120px', width: '300px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '20px', border: 'none', cursor: 'pointer' }}>server start</button>
                </div>
            </div>
        </div>
    );
}

export default TelloSetting;
