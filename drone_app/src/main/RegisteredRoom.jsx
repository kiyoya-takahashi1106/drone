import React from 'react';
// import { useState } from 'react';
// import { Link } from 'react-router-dom';
// import Desk from '../Components/Desk';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function RegisteredRoom() {
  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Registered Room"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px' }}>
          <div style={{ height: '471px', width: '944px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisteredRoom;
