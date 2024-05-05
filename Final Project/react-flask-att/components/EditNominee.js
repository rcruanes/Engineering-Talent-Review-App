import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { TextField, Button, Typography, Paper, Container, Grid } from '@mui/material';

function EditNominee() {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        department_name: '',
        job_category: '',
        email: '',
        nominator_qualification: ''
    });
    const { id } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/nominee/${id}/info`)
            .then(response => {
                setFormData(response.data);
            })
            .catch(error => {
                console.error('Error fetching nominee details:', error);
            });
    }, [id]);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        const authToken = localStorage.getItem('authToken');

        axios.put(`http://127.0.0.1:5000/nominee/${id}/update`, formData, {
            headers: {
                'Authorization': `Bearer ${authToken}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            alert('Nominee updated successfully');
            navigate('/nominee/dashboard');
        })
        .catch(error => {
            console.error('Failed to update nominee:', error);
            alert('Failed to update nominee: ' + (error.response && error.response.data.error ? error.response.data.error : 'Unknown error'));
        });
    };

    return (
        <Container component={Paper} style={{ padding: '20px', marginTop: '20px' }}>
            <Typography variant="h4" gutterBottom>Edit Nominee</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    fullWidth
                    margin="normal"
                    label="First Name"
                    name="first_name"
                    value={formData.first_name}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Last Name"
                    name="last_name"
                    value={formData.last_name}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Department Name"
                    name="department_name"
                    value={formData.department_name}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Job Category"
                    name="job_category"
                    value={formData.job_category}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Email"
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Nominator Qualification"
                    name="nominator_qualification"
                    value={formData.nominator_qualification}
                    onChange={handleChange}
                    multiline
                    rows={4}
                />
                <Grid container spacing={2} justifyContent="space-between" alignItems="center" style={{ marginTop: 20 }}>
                    <Grid item>
                        <Button type="submit" variant="contained" color="primary">Update Nominee</Button>
                    </Grid>
                    <Grid item>
                        <Button variant="contained" onClick={() => navigate('/nominee/dashboard')}>Back to Dashboard</Button>
                    </Grid>
                    <Grid item>
                    <Button variant="contained" onClick={() => navigate(`/nominee/${id}/education`)} color="secondary">Edit Education</Button>
                    </Grid>
                </Grid>
            </form>
        </Container>
    );
}

export default EditNominee;
