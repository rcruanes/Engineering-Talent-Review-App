import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, FormControl, InputLabel, Select, MenuItem, Container, Paper, Typography } from '@mui/material';
import { useAuth } from './AuthContext';

function RegistrationForm() {
  const [formData, setFormData] = useState({
    email: '',
    pw: '',
    first_name: '',
    last_name: '',
    confirm_pw: '',
    role: '',
    isLogin: true
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const { login } = useAuth();

  const handleSubmit = async (e) => {
      e.preventDefault();
      const endpoint = formData.isLogin ? '/user/login' : '/user/create';
      try {
          const response = await axios.post(`http://127.0.0.1:5000${endpoint}`, formData);
          if (response.data.access_token) {
              login(response.data.access_token, response.data.role);
              console.log(response.data)
              navigate('/dashboard');
          }
      } catch (error) {
          console.error('Error:', error.response ? error.response.data : 'Error during the request');
      }
  };

  const toggleForm = () => {
    setFormData({
      ...formData,
      isLogin: !formData.isLogin
    });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} style={{ padding: 20, marginTop: '20vh' }}> {/* Added Paper and style for centering */}
        <Typography variant="h5" component="h1" gutterBottom>
          {formData.isLogin ? 'Login' : 'Register'}
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Email"
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Password"
            type="password"
            name="pw"
            value={formData.pw}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          {!formData.isLogin && (
            <>
              <TextField
                label="First Name"
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Last Name"
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                fullWidth
                margin="normal"
              />
              <TextField
                label="Confirm Password"
                type="password"
                name="confirm_pw"
                value={formData.confirm_pw}
                onChange={handleChange}
                fullWidth
                margin="normal"
              />
              <FormControl fullWidth margin="normal">
                <InputLabel>Role</InputLabel>
                <Select
                  name="role"
                  value={formData.role}
                  onChange={handleChange}
                  label="Role"
                >
                  <MenuItem value="Nominator">Nominator</MenuItem>
                  <MenuItem value="Recommender">Recommender</MenuItem>
                  <MenuItem value="Review Committee">Review Committee</MenuItem>
                </Select>
              </FormControl>
            </>
          )}
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
            {formData.isLogin ? 'Login' : 'Register'}
          </Button>
          <Button variant="text" onClick={toggleForm} fullWidth sx={{ mt: 1 }}>
            {formData.isLogin ? 'Switch to Register' : 'Switch to Login'}
          </Button>
        </form>
      </Paper>
    </Container>
  );
}

export default RegistrationForm;
