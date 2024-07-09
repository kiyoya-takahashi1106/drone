import React from 'react'

const Loading = () => {
  return (
    <div style={{ height: '832px', width: '1280px', backgroundColor: '#9A9A9A', position: 'relative', border: 'none', display: 'flex' }}>
        <div style={{ width: '100%', height: '100%', backgroundColor: '#D45454', clipPath: 'polygon(3% 0%, 58.5% 0%, 38.5% 100%, 3% 100%)', position: 'absolute' }}></div>
        <div style={{ width: '100%', height: '100%', backgroundColor: '#4DB5E1', clipPath: 'polygon(61.5% 0%, 97% 0%, 97% 100%, 41.5% 100%)', position: 'absolute' }}></div>
        <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', fontFamily: '"Zen Dots", sans-serif', color: 'white', textShadow: '3px 3px 0 black, -3px -3px 0 black, -3px 3px 0 black, 3px -3px 0 black, 2px 2px 0 black, -2px -2px 0 black, -2px 2px 0 black, 2px -2px 0 black, 1px 1px 0 black, -1px -1px 0 black, -1px 1px 0 black, 1px -1px 0 black' , display: 'flex', flexDirection: 'column', textAlign: 'center' }}>
            <div style={{fontSize: '40px', margin: '0px 100px 0px 0px' }}>auto</div>
            <div style={{fontSize: '70px', margin: '-20px 0px 0px 0px' }}>Tello</div>
        </div>
    </div>
  );
};

export default Loading

