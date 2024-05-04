import React, { useState } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';
import { Button, TextField, Typography, Container, Box } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom'; // Import useNavigate

const NewNomineeForm = () => {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    department_name: '',
    job_category: '',
    email: '',
    nominator_qualification: ''
  });

  const { authToken, userId } = useAuth();
  const navigate = useNavigate(); // Hook for navigation

  const handleChange = e => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = e => {
    e.preventDefault();
    const fullData = {
        ...formData,
        user_id: userId
    };
    axios.post('http://127.0.0.1:5000/nominee/create', fullData, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        }
    })
    .then(response => {
      console.log('Response data:', response.data);  // Debug: Log the entire response data
      if(response.data && response.data.id) {
          navigate(`/nominee/${response.data.id}/education`);
      } else {
          throw new Error('ID not found in response');
      }
  })
    .catch(error => {
        console.error('Error creating nominee:', error.response ? error.response.data : "No response");
    });
  };

  return (
    <Container>
      <Typography variant="h6" gutterBottom>New Nominee Form Information</Typography>
      <form onSubmit={handleSubmit}>
        <TextField fullWidth label="Nominee First Name" name="first_name" value={formData.first_name} onChange={handleChange} variant="outlined" margin="normal" />
        <TextField fullWidth label="Nominee Last Name" name="last_name" value={formData.last_name} onChange={handleChange} variant="outlined" margin="normal" />
        <TextField fullWidth label="Department Name" name="department_name" value={formData.department_name} onChange={handleChange} variant="outlined" margin="normal" />
        <TextField fullWidth label="Job Category" name="job_category" value={formData.job_category} onChange={handleChange} variant="outlined" margin="normal" />
        <TextField fullWidth label="Email" name="email" type="email" value={formData.email} onChange={handleChange} variant="outlined" margin="normal" />
        <TextField fullWidth label="Nominator Qualification" name="nominator_qualification" value={formData.nominator_qualification} onChange={handleChange} variant="outlined" margin="normal" multiline rows={4} />
        <Box display="flex" justifyContent="space-between" mt={2}>
          <Button type="submit" variant="contained" color="primary">Continue</Button>
          <Button variant="contained" color="primary" component={Link} to="/nominee/dashboard">
            Back to Dashboard
          </Button>
        </Box>
      </form>
    </Container>
  );
};

export default NewNomineeForm;
