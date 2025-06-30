import Heading from "../components/Heading";

export default function PrivacyPolicy() {
    return(
        <>
            <Heading text={"Persona Insight"} />

            <main className={"main"}>
                <div className={"left-container"}>
                    <img src={require("../assets/privacy-policy.png")} alt={"about-us"}/>
                    <img src={require("../assets/security-scan.png")} alt={"security-scan"}/>
                    <img src={require("../assets/data-security.png")} className={"icon"} alt={"data-security"}/>

                    <img src={require("../assets/ai-c.png")} className={"icon"} alt={"what-if-analysis"}/>
                    <img src={require("../assets/shield.png")} alt={"shield"}/>

                    <img src={require("../assets/data-icon.png")} className={"icon"} alt={"data-icon"}/>
                </div>
                <div className={"right-container"}>
                    <h2 style={{color: "white"}}>Privacy Policy</h2><br/>
                    <span className={"regular-text"}>
                        At <span className={"dynamic-word"}>Persona Insight</span>, your privacy is important to us.
                        We do not store, track, or retain any data beyond what
                        is necessary for user login and registration purposes.
                        The only information we collect is your registration
                        credentials (such as email and password), which are securely
                        stored and protected. We do not store or analyze any other
                        personal data, including any data from Twitter profiles you
                        choose to analyze. Rest assured, your privacy and security
                        are our top priorities.
                  </span>
                </div>
            </main>
        </>

    )
}
