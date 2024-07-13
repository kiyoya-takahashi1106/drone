// src/pages/RegisteredRoom.jsx
import { useEffect, useState } from "react";
import { useParams } from 'react-router-dom';
import { collection, addDoc, getDocs, deleteDoc, doc } from "firebase/firestore";
import { db } from '../firebase';  // Firebaseの初期化設定をインポート
import TopHeader from '../Components/TopHeader';
import LeftHeader from '../Components/LeftHeader';
import Room from '../Components/Room';

function RegisteredRoom() {
  const params = useParams();
  useEffect(() => {
    console.log(params);
  }, [params]);

  const [roomName, setRoomName] = useState('');
  const [N, setN] = useState(params.N);
  const [M, setM] = useState(params.M);
  const [height, setHeight] = useState(params.height);
  const [width, setWidth] = useState(params.width);
  const [roomsInformation, setRoomsInformation] = useState([]);

  useEffect(() => {
    const fetchRooms = async () => {
      const querySnapshot = await getDocs(collection(db, "rooms"));
      const rooms = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setRoomsInformation(rooms);
    };

    fetchRooms();
  }, []);

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

  const handleClick = async () => {
    if (roomName === '' || N === '' || M === '' || height === '' || width === '') {
      alert('すべての項目を入力してください。');
      return;
    }
    if (roomName.length >= 9) {
      alert('部屋名を8文字以下にしてください');
      return;
    }
    
    const newRoom = {
      roomName: roomName,
      N: N,
      M: M,
      height: height,
      width: width
    };
    try {
      const docRef = await addDoc(collection(db, "rooms"), newRoom);
      setRoomsInformation([...roomsInformation, { id: docRef.id, ...newRoom }]);
      setRoomName('');
      setN('');
      setM('');
      setHeight('');
      setWidth('');
    } catch (e) {
      console.error("Error adding document: ", e);
    }
  };

  const deleteRoom = async (index, id) => {
    await deleteDoc(doc(db, "rooms", id));
    setRoomsInformation((prevRoomsInformation) => prevRoomsInformation.filter((_, i) => i !== index));
  };

  return (
    <div style={{ height: '832px', width: '1280px' }}>
      <TopHeader s={"Registered Room"} />
      <div style={{ display: 'flex' }}>
        <LeftHeader />
        <div style={{ height: '678px', width: '944px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <div style={{ height: '300px', width: '800px', margin: '39px 0px 20px 0px', border: '2px solid black' }}>
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
            <button onClick={handleClick} style={{ height: '50px', fontSize: '30px', fontFamily: '"Zen Dots", sans-serif', backgroundColor: '#D9D9D9', margin: '0px 0px 0px 350px', border: 'none', cursor: 'pointer' }}>Save with this content</button>
          </div>

          <div style={{}}>
            {roomsInformation.map((roomInformation, index) => (
              <div key={index}>
                <Room roomInformation={roomInformation} idx={index} onDelete={() => deleteRoom(index, roomInformation.id)} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisteredRoom;