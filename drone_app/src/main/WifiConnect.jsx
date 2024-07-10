import React from 'react';
// import { useState } from 'react';
// import { Link } from 'react-router-dom';
// import Desk from '../Components/Desk';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function TelloSetting() {
    const handleClose = () => {
        window.close();
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
                            <div>➀</div>
                            <div>➁このブラウザを手動で閉じてください</div>
                            <div>➂閉じた後TelloWifiと繋げてください</div>
                        </div>
                    </div>
                    <button onClick={handleClose} style={{ height: '70px', width: '300px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '20px', border: 'none', cursor: 'pointer' }}>close site</button>
                </div>
            </div>
        </div>
    );
}

export default TelloSetting;
