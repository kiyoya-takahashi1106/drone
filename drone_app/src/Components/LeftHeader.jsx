import React from 'react';
import { Link } from 'react-router-dom';

const LeftHeader = () => {
  return (
    <div style={{ height: '683px', width: '335.48px', backgroundColor: 'rgba(195, 251, 255, 0.5)', fontFamily: '"Zen Dots", sans-serif', borderRight: '2px solid black', display: 'flex', alignItems: 'center', flexDirection: 'column' }}>
      <div style={{ fontSize: '49px', marginTop: '20px', cursor: 'pointer' }}>menu</div>
      <Link to={'/home'}>
        <button style={{ fontSize: '25px', marginTop: '30px', backgroundColor: 'rgba(195, 251, 255, 0.5)', border: 'none', borderBottom: '2px solid black', fontFamily: '"Zen Dots", sans-serif', cursor: 'pointer' }}>Home</button>
      </Link>
      <Link to={'/registeredroom'}>
        <button style={{ fontSize: '25px', marginTop: '30px', backgroundColor: 'rgba(195, 251, 255, 0.5)', border: 'none', borderBottom: '2px solid black', fontFamily: '"Zen Dots", sans-serif', cursor: 'pointer' }}>registered_room</button>
      </Link>
      <button style={{ fontSize: '25px', marginTop: '30px', backgroundColor: 'rgba(195, 251, 255, 0.5)', border: 'none', borderBottom: '2px solid black', fontFamily: '"Zen Dots", sans-serif', cursor: 'pointer' }}>How to use</button>

      {/*
      <div style={{ fontSize: '18px', marginTop: '40px' }}>known_face</div>
      <div style={{ fontSize: '18px', marginTop: '30px' }}>picture</div>
      */}
    </div>
  );
};

export default LeftHeader;
