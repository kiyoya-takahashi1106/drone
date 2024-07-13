import React from 'react';
import { useParams, Link } from 'react-router-dom';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';
import droneImg from '../img/drone.jpg';

function TelloSetting() {
  const params = useParams();
  console.log(params);

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Home"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
            <div style={{ fontFamily: '"Abel", sans-serif' }}>
                <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column'}}>
                    <div style={{ fontSize: '59px' }}>Tello Setting</div>
                    <img src={droneImg} style={{ height: '300px', width: '460px' }} alt="droneImage" />
                </div>
                <div style={{ fontSize: '35px' }}>
                    <div>➀Telloにバッテリーを入れ, 電源を付ける.</div>
                    <div>➁(0,0)と(1,0)の席の間にセットしてください.</div>
                </div>
            </div>
            <Link to={`/home/setting/executionphase/${params.N}/${params.M}/${params.height}/${params.width}`}>
              <button style={{ height: '70px', width: '180px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '20px', border: 'none', cursor: 'pointer' }}>Next</button>
            </Link>
        </div>
      </div>
    </div>
  );
}

export default TelloSetting;
