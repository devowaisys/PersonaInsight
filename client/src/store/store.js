import { createContext, useCallback, useState } from "react";

export const UserContext = createContext({
    user: {
        id: "",
        full_name: "",
        email: "",
    },
    token: "",
    addUser: (userData, token) => {},
    updateUser: (userData) => {},  // New function
    setToken: (token) => {},       // New function
    removeUser: () => {},
    resetData: () => {},
    logout: () => {},  // Add this new function
});

export default function UserContextProvider({ children }) {
    const [user, setUser] = useState(() => {
        const savedUser = localStorage.getItem('user');
        return savedUser ? JSON.parse(savedUser) : {
            id: "",
            full_name: "",
            email: "",
        };
    });

    const [token, setToken] = useState(() => {
        return localStorage.getItem('token') || "";
    });

    // For initial login/signup (sets both user and token)
    const addUser = useCallback((userData, authToken) => {
        setUser(userData);
        setToken(authToken);
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('token', authToken);
    }, []);

    // For updating user data only (preserves token)
    const updateUser = useCallback((userData) => {
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        // Token remains unchanged
    }, []);

    // For updating token only (preserves user data)
    const setAuthToken = useCallback((authToken) => {
        setToken(authToken);
        localStorage.setItem('token', authToken);
    }, []);

    const removeUser = useCallback(() => {
        setUser({
            id: "",
            full_name: "",
            email: "",
        });
        setToken("");
        localStorage.removeItem('user');
        localStorage.removeItem('token');
    }, []);

    const resetData = useCallback(() => {
        removeUser();
    }, [removeUser]);

    const logout = useCallback(() => {
        // Clear user data and token
        removeUser();

        // You might want to add additional cleanup here if needed
        console.log("User logged out successfully");
    }, [removeUser]);

    const value = {
        user,
        token,
        addUser,
        updateUser,  // Expose new function
        setToken: setAuthToken,  // Expose token setter
        removeUser,
        resetData,
        logout
    };

    return <UserContext.Provider value={value}>{children}</UserContext.Provider>;
}