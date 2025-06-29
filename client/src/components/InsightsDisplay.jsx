import React from "react";
import TraitsGrid from "./TraitsGrid";

export default function InsightsDisplay({ insights }) {
    // Helper function to group insights by type
    const groupInsightsByType = (insights) => {
        if (!insights) return null;

        const grouped = {};
        insights.forEach(insight => {
            if (!grouped[insight.INSIGHT_TYPE]) {
                grouped[insight.INSIGHT_TYPE] = [];
            }
            grouped[insight.INSIGHT_TYPE].push(insight.INSIGHT_TEXT);
        });
        return grouped;
    };

    if (!insights) {
        return <p className="no-insights">No insights available for this analysis</p>;
    }

    return (
        <div className="insights-section">
            <h3>Insights</h3>
            {Object.entries(groupInsightsByType(insights)).map(([type, insights]) => (
                <div key={type} className="insight-group">
                    <h4 className="insight-type">
                        {type.replace(/_/g, ' ').toLowerCase()}
                    </h4>
                    <ul className="insight-list">
                        {insights.map((insight, i) => (
                            <li key={i} className="insight-item">
                                {insight}
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
}