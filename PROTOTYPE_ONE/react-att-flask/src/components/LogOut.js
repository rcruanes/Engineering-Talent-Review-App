// LogoutButton.js
import React from 'react';
import { useAuth } from './AuthContext';

const LogoutButton = () => {
  const { logout } = useAuth();

  const handleLogout = () => {
    // Perform logout action (e.g., send logout request to backend)
    // Upon successful logout, call the logout function
    logout();
  };

  return <button onClick={handleLogout}>Logout</button>;
};

export default LogoutButton;
