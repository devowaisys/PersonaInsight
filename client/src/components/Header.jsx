import Heading from "./Heading";
import NavigationMenu from "./NavigationMenu";

export default function Header({type, onClick}){
    return (
        <header>
            <Heading text={"Persona Insight"}/>
            <NavigationMenu type={type} onClick={onClick}/>
        </header>
    )
}