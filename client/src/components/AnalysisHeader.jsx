import React from "react";
import TraitsGrid from "./TraitsGrid";
import InsightsDisplay from "./InsightsDisplay";

export default function AnalysisHeader({ analysis, index = null }) {
    // Helper functions for display
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    const cleanString = (str) => {
        return str ? str.trim() : '';
    };

    return (
        <div className="analysis-header">
            <div>
                {index !== null && analysis.USERNAME && (
                    <h2 className="analysis-name">
                        Analysis #{index + 1} - {cleanString(analysis.USERNAME)}
                    </h2>
                )}
                <p className="analysis-date">
                    {formatDate(analysis.ANALYSIS_DATE)}
                </p>
            </div>
            <span className="tweet-count">
        {analysis.TWEETS_COUNT} tweets analyzed
      </span>
        </div>
    );
}