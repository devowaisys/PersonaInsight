import Button from "./Button";
import { useState, useContext } from "react";
import Loader from "./Loader";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../store/store";

export default function LoginPopup({ onCancel, onRegister }) {
    const [error, setError] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loaderVisible, setLoaderVisible] = useState(false);
    const navigate = useNavigate();
    const userContext = useContext(UserContext);

    async function req_login(email, password) {
        if (!email || !password) {
            setError("Please check the input fields");
            return;
        }
        if(!email.endsWith('.com') || !email.includes('@')){
            setError("Please provide a valid email address");
            return
        }
        if(!password.length > 8){
            setError("Password should be greater than 8 characters.");
            return
        }
        try {
            setError("");
            setLoaderVisible(true);
            const timeoutMs = 10000;
            const response = await Promise.race([
                fetch(`http://127.0.0.1:5000/api/users/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        email: email,
                        password: password,
                    }),

                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
                ),
            ]);

            if (response) {
                const dataJson = await response.json();
                console.log(dataJson)
                if (response.status >= 200 && response.status < 300) {

                    if (dataJson.success === true) {
                        userContext.addUser(
                            {
                                id: dataJson.user.ID,
                                full_name: dataJson.user.FULLNAME,
                                email: dataJson.user.EMAIL,
                            },
                            dataJson.access_token
                        );
                        navigate('/home');
                    } else if(dataJson.success === false){
                        setError(dataJson.error);
                    }
                } else {
                    setError(dataJson.error);
                }
            } else {
                setError("Request timed out. Please try again later.");
            }
        } catch (error) {
            setError("An error occurred. Please try again later.");
        } finally {
            setLoaderVisible(false);
        }
    }

    return (
        <div className="popup-overlay">
            <div className="popup-content">
                <div onClick={onCancel} className={"cancel-btn"}></div>
                <h1>Login</h1>
                {loaderVisible ? <Loader customStyles={{margin: "0 auto"}}/> : ""}
                <span className={"error-text"}>{error}</span>
                <form method={"POST"} className={"form-container-vertical"} onSubmit={(e) => e.preventDefault()}>
                    <label className={"form-label"}>Email</label><br/>
                    <input type="email" name="email" id="email" placeholder="Email" className={"form-input"} onChange={(event) => setEmail(event.target.value)}/><br/>
                    <label className={"form-label"}>Password</label><br/>
                    <input type="password" name="password" id="password" placeholder="Password" className={"form-input"} onChange={(event) => setPassword(event.target.value)}/><br/>
                    <div className={"form-container-horizontal"}>
                        <Button text={"Register"} onClick={onRegister}/>
                        <Button text={"Login"} onClick={() => req_login(email, password)}/>
                    </div>
                </form>
            </div>
        </div>
    );
}