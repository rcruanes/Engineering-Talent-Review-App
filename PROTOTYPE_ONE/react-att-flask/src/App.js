import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    pw: '',
    confirm_pw: '',
    role: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log('Form Data:', formData); // Log the form data before sending the request
      const response = await axios.post('http://127.0.0.1:5000/user/create', formData);
      console.log('User created:', response.data);
      // Optionally, handle success response (e.g., redirect to dashboard)
    } catch (error) {
      console.error('Error creating user:', error.response); // Log the error response
      // Optionally, handle error response (e.g., display error messages)
    }
  };

  return (
    <div className="d-flex justify-content-around">
      <form onSubmit={handleSubmit} className="col-4 p-4 bg-dark text-light">
        <h2 className="text-primary">Register</h2>
        <input type="text" name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleChange} className="form-control" />
        <input type="text" name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleChange} className="form-control" />
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} className="form-control" />
        <input type="password" name="pw" placeholder="Password" value={formData.pw} onChange={handleChange} className="form-control" />
        <input type="password" name="confirm_pw" placeholder="Confirm Password" value={formData.confirm_pw} onChange={handleChange} className="form-control" />
        <select name="role" value={formData.role} onChange={handleChange} className="form-control">
          <option value="">Select Role</option>
          <option value="Nominator">Nominator</option>
          <option value="Recommender">Recommender</option>
          <option value="ReviewCommittee">ReviewCommittee</option>
        </select>
        <button type="submit" className="btn btn-primary">Register</button>
      </form>
    </div>
  );
}

export default App;
