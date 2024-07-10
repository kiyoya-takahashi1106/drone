import React from 'react';
import { useLocation } from 'react-router-dom';
// import { useState } from 'react';
// import { Link } from 'react-router-dom';
// import Desk from '../Components/Desk';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function RegisteredRoom() {
  const location = useLocation();
  const { M, N, height, width } = location.state || {};

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Registered Room"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', justifyContent: 'center' }}>
          <div style={{ height: '300px', width: '800px', margin: '39px 0px 0px 0px', border: '2px solid black' }}>
            <div style={{ height: '240px', width: '700px', display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center', fontSize: '36px', marginLeft: '30px', fontFamily: '"Abel", sans-serif' }}>
              <div style={{display: "flex" }}>
                <div style={{ margin: '10px 30px 0px -68px' }}>部屋名:</div>
                <input type="number" value={N} style={{ height: '60px', width: '400px', fontSize: '40px', margin: '5px 0px 0px 0px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
              <div style={{display: "flex", marginTop: '20px' }}>
                <div style={{ marginRight: '50px' }}>個数:</div>
                <div>N(縦) =</div>
                <input type="number" value={N} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '40px' }}>,</div>
                <div>M(横) =</div>
                <input type="number" value={M} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
              <div style={{ display: "flex", marginTop: '10px' }}>
                <div style={{ marginRight: '46px' }}>長さ:</div>
                <div>height =</div>
                <input type="number" value={height} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '45px' }}>,</div>
                <div>width =</div>
                <input type="number" value={width} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
            </div>

            <button style={{ height: '50px', fontSize: '30px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', margin: '0px 0px 0px 350px', border: 'none', cursor: 'pointer' }}>Save with this content</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisteredRoom;
