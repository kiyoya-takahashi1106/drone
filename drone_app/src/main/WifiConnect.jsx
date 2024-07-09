import React from 'react';
// import { useState } from 'react';
// import { Link } from 'react-router-dom';
// import Desk from '../Components/Desk';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';
import droneImg from '../img/drone.jpg';

function WifiConnect() {
  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Wifi Connect"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
            <div style={{ fontFamily: '"Abel", sans-serif' }}>
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
                    <div style={{ fontSize: '49px' }}>Connect to Tello</div>
                    <img src={droneImg} style={{ height: '300px', width: '400px' }} alt="droneImage" />
                </div>
                <div style={{ fontSize: '30px' }}>
                    <div>➀Telloにバッテリーを入れ, 電源を付ける.</div>
                    <div>➁PCのWifiをtelloと繋げる.</div>
                    <div>➂(0,0)と(1,0)の席の間にセットしてください.</div>
                </div>
            </div>
            <button style={{ height: '70px', width: '180px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '0px', border: 'none', cursor: 'pointer' }}>Next</button>
        </div>
      </div>
    </div>
  );
}

export default WifiConnect;
