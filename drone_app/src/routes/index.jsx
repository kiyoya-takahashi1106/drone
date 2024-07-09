import { BrowserRouter, Routes, Route } from "react-router-dom";
import Loading from "../main/Loading";
import Home from "../main/Home";
import RegisteredRoom from "../main/RegisteredRoom";
import WifiConnect from "../main/WifiConnect";

const Rooter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Loading />} />
                <Route path="/home" element={<Home />} />
                <Route path="/home/wificonnect" element={<WifiConnect />} />
                <Route path="/registeredroom" element={<RegisteredRoom />} />
                
            </Routes>
        </BrowserRouter>
    )
}
export default Rooter;