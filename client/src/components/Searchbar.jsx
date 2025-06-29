import Button from "./Button";

export default function Searchbar({onClick, onChange}) {
    return (
        <>
            <input type={"search"} className={"searchbar"} placeholder={"Profile Link"} onChange={(e) => onChange(e.target.value)}/>
            <Button text={"Search"} onClick={onClick}/>
        </>

    )

}