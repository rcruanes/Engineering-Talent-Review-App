import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
    Button,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Container,
    Typography,
    Paper,
    AppBar,
    Toolbar,
    Dialog
} from '@mui/material';
import ViewNominee from './ViewNominee';

const NominatorDashboard = () => {
    const [nominees, setNominees] = useState([]);
    const [viewNomineeId, setViewNomineeId] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/nominee/dashboard')
          .then(response => {
            setNominees(response.data.all_nominees_nominator || []);
          })
          .catch(error => {
            console.error('Error fetching nominees:', error);
          });
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('userToken');
        navigate('/');
    };

    const goToDashboard = () => {
        navigate('/dashboard');
    };

    const handleViewClose = () => {
        setViewNomineeId(null);  // This function will close the dialog
    };

    const handleViewOpen = (id) => {
        setViewNomineeId(id);  // This function will open the dialog with the specific nominee ID
    };

    const confirmDelete = (id) => {
        const token = localStorage.getItem('authToken');
        if (window.confirm("Are you sure you want to delete this nominee?")) {
            axios.delete(`http://127.0.0.1:5000/nominee/${id}/delete`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
            .then(response => {
                console.log("Nominee deleted successfully", response);
                setNominees(nominees.filter(nominee => nominee.id !== id));
            })
            .catch(error => {
                console.error("Error deleting nominee:", error);
            });
        }
    };

    return (
      <Container maxWidth="lg">
        <AppBar position="static">
            <Toolbar>
                <Button color="inherit" onClick={goToDashboard}>Back to Dashboard</Button>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    Nominator Dashboard
                </Typography>
                <Button color="inherit" onClick={handleLogout}>Logout</Button>
            </Toolbar>
        </AppBar>
        <TableContainer component={Paper} sx={{ marginTop: 3 }}>
            <Table aria-label="nominee table">
                <TableHead>
                    <TableRow>
                        <TableCell>Nominee Name</TableCell>
                        <TableCell>Nominator</TableCell>
                        <TableCell>Actions</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {nominees.map(nominee => (
                        <TableRow key={nominee.id}>
                            <TableCell>{nominee.first_name} {nominee.last_name}</TableCell>
                            <TableCell>{nominee.nominator ? `${nominee.nominator.first_name} ${nominee.nominator.last_name}` : 'No Nominator'}</TableCell>
                            <TableCell>
                                <Button onClick={() => handleViewOpen(nominee.id)}>View</Button>
                                <Button component={RouterLink} to={`/nominee/${nominee.id}/edit`} color="primary">Edit</Button>
                                <Button color="error" onClick={() => confirmDelete(nominee.id)}>Delete</Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
        {viewNomineeId && (
            <Dialog open={Boolean(viewNomineeId)} onClose={handleViewClose}>
                <ViewNominee id={viewNomineeId} onClose={handleViewClose} />
            </Dialog>
        )}
        <Button variant="contained" color="primary" component={RouterLink} to="/nominee/new" sx={{ mt: 2 }}>
            Submit New Nominee
        </Button>
      </Container>
    );
};

export default NominatorDashboard;
