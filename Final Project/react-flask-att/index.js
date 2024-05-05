import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { AuthProvider } from './components/AuthContext'; // Adjust the path if necessary
import reportWebVitals from './reportWebVitals';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:5000';
axios.defaults.withCredentials = true; // Ensure credentials are sent with each request


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider> {/* Provide AuthContext to the entire app */}
      <App />
    </AuthProvider>
  </React.StrictMode>
);

// Optional: Setup for measuring and reporting web vitals
reportWebVitals(console.log);
