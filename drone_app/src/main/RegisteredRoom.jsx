import { useEffect, useState } from "react";
import { useLocation, useParams } from 'react-router-dom';
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';

function RegisteredRoom() {
  const location = useLocation();
  const { initM, initN, initHeight, initWidth } = location.state || {};
  console.log("initM", initM)
  console.log("initN", initN)
  console.log("initHeight", initHeight)
  console.log("initWidth", initWidth)
  const [roomName, setRoomName] = useState('');
  const [M, setM] = useState(initM || '');
  const [N, setN] = useState(initN || '');
  const [height, setHeight] = useState(initHeight || '');
  const [width, setWidth] = useState(initWidth || '');
  const params = useParams();
  useEffect(() => {
    console.log(params);
  }, [params]);
  const handleSetRoomName = (event) => {
    setRoomName(event.target.value);
  };

  const handleSetN = (event) => {
    setN(event.target.value);
  };

  const handleSetM = (event) => {
    setM(event.target.value);
  };

  const handleSetHeight = (event) => {
    setHeight(event.target.value);
  };

  const handleSetWidth = (event) => {
    setWidth(event.target.value);
  };

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Registered Room"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', justifyContent: 'center' }}>
          <div style={{ height: '300px', width: '800px', margin: '39px 0px 0px 0px', border: '2px solid black' }}>
            <div style={{ height: '240px', width: '700px', display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center', fontSize: '36px', marginLeft: '30px', fontFamily: '"Abel", sans-serif' }}>
              <div style={{ display: "flex" }}>
                <div style={{ margin: '10px 30px 0px -68px' }}>部屋名:</div>
                <input type="text" value={roomName} onChange={handleSetRoomName} style={{ height: '60px', width: '400px', fontSize: '40px', margin: '5px 0px 0px 0px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
              <div style={{ display: "flex", marginTop: '20px' }}>
                <div style={{ marginRight: '50px' }}>個数:</div>
                <div>N(縦) =</div>
                <input type="number" value={N} onChange={handleSetN} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '40px' }}>,</div>
                <div>M(横) =</div>
                <input type="number" value={M} onChange={handleSetM} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
              </div>
              <div style={{ display: "flex", marginTop: '10px' }}>
                <div style={{ marginRight: '46px' }}>長さ:</div>
                <div>height =</div>
                <input type="number" value={height} onChange={handleSetHeight} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
                <div style={{ marginRight: '45px' }}>,</div>
                <div>width =</div>
                <input type="number" value={width} onChange={handleSetWidth} style={{ height: '60px', width: '100px', fontSize: '40px', textAlign: 'center', backgroundColor: '#D9D9D9', border: 'none', borderRadius: '30px', cursor: 'pointer' }}></input>
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