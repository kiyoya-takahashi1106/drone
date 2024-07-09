import React from 'react';

const TopHeader = () => {
  return (
    <div style={{ height: '149px', width: '1280px', fontFamily: '"Zen Dots", sans-serif', borderBottom: '2px solid black', display: 'flex' }}>
      <div style={{ height: '149px', width: '336px', color: 'white', textShadow: '3px 3px 0 black, -3px -3px 0 black, -3px 3px 0 black, 3px -3px 0 black, 2px 2px 0 black, -2px -2px 0 black, -2px 2px 0 black, 2px -2px 0 black, 1px 1px 0 black, -1px -1px 0 black, -1px 1px 0 black, 1px -1px 0 black' , backgroundColor: 'rgba(208, 242, 199, 0.65)', borderRight: '2px solid black', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ fontSize: '40px', margin: '0px 100px 0px 0px' }}>auto</div>
        <div style={{ fontSize: '70px', margin: '-24px 0 0 0' }}>Tello</div>
      </div>
      <div style={{ height: '149px', width: '944px', fontSize: '70px', backgroundColor: 'rgba(231, 226, 119, 0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        Home
      </div>
    </div>
  );
};

export default TopHeader;
