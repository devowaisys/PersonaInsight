import Header from "../components/Header";
import { useContext, useState, useEffect } from "react";
import { UserContext } from "../store/store";
import Loader from "../components/Loader";
import TraitsGrid from "../components/TraitsGrid";
import InsightsDisplay from "../components/InsightsDisplay";
import AnalysisHeader from "../components/AnalysisHeader";

export default function History() {
    const [sample_res, setSample_res] = useState({ analyses: [] });
    const [error, setError] = useState(null);
    const [loaderVisible, setLoaderVisible] = useState(false);
    const [message, setMessage] = useState(null);
    const { token, user } = useContext(UserContext);

    async function getHistory() {
        setLoaderVisible(true);
        setError(null);
        try {
            setError("");
            setMessage("");
            const timeoutMs = 10000;
            const response = await Promise.race([
                fetch(`http://127.0.0.1:5000/api/get_analysis_by_email?email=${user.email}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
                ),
            ]);

            if (response) {
                const dataJson = await response.json();
                console.log("Response from server:", dataJson);

                if (response.ok && dataJson.success) {
                    setMessage("History loaded successfully");
                    setSample_res(dataJson);
                } else {
                    setError(dataJson.error || dataJson.message ||
                        `Failed to get history`);
                }
            } else {
                setError("Request timed out. Please try again later.");
            }
        } catch (error) {
            console.error("History error:", error);
            setError(error.message || "An error occurred. Please try again.");
        } finally {
            setLoaderVisible(false);
        }
    }

    // Use useEffect to call getHistory when component mounts
    useEffect(() => {
        getHistory();
    }, []);

    return (
        <>
            <Header type={false} />
            <h1 className="history-title">Analysis History</h1>
            <div className="history-container">
                {loaderVisible && <Loader customStyles={{ margin: "0 auto" }} />}
                {error && <span className={"error-text"}>{error}</span>}
                {message && <span className={"regular-text"} style={{ textAlign: "center" }}>**{message}**</span>}
                <div className="analyses-list">
                    {sample_res.analyses.map((analysis, index) => (
                        <div key={analysis.ANALYSIS_ID} className="analysis-card">
                            <AnalysisHeader analysis={analysis} index={index} />
                            <TraitsGrid traits={analysis} />
                            <InsightsDisplay insights={analysis.insights} />
                        </div>
                    ))}
                </div>
            </div>
        </>
    );
}