// Loading.jsx
import React, { useState, useEffect } from 'react';
import './Loading.css'; // Import CSS file for styling

const Loading = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay with setTimeout
    const timer = setTimeout(() => {
      setLoading(false);
    }, 3500); // Adjust the time as needed

    // Clean up the timer on component unmount
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="loading-container" style={{ display: loading ? 'flex' : 'none' }}>
      <img src="https://media.giphy.com/avatars/WDemojis/2GqVcpH4rKdT/200h.gif" alt="Loading" className="loading-gif" />
    </div>
  );
}

export default Loading;
