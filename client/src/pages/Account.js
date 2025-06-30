import Header from "../components/Header";
import Button from "../components/Button";
import { UserContext } from "../store/store";
import { useContext, useEffect, useState } from "react";
import {useNavigate} from "react-router-dom";
import Loader from "../components/Loader";

export default function Account() {
    const { user, token, updateUser, logout: contextLogout } = useContext(UserContext); // Changed to use updateUser
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [prevPass, setPrevPass] = useState("");
    const [newPass, setNewPass] = useState("");
    const [message, setMessage] = useState("");
    const [error, setError] = useState("");
    const [loaderVisible, setLoaderVisible] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (user) {
            setFullName(user.full_name || "");
            setEmail(user.email || "");
        }
    }, [user]);

    async function req_update(full_name, email, prev_pass, new_pass) {
        if (!full_name || !email || !prev_pass) {
            setError("Full name, email, and current password are required");
            return;
        }

        try {
            console.log("Sending update request with:", { full_name, email });
            console.log("Current token:", token);

            setError("");
            setMessage("");
            setLoaderVisible(true);

            const requestBody = {
                full_name: full_name,
                email: email,
                current_password: prev_pass,
            };

            if (new_pass && new_pass.trim() !== "") {
                requestBody.new_password = new_pass;
            }

            const timeoutMs = 10000;
            const response = await Promise.race([
                fetch(`http://127.0.0.1:5000/api/update_users`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                    body: JSON.stringify(requestBody),
                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
                ),
            ]);

            if (response) {
                const dataJson = await response.json();
                console.log("Response from server:", dataJson);

                if (response.ok && dataJson.success) {
                    setMessage("Your account info has been updated.");

                    // Use updateUser instead of addUser to preserve token
                    updateUser({
                        ...user,
                        full_name: full_name,
                        email: email,
                    });

                    setPrevPass("");
                    setNewPass("");
                } else {
                    setError(dataJson.error || dataJson.message ||
                        `Failed to update account (${response.status})`);
                }
            } else {
                setError("Request timed out. Please try again later.");
            }
        } catch (error) {
            console.error("Update error:", error);
            setError(error.message || "An error occurred. Please try again.");
        } finally {
            setLoaderVisible(false);
        }
    }

    async function logout(){
        try {
            console.log("Sending logout request");
            console.log("Current token:", token);

            setError("");
            setMessage("");
            setLoaderVisible(true);

            const timeoutMs = 10000;
            const response = await Promise.race([
                fetch(`http://127.0.0.1:5000/api/logout`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                }),
                new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
                ),
            ]);

            if (response) {
                const dataJson = await response.json();
                console.log("Response from server:", dataJson);

                if (response.ok && dataJson.success) {
                    setMessage("Your account info has been updated.");

                    contextLogout()
                    navigate('/')

                } else {
                    if (response.status === 401) {
                        let countdown = 3; // Starting countdown value
                        setError(
                            `Your session has expired. Redirecting in ${countdown} seconds...`
                        );

                        const interval = setInterval(() => {
                            countdown -= 1;
                            if (countdown > 0) {
                                setError(
                                    `Your session has expired. Redirecting in ${countdown} seconds...`
                                );
                            }
                        }, 1000); // Update message every second

                        setTimeout(() => {
                            clearInterval(interval); // Stop the countdown updates
                            contextLogout()
                            navigate("/");
                        }, 3000); // Redirect after 3 seconds

                    }

                }
            } else {
                setError("Request timed out. Please try again later.");
            }
        } catch (error) {
            console.error("Logout error:", error);
            setError(error.message || "An error occurred. Please try again.");
        } finally {
            setLoaderVisible(false);
        }
    }

    return (
        <>
            <Header type={false} />
            <main className={"main"}>
                <div className={"left-container"}>
                    <img src={require("../assets/secure-access.png")} alt={"wifi"} className={"icon"}/>
                    <img src={require("../assets/account-shield.png")} alt={"ai"} className={"icon"}/>
                    <img src={require("../assets/account.png")} alt={"deep-learning"} className={"icon"}/>
                    <img src={require("../assets/edit-info.png")} alt={"twitter"} className={"icon"}/>
                    <img src={require("../assets/person.png")} alt={"internet"} className={"icon"}/>
                    <img src={require("../assets/privacy-policy.png")} alt={"donut-chart"} className={"icon"}/>
                </div>
                <div className={"right-container"} style={{justifyContent: 'center', alignItems: 'center'}}>
                    <span className={"subheading"}>Account Management</span>
                    {loaderVisible && <Loader customStyles={{margin: "0 auto"}}/>}
                    {error && <span className={"error-text"}>{error}</span>}
                    {message && <span className={"regular-text"} style={{textAlign: "center"}}>**{message}**</span>}
                    <form className={"form-container-vertical"} onSubmit={e => e.preventDefault()}>
                        <input type="text" value={fullName}
                               className={"form-input"}
                               onChange={(e) => setFullName(e.target.value)}/><br/>
                        <input type="email" value={email}
                               className={"form-input"}
                               onChange={(e) => setEmail(e.target.value)}/><br/>
                        <input type="password" placeholder="Current Password" value={prevPass}
                               className={"form-input"}
                               onChange={(e) => setPrevPass(e.target.value)}/><br/>
                        <input type="password" placeholder="New Password (leave blank to keep current)" value={newPass}
                               className={"form-input"}
                               onChange={(e) => setNewPass(e.target.value)}/><br/>
                        <div className={'horizontal-btn-container'}>
                            <Button text={"Logout"} onClick={logout}/>
                            <Button text={"Update"} onClick={() => req_update(fullName, email, prevPass, newPass)}/>
                        </div>

                    </form>
                </div>
            </main>
        </>
    );
}