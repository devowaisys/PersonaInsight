import { useEffect, useState, useRef } from "react";
import Header from "../components/Header";
import LoginPopup from "../components/LoginPopup";
import RegisterPopup from "../components/RegisterPopup";

export default function Index() {
    const [popupOpenLogin, setPopupOpenLogin] = useState(false);
    const [popupOpenRegister, setPopupOpenRegister] = useState(false);
    const [currentWord, setCurrentWord] = useState("Discover");
    const [fadeOut, setFadeOut] = useState(false);
    const words = useRef(["Discover", "Analyze", "Understand", "and Unveil"]);

    useEffect(() => {
        let wordIndex = 0;
        const interval = setInterval(() => {
            setFadeOut(true);
            setTimeout(() => {
                wordIndex = (wordIndex + 1) % words.current.length;
                setCurrentWord(words.current[wordIndex]);
                setFadeOut(false);
            }, 500);
        }, 2500);

        return () => clearInterval(interval);
    }, []);

    function handlePopupOpenRegister(){
        setPopupOpenRegister(!popupOpenRegister);
        setPopupOpenLogin(false);
    }
    return (
        <>
            <Header type={true} onClick={() => setPopupOpenLogin(!popupOpenLogin)} />
            <main className="main">
                <div className="left-container">
                    <img src={require("../assets/wifi.png")} alt={"wifi"} className={"icon"}/>
                    <img src={require("../assets/ai-c.png")} alt={"ai"} className={"icon"}/>
                    <img src={require("../assets/deep-learning-c.png")} alt={"deep-learning"} className={"icon"}/>
                    <img src={require("../assets/twitter.png")} alt={"twitter"} className={"icon"}/>
                    <img src={require("../assets/internet.png")} alt={"internet"} className={"icon"}/>
                    <img src={require("../assets/donut-chart-c.png")} alt={"donut-chart"} className={"icon"}/>
                </div>
                <div className="right-container">
                    <span className="intro-text">
                        <span className={`dynamic-word ${fadeOut ? "fade-out" : "fade-in"}`}>{currentWord}</span>, <br/>
                        the Personality Behind Any X (Twitter) Profile.
                    </span>
                </div>
                {popupOpenLogin ?  <LoginPopup onCancel={() => setPopupOpenLogin(false)} onRegister={handlePopupOpenRegister}/> : ""}
                {popupOpenRegister ?  <RegisterPopup onCancel={() => setPopupOpenRegister(false)}/> : ""}
            </main>
        </>
    );
}
