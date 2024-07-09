import React from 'react';
import TopHeader from './Components/TopHeader';
import LeftHeader from './Components/LeftHeader';
import { useState } from 'react';

function App() {
  const [N, setN] = useState(null)
  const [M, setM] = useState(null)
  const [height, setHeight] = useState(null)
  const [width, setWidth] = useState(null)
  const handleSetN = (event) => {
    setN(event.target.value);
  }
  const handleSetM = (event) => {
    setM(event.target.value);
  }
  const handleSetHeight = (event) => {
    setHeight(event.target.value);
  }
  const handleSetWidth = (event) => {
    setWidth(event.target.value);
  }

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px' }}>
          <div style={{ height: '471px', width: '944px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ height: '431px', width: '815px', marginTop: '20px', borderRadius: '50px', backgroundColor: '#D9D9D9' }}>
            </div>
          </div>
          <div style={{ height: '206px', width: '944px', display: 'flex' }}>
            <div style={{ height: '206px', width: '708px', fontSize: '36px', fontFamily: '"Abel", sans-serif' }}>
              <div style={{ marginTop: '45px', marginLeft: '45px', display: 'flex' }}>
                <div style={{ marginRight: '50px' }}>個数:</div>
                <div>N(縦) =</div>
                <input type="number" value={N} onChange={handleSetN} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '40px' }}>,</div>
                <div>M(横) =</div>
                <input type="number" value={M} onChange={handleSetM} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
              <div style={{ marginTop: '10px', marginLeft: '45px', display: 'flex' }}>
                <div style={{ marginRight: '46px' }}>長さ:</div>
                <div>height =</div>
                <input type="number" value={height} onChange={handleSetHeight} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '45px' }}>,</div>
                <div>width =</div>
                <input type="number" value={width} onChange={handleSetWidth} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
            </div>

            <div style={{ height: '206px', width: '236px', fontFamily: '"Zen Dots", sans-serif', display: 'flex', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column' }}>
                <button style={{ height: '70px', width: '180px', fontSize: '40px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', marginTop: '70px', border: 'none', cursor: 'pointer' }}>Next</button>
                <button style={{ border: 'none', fontSize: '30px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: 'white', marginTop: '12px', cursor: 'pointer' }}>Save</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
