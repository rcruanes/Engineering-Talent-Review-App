import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  Divider,
  Button,
  Dialog
} from '@mui/material';
import ViewNominee from './ViewNominee';  // Ensure this component is correctly imported

function NomineeDetails() {
    const { nomineeId } = useParams();
    const navigate = useNavigate();
    const [details, setDetails] = useState([]);
    const [nomineeName, setNomineeName] = useState('');
    const [openDialog, setOpenDialog] = useState(false);

    useEffect(() => {
        axios.get(`http://127.0.0.1:5000/review/nominee/${nomineeId}/details`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('authToken')}` }
        })
        .then(response => {
            if (response.data.length > 0) {
                setNomineeName(response.data[0].nominee_name);  // Assuming the first entry is the nominee's name
                setDetails(response.data.slice(1));  // The rest are the details
            }
        })
        .catch(error => {
            console.error('Error fetching nominee details:', error);
            navigate('/dashboard'); // Redirect or handle error
        });
    }, [nomineeId, navigate]);

    const handleDialogOpen = () => {
        setOpenDialog(true);
    };

    const handleDialogClose = () => {
        setOpenDialog(false);
    };

    const handleBack = () => {
        navigate(-1); // Navigate back to the previous page
    };

    return (
        <Paper style={{ padding: 20 }}>
            <Button variant="outlined" onClick={handleBack} style={{ marginBottom: 20 }}>
                Go Back
            </Button>
            <Typography variant="h5" gutterBottom>
                Details for Nominee: <Button onClick={handleDialogOpen} style={{
                    textDecoration: 'underline',
                    color: 'blue',
                    cursor: 'pointer'
                }}>
                    {nomineeName}
                </Button>
            </Typography>
            <List>
                {details.map((detail, index) => (
                    <React.Fragment key={index}>
                        <ListItem alignItems="flex-start">
                            <ListItemText
                                primary={`Recommender's Feedback by ${detail.first_name || 'Unknown'} ${detail.last_name || 'Recommender'}:`}
                                secondary={
                                    <>
                                        <Typography component="span" variant="body2" color="textPrimary" display="block">
                                            "Personally, became aware of the importance of his/her extraordinary accomplishments and their impact on the company:"
                                            <br />{detail.ic_q1}
                                        </Typography>
                                        <Typography component="span" variant="body2" color="textPrimary" display="block">
                                            "List technical patents; technical reports and presentations; development of products, applications and systems; and application of facilities and services:"
                                            <br />{detail.ic_q2}
                                        </Typography>
                                        <Typography component="span" variant="body2" color="textPrimary" display="block">
                                            "Comparing with people in this position:"
                                            <br />{detail.ic_q3}
                                        </Typography>
                                        <Typography component="span" variant="body2" color="textPrimary" display="block">
                                            "What’s the expansion of job responsibility:"
                                            <br />{detail.ic_q4}
                                        </Typography>
                                        <Typography component="span" variant="body2" color="textPrimary" display="block">
                                            "What is the future development area, what’s manager’s plan for the career development:"
                                            <br />{detail.ic_q5}
                                        </Typography>
                                    </>
                                }
                            />
                        </ListItem>
                        {index < details.length - 1 && <Divider variant="inset" component="li" />}
                    </React.Fragment>
                ))}
            </List>
            <Dialog open={openDialog} onClose={handleDialogClose} fullWidth maxWidth="sm">
                <ViewNominee id={nomineeId} onClose={handleDialogClose} />
            </Dialog>
        </Paper>
    );
}

export default NomineeDetails;
