import Button from "./Button";
import {useState} from "react";
import Loader from "./Loader";

export default function RegisterPopup({onCancel, onSubmit}) {
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");
    const [fullName, setFullName] = useState("")
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loaderVisible, setLoaderVisible] = useState(false)

    async function req_register(full_name, email, password) {
        setMessage("");
        setError("");
        if (!full_name || !email || !password) {
            setError("Please check the input fields");
            return;
        }
        if(!email.endsWith('.com') || !email.includes('@')){
            setError("Please provide a valid email address");
            return
        }
        if(password.length < 8){
            setError("Password should be greater than 8 characters.");
            return
        }
        try {
            setError("")
            setMessage("")
            setLoaderVisible(true);
            const timeoutMs = 10000;
            const response = await Promise.race([
                fetch(`http://127.0.0.1:5000/api/add_user`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        full_name: full_name,
                        email: email,
                        password: password,
                    }),
                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
                ),
            ]);

            if (response) {
                const data = await response.text();
                const dataJson = JSON.parse(data);
                console.log(dataJson)
                if (response.status >= 200 && response.status < 300) {
                    if (dataJson.success === true) {
                        setMessage("Your account has been created successfully.")

                    } else if (dataJson.success === false) {
                        setError(dataJson.error);
                    }
                } else {
                    if(dataJson.message.includes("Email already exists")){
                        setError('User already exists');
                    }
                    console.log(dataJson.message);
                }
            } else {
                setError("Request timed out. Please try again later.");
            }
        } catch (error) {
            setError("An error occurred. Please try again later.");
        } finally {
            setLoaderVisible(false)
        }
    }

    return (
        <div className="popup-overlay">
            <div className="popup-content">

                <div onClick={onCancel} className={"cancel-btn"}></div>
                <h1>Register</h1>
                {loaderVisible ? <Loader customStyles={{margin: "0 auto"}}/> : ""}
                <p className={"error-text"} >{error}</p>
                <p className={"regular-text"} style={{textAlign: "center", width: '100%'}}>{message ? `**${message}**` : ""}</p>
                <form method={"POST"} className={"form-container-vertical"}
                      onSubmit={(event) => event.preventDefault()}>
                    <label className={"form-label"}>Full Name</label><br/>
                    <input type="text" name="fullname" id="fullname" placeholder="Full Name" className={"form-input"}
                           onChange={(event) => setFullName(event.target.value)}/><br/>
                    <label className={"form-label"}>Email</label><br/>
                    <input type="email" name="email" id="email" placeholder="Email" className={"form-input"}
                           onChange={(event) => setEmail(event.target.value)}/><br/>
                    <label className={"form-label"}>Password</label><br/>
                    <input type="password" name="password" id="password" placeholder="Password"
                           className={"form-input"} onChange={(event) => setPassword(event.target.value)}/><br/>
                    <Button text={"Register"} onClick={() => req_register(fullName, email, password)}/>

                </form>
            </div>
        </div>
    )
}