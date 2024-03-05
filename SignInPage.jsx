import React, { useState } from 'react';
import './SignInPage.css'; // Import CSS file for styling

const SignInPage = ({ onSignIn }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    // Basic validation, replace with your authentication logic
    if (username === 'admin' && password === 'password') {
      onSignIn(username); // Call parent component function to indicate successful sign-in
    } else {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="container">
      <h2>Sign In</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit">Sign In</button>
        {error && <p>{error}</p>}
      </form>
    </div>
  );
}

export default SignInPage;
