import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { DialogContent, DialogTitle, Dialog, Button, Typography, Container, Grid } from '@mui/material';

function ViewNominee({ id, onClose }) {
    const [nominee, setNominee] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/nominee/${id}/info`)
            .then(response => {
                setNominee(response.data);
            })
            .catch(error => {
                console.error('Error fetching nominee details:', error);
                navigate('/'); // Redirect if the fetch fails
            });
    }, [id, navigate]);

    if (!nominee) {
        return <DialogContent><Typography>Loading...</Typography></DialogContent>;
    }

    return (
        <Dialog open onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>Nominee Details</DialogTitle>
            <DialogContent dividers>
                <Container>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <Typography variant="subtitle1"><strong>First Name:</strong> {nominee.first_name}</Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <Typography variant="subtitle1"><strong>Last Name:</strong> {nominee.last_name}</Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <Typography variant="subtitle1"><strong>Department:</strong> {nominee.department_name}</Typography>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <Typography variant="subtitle1"><strong>Job Category:</strong> {nominee.job_category}</Typography>
                        </Grid>
                        <Grid item xs={12}>
                            <Typography variant="subtitle1"><strong>Email:</strong> {nominee.email}</Typography>
                        </Grid>
                        <Grid item xs={12}>
                            <Typography variant="subtitle1"><strong>Nominator Qualification:</strong> {nominee.nominator_qualification}</Typography>
                        </Grid>
                        {/* Education History */}
                        <Grid item xs={12}>
                            <Typography variant="h6">Educational History:</Typography>
                            {nominee.educations && nominee.educations.map((education, index) => (
                                <Typography key={index} variant="subtitle1">
                                    <strong>{education.degree} in {education.program}</strong> from {education.college_name}, {education.location} ({education.graduation_year})
                                </Typography>
                            ))}
                        </Grid>
                    </Grid>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={onClose}
                        style={{ marginTop: '20px' }}
                    >
                        Close
                    </Button>
                </Container>
            </DialogContent>
        </Dialog>
    );
}

export default ViewNominee;
