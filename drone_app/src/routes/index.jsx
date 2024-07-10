import { BrowserRouter, Routes, Route } from "react-router-dom";
import Loading from "../main/Loading";
import Home from "../main/Home";
import RegisteredRoom from "../main/RegisteredRoom";
import TelloSetting from "../main/TelloSetting";
import WifiConnect from "../main/WifiConnect";

const Rooter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Loading />} />
                <Route path="/home" element={<Home />} />
                <Route path="/home/setting" element={<TelloSetting />} />
                <Route path="/home/setting/wificonnect" element={<WifiConnect />} />
                <Route path="/registeredroom/:N/:M/:height/:width" element={<RegisteredRoom />} />
                <Route path="/registeredroom" element={<RegisteredRoom />} />
            </Routes>
        </BrowserRouter>
    )
}
export default Rooter;