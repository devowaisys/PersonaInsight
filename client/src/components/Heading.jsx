import {Link} from "react-router-dom";
import "../store/store"
import {useContext} from "react";
import {UserContext} from "../store/store";

export default function Heading({text}) {
    const {user} = useContext(UserContext);
    return (
        <Link to={user.id === ""? "/": "/home"} className={"main-heading"}>{text}</Link>
    );
}