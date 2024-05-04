import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext(null);

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [authInfo, setAuthInfo] = useState({
        isAuthenticated: false,
        authToken: null,
        role: null,
    });

    const login = (token, role) => {
        setAuthInfo({
            isAuthenticated: true,
            authToken: token,
            role: role,
        });
        localStorage.setItem('authToken', token);
        localStorage.setItem('userRole', role);
    };

    const logout = () => {
        setAuthInfo({
            isAuthenticated: false,
            authToken: null,
            role: null,
        });
        localStorage.clear();  // Clears all local storage items
    };

    return (
        <AuthContext.Provider value={{ ...authInfo, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthProvider;
