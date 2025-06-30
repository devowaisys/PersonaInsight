import React, { useEffect, useState, useContext } from "react";
import { UserContext } from "../store/store";
import Loader from "../components/Loader";
import Header from "../components/Header";
import {
    BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend
} from "recharts";

export default function Dashboard() {
    const [data, setData] = useState([]);
    const [loaderVisible, setLoaderVisible] = useState(false);
    const [error, setError] = useState(null);
    const { token, user } = useContext(UserContext);

    useEffect(() => {
        async function fetchData() {
            setLoaderVisible(true);
            setError(null);
            try {

                const response = await fetch(`http://127.0.0.1:5000/api/get_analysis_by_email?email=${user.email}`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                });

                const json = await response.json();
                if (response.ok && json.success) {
                    setData(json.analyses);
                } else {
                    setError(json.message || "Failed to load dashboard data");
                }
            } catch (err) {
                setError("Error fetching data");
                console.error(err);
            } finally {
                setLoaderVisible(false);
            }
        }
        fetchData();
    }, []);

    const traitLabels = [
        "AVERAGE_OPENNESS",
        "AVERAGE_CONSCIENTIOUSNESS",
        "AVERAGE_EXTRAVERSION",
        "AVERAGE_AGREEABLENESS",
        "AVERAGE_NEUROTICISM"
    ];

    const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#ff8042", "#8dd1e1"];

    const averageTraits = traitLabels.map(trait => {
        const total = data.reduce((sum, item) => sum + parseFloat(item[trait] || 0), 0);
        const avg = data.length ? total / data.length : 0;
        return {
            name: trait.replace("AVERAGE_", ""),
            value: parseFloat(avg.toFixed(2))
        };
    });

    return (
        <>
            <Header type={false} />
            <h1 className="history-title">Dashboard Overview</h1>
            <div className="dashboard-container">
                {loaderVisible && <Loader customStyles={{ margin: "0 auto" }} />}
                {error && <p className="error-text">{error}</p>}

                {!loaderVisible && !error && (
                    <div className="dashboard-content">
                        <div className="summary-card">
                            <h2>Total Analyses</h2>
                            <p>{data.length}</p>
                        </div>

                        <div className="chart-section">
                            <h3>Average Personality Traits</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={averageTraits}>
                                    <XAxis dataKey="name" />
                                    <YAxis domain={[0, 10]} />
                                    <Tooltip />
                                    <Bar dataKey="value" fill="#8884d8" />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>

                        <div className="chart-section">
                            <h3>Pie Chart Overview</h3>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={averageTraits}
                                        dataKey="value"
                                        nameKey="name"
                                        cx="50%"
                                        cy="50%"
                                        outerRadius={100}
                                        fill="#82ca9d"
                                        label
                                    >
                                        {averageTraits.map((entry, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                    <Legend />
                                </PieChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                )}
            </div>
        </>
    );
}
