import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../store/store";

export default function ProtectedRoute({ children }) {
    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user.id) {
            navigate('/');
        }
    }, [user, navigate]);

    return user.id ? children : null;
}