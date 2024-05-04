import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { TextField, Button, Typography, Container } from '@mui/material';

function EditEducationForm() {
    const { eduId } = useParams(); // Assuming you're using React Router v6
    const navigate = useNavigate();
    const [educationData, setEducationData] = useState({
        college_name: '',
        location: '',
        degree: '',
        program: '',
        graduation_year: ''
    });

    useEffect(() => {
        // Fetch the current education data to populate the form (Assuming an endpoint to fetch this data exists)
        axios.get(`http://127.0.0.1:5000/nominee/education/${eduId}/info`)
            .then(response => {
                setEducationData(response.data);
            })
            .catch(error => console.error('Failed to fetch education data:', error));
    }, [eduId]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setEducationData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`http://127.0.0.1:5000/nominee/education/${eduId}/update`, educationData)
            .then(response => {
                console.log('Education updated:', response.data);
                navigate('/nominee/dashboard');  // Redirect to a dashboard or another appropriate page
            })
            .catch(error => {
                console.error('Failed to update education:', error.response ? error.response.data : "No response");
            });
    };

    return (
        <Container maxWidth="sm">
            <Typography variant="h6" gutterBottom>Edit Education Details</Typography>
            <form onSubmit={handleSubmit}>
                <TextField
                    fullWidth
                    label="College Name"
                    name="college_name"
                    value={educationData.college_name}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    label="Location"
                    name="location"
                    value={educationData.location}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    label="Degree"
                    name="degree"
                    value={educationData.degree}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    label="Program"
                    name="program"
                    value={educationData.program}
                    onChange={handleChange}
                    margin="normal"
                />
                <TextField
                    fullWidth
                    type="date"
                    label="Graduation Year"
                    name="graduation_year"
                    value={educationData.graduation_year}
                    onChange={handleChange}
                    margin="normal"
                    InputLabelProps={{
                        shrink: true,
                    }}
                />
                <Button type="submit" variant="contained" color="primary">Update Education</Button>
            </form>
        </Container>
    );
}

export default EditEducationForm;
