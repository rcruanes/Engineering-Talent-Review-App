// src/components/ProtectedRoute.js
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from './AuthContext';  // Adjust the path as necessary
import AccessDeniedDialog from './AccessDeniedDialog';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const { authToken, role } = useAuth();
    const location = useLocation();
    

    if (!authToken) {
        return <Navigate to="/" state={{ from: location }} replace />;
    }

    if (!allowedRoles.includes(role)) {
        console.log({'current role ': role});
        return <AccessDeniedDialog />;
    }

    return children;
};

export default ProtectedRoute;
