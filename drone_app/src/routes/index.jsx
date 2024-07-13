import { BrowserRouter, Routes, Route } from "react-router-dom";
import Loading from "../main/Loading";
import Home from "../main/Home";
import TelloSetting from "../main/TelloSetting";
import RegisteredRoom from "../main/RegisteredRoom";
import HowToUse from "../main/HowToUse";
import ExecutionPhase from "../main/ExecutionPhase";

const Rooter = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Loading />} />
                <Route path="/home" element={<Home />} />

                {/* <Route path="/home/setting" element={<TelloSetting />} /> */}
                <Route path="/home/setting/:N/:M/:height/:width" element={<TelloSetting />} />

                {/* <Route path="/home/setting/wificonnect" element={<WifiConnect />} /> */}
                <Route path="/home/setting/executionphase/:N/:M/:height/:width" element={<ExecutionPhase />} />

                <Route path="/registeredroom" element={<RegisteredRoom />} />
                <Route path="/registeredroom/:N/:M/:height/:width" element={<RegisteredRoom />} />

                <Route path="/howtouse" element={<HowToUse />} />
            </Routes>
        </BrowserRouter>
    )
}
export default Rooter;