import React from 'react'
import startIcon from '../img/startIcon.jpg'
import deleteIcon from '../img/deleteIcon.png'
import { Link } from 'react-router-dom'


const Room = ({ roomInformation, idx, onDelete }) => {
  return (
    <div style={{ height: '50px', width: '800px', margin: '5px 0px 0px 0px', display: 'flex', alignItems: 'center', border: '2px solid black', fontFamily: '"Abel", sans-serif' }}>
        <div style={{ height: '50px', width: '700px', fontSize: '27px', display: 'flex', alignItems: 'center' }}>
            <div style={{ margin: '0px 10px 0px 20px' }}>部屋名:{roomInformation.roomName},</div>
            <div style={{ margin: '0px 10px 0px 0px' }}>N:{roomInformation.N},</div>
            <div style={{ margin: '0px 10px 0px 0px' }}>M:{roomInformation.M},</div>
            <div style={{ margin: '0px 10px 0px 0px' }}>height:{roomInformation.height},</div>
            <div style={{ margin: '0px 10px 0px 0px' }}>width:{roomInformation.width}</div>
        </div>
        <Link to={{ pathname: "/home/setting/"+roomInformation.N+"/"+roomInformation.M+"/"+roomInformation.height+"/"+roomInformation.width }}>
            <button style={{ height: '48px', width: '50px', marginTop: '2px', backgroundImage: `url(${startIcon})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat', border: 'none', cursor: 'pointer' }}></button>
        </Link>
        <button onClick={onDelete} style={{ height: '48px', width: '50px', marginTop: '1px', backgroundImage: `url(${deleteIcon})`, backgroundSize: 'cover', backgroundRepeat: 'no-repeat', border: 'none', cursor: 'pointer' }}></button>
    </div>
  )
}

export default Room