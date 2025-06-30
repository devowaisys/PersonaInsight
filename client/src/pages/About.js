import Heading from "../components/Heading";

export default function About() {
  return(
      <>
          <Heading text={"Persona Insight"} />

          <main className={"main"}>
              <div className={"left-container"}>
                  <img src={require("../assets/about.png")} className={"icon"} alt={"about"}/>
                  <img src={require("../assets/exclamation.png")} alt={"exclamation"}/>
                  <img src={require("../assets/question-mark.png")} alt={"question-mark"}/>
                  <img src={require("../assets/what-if-analysis.png")} alt={"what-if-analysis"}/>
                  <img src={require("../assets/about-us.png")} alt={"about-us"}/>
                  <img src={require("../assets/ai-c.png")} className={"icon"} alt={"ai"}/>
              </div>
              <div className={"right-container"}>
              <h2 style={{color: "white"}}>About Us</h2><br/>
                  <span className={"regular-text"}>
                      At <span className={"dynamic-word"}>Persona Insight</span>, we specialize in analyzing digital
                      personas to help you uncover deeper insights into any Twitter
                      profile. Using cutting-edge AI and personality analysis based
                      on the OCEAN model, we transform social data into meaningful
                      interpretations. Our mission is to provide a tool that empowers
                      individuals and organizations to understand online behavior and
                      personalities better, enabling informed decisions and deeper
                      connections. Whether you're curious about yourself or someone else,
                      we offer a reliable way to unveil the personality behind the profile.
                  </span>
              </div>
          </main>
      </>

  )
}
