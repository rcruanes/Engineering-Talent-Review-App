import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {
  TextField,
  Button,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Typography,
  Container,
  Card,
  CardContent,
  Grid,
  Box
} from '@mui/material';

function RecommendNewNominee() {
    const [nominees, setNominees] = useState([]);
    const [selectedNominee, setSelectedNominee] = useState('');
    const [workContributions, setWorkContributions] = useState({
        individual_contributor: false,
        project_manager: false,
        people_manager: false
    });
    const [answers, setAnswers] = useState({
        ic_q1: '',
        ic_q2: '',
        ic_q3: '',
        ic_q4: '',
        ic_q5: '',
    });
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/nominee/dashboard')
            .then(response => {
                setNominees(response.data.all_nominees_nominator || []);
            })
            .catch(error => console.error('Error fetching nominees:', error));
    }, []);

    const handleInputChange = (e) => {
        setAnswers({
            ...answers,
            [e.target.name]: e.target.value
        });
    };

    const handleCheckboxChange = (e) => {
        setWorkContributions({
            ...workContributions,
            [e.target.name]: e.target.checked
        });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const token = localStorage.getItem('authToken');
        const dataToSend = {
            nominee_id: selectedNominee,
            work_contributions: Object.keys(workContributions).filter(k => workContributions[k]),
            answers
        };

        axios.post('http://127.0.0.1:5000/recommendation/create', dataToSend, {
            headers: { 
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'  
            }
        })
        .then(response => {
            console.log('Recommendation submitted:', response.data);
            navigate('/recommender/dashboard');
        })
        .catch(error => {
            console.error('Error submitting recommendation:', error);
        });
    };

    return (
        <Container maxWidth="md">
            <Card raised>
                <CardContent>
                    <Typography variant="h4" gutterBottom>Recommend New Nominee</Typography>
                    <form onSubmit={handleSubmit}>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <FormControl fullWidth>
                                    <InputLabel id="nominee-label">Select Nominee</InputLabel>
                                    <Select
                                        labelId="nominee-label"
                                        id="all_nominees"
                                        value={selectedNominee}
                                        label="Select Nominee"
                                        onChange={e => setSelectedNominee(e.target.value)}
                                    >
                                        {nominees.map(nominee => (
                                            <MenuItem key={nominee.id} value={nominee.id}>{nominee.first_name} {nominee.last_name}</MenuItem>
                                        ))}
                                    </Select>
                                </FormControl>
                            </Grid>
                            <Grid item xs={12}>
                                <FormGroup>
                                    <FormControlLabel control={<Checkbox checked={workContributions.individual_contributor} onChange={handleCheckboxChange} name="individual_contributor" />} label="Individual Contributor" />
                                    <FormControlLabel control={<Checkbox checked={workContributions.project_manager} onChange={handleCheckboxChange} name="project_manager" />} label="Project Manager" />
                                    <FormControlLabel control={<Checkbox checked={workContributions.people_manager} onChange={handleCheckboxChange} name="people_manager" />} label="People Manager" />
                                </FormGroup>
                            </Grid>
                            {Object.values(workContributions).some(value => value) && (
                                <Grid item xs={12}>
                                    {[
                                        { key: 'ic_q1', question: 'Personally, became aware of the importance of his/her extraordinary accomplishments and their impact on the company.' },
                                        { key: 'ic_q2', question: 'List technical patents; technical reports and presentations; development of products, applications and systems; and application of facilities and services.' },
                                        { key: 'ic_q3', question: 'Comparing with people in this position.' },
                                        { key: 'ic_q4', question: 'What’s the expansion of job responsibility.' },
                                        { key: 'ic_q5', question: 'What is the future development area, what’s manager’s plan for the career development.' }
                                    ].map(field => (
                                        <Box key={field.key}>
                                            <Typography gutterBottom>{field.question}</Typography>
                                            <TextField fullWidth variant="outlined" name={field.key} value={answers[field.key]} onChange={handleInputChange} margin="normal" />
                                        </Box>
                                    ))}
                                </Grid>
                            )}
                            <Grid item xs={12}>
                                <Button type="submit" variant="contained" color="primary">Submit New Nominee</Button>
                                <Button variant="contained" onClick={() => navigate('/recommender/dashboard')} sx={{ ml: 2 }}>Back</Button>
                            </Grid>
                        </Grid>
                    </form>
                </CardContent>
            </Card>
        </Container>
    );
}

export default RecommendNewNominee;
