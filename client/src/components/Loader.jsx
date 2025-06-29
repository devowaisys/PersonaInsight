import { useEffect, useState, useRef } from "react";

export default function Loader({text, customStyles}) {
    const [currentWord, setCurrentWord] = useState("Fetching Tweets");
    const [fadeOut, setFadeOut] = useState(false);
    const words = useRef([
        "Fetching Tweets",
        "Analyzing data",
        "Running OCEAN Analysis",
        "Running Sentiment Analysis",
        "Thanks for your patience",
        "Almost there",
        "It might take a little bit longer depending upon your internet speed.",
        "Bear with us"
    ]);

    useEffect(() => {
        let wordIndex = 0;
        const interval = setInterval(() => {
            setFadeOut(true);
            setTimeout(() => {
                wordIndex = (wordIndex + 1) % words.current.length;
                setCurrentWord(words.current[wordIndex]);
                setFadeOut(false);
            }, 500);
        }, 3000);

        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <div className="loader" style={customStyles ? customStyles : {}}></div>
            {text ? (
                <span className={`regular-text ${fadeOut ? "fade-out" : "fade-in"}`}
                      style={{ textAlign: "center", marginBottom: "-3rem" }}>
                {currentWord}
            </span>
            ) : ""}
        </>

);
}
