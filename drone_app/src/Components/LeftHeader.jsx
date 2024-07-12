import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const LeftHeader = () => {
  const location = useLocation();
  console.log(location.pathname)

  const getButtonStyle1 = (path) => ({
    fontSize: location.pathname.includes(path) ? '40px' : '25px',
    marginTop: location.pathname.includes(path) ? '145px' : '160px',
    backgroundColor: 'rgba(195, 251, 255, 0.5)',
    border: 'none',
    borderBottom: '2px solid black',
    fontFamily: '"Zen Dots", sans-serif',
    cursor: 'pointer'
  });

  const getButtonStyle2 = (path) => ({
    fontSize: location.pathname.includes(path) ? '30px' : '25px',
    marginTop: location.pathname.includes(path) ? '25px' : '30px',
    backgroundColor: 'rgba(195, 251, 255, 0.5)',
    border: 'none',
    borderBottom: '2px solid black',
    fontFamily: '"Zen Dots", sans-serif',
    cursor: 'pointer'
  });

  const getButtonStyle3 = (path) => ({
    fontSize: location.pathname.includes(path) ? '40px' : '25px',
    marginTop: location.pathname.includes(path) ? '15px' : '30px',
    backgroundColor: 'rgba(195, 251, 255, 0.5)',
    border: 'none',
    borderBottom: '2px solid black',
    fontFamily: '"Zen Dots", sans-serif',
    cursor: 'pointer'
  });

  return (
    <div style={{ height: '683px', width: '335.48px', backgroundColor: 'rgba(195, 251, 255, 0.5)', fontFamily: '"Zen Dots", sans-serif', borderRight: '2px solid black', display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
      <div style={{ fontSize: '49px', marginTop: '20px', cursor: 'pointer' }}>menu</div>
        <div style={{ height: '614px', width: '335.48px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Link to={'/home'}>
            <button style={getButtonStyle1('/home')}>Home</button>
          </Link>

          <Link to={'/registeredroom'}>
            <button style={getButtonStyle2('/registeredroom')}>registered_room</button>
          </Link>
          
          <Link to={'/howtouse'}>
            <button style={getButtonStyle3('/howtouse')}>How to use</button>
          </Link>
          
          {/*
          <div style={{ fontSize: '18px', marginTop: '40px' }}>known_face</div>
          <div style={{ fontSize: '18px', marginTop: '30px' }}>picture</div>
          */}
      </div>
    </div>
  );
};

export default LeftHeader;
