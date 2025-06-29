import React from "react";

export default function TraitsGrid({ traits }) {
    return (
        <div className="traits-section">
            <h3>Personality Traits</h3>
            <div className="traits-grid">
                <div className="trait-box">
                    <p className="trait-label">Openness</p>
                    <p className="trait-value">{traits.AVERAGE_OPENNESS}</p>
                </div>
                <div className="trait-box">
                    <p className="trait-label">Conscientiousness</p>
                    <p className="trait-value">{traits.AVERAGE_CONSCIENTIOUSNESS}</p>
                </div>
                <div className="trait-box">
                    <p className="trait-label">Extraversion</p>
                    <p className="trait-value">{traits.AVERAGE_EXTRAVERSION}</p>
                </div>
                <div className="trait-box">
                    <p className="trait-label">Agreeableness</p>
                    <p className="trait-value">{traits.AVERAGE_AGREEABLENESS}</p>
                </div>
                <div className="trait-box">
                    <p className="trait-label">Neuroticism</p>
                    <p className="trait-value">{traits.AVERAGE_NEUROTICISM}</p>
                </div>
            </div>
        </div>
    );
}