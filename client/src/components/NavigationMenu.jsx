import Button from "./Button";
import {Link} from "react-router-dom";

export default function NavigationMenu({onClick, type}){
    return(
        <nav className={"navigation-menu"}>
            {
                type &&  <Button text={"Get Started"} onClick={onClick} />
            }

            <ul className={"navigation-list"}>
                {
                    !type &&
                    <>
                        <li className={"nav-item"}><Link to="/dashboard">Dashboard</Link></li>
                        <li className={"nav-item"}><Link to="/history">History</Link></li>
                    </>
                }
                <li className={"nav-item"}><Link to="/about">About</Link></li>
                <li className={"nav-item"}><Link to="/privacy-policy">Privacy Policy</Link></li>
                <li className={"nav-item"}><Link to="/account">
                    <img className={"icon"} src={require("../assets/user.png")} alt={"icon"}/>
                </Link></li>
            </ul>
        </nav>
    )
}