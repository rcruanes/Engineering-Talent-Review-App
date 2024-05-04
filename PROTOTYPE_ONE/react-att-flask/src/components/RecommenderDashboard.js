import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
  Container,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  AppBar,
  Toolbar,
  Typography,
  Dialog
} from '@mui/material';
import ViewNominee from './ViewNominee';  // Ensure this is correctly imported

function RecommenderDashboard() {
    const [nominees, setNominees] = useState([]);
    const [currentUser, setCurrentUser] = useState({});
    const [viewNomineeId, setViewNomineeId] = useState(null);  // State to control dialog visibility
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            const authToken = localStorage.getItem('authToken');
            if (!authToken) {
                console.error('No authentication token found');
                navigate('/');
                return;
            }

            try {
                const userRes = await axios.get('http://localhost:5000/recommender/dashboard', {
                    headers: { Authorization: `Bearer ${authToken}` }
                });
                setCurrentUser(userRes.data);
        
                const nomineesRes = await axios.get('http://localhost:5000/nominees/nominator', {
                    headers: { Authorization: `Bearer ${authToken}` }
                });
                setNominees(nomineesRes.data);
            } catch (error) {
                console.error('Error fetching data:', error);
                if (error.response && error.response.status === 401) {
                    navigate('/');
                }
            }
        };

        fetchData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('authToken');
        navigate('/');
    };

    const handleViewClose = () => {
        setViewNomineeId(null);  // This function will close the dialog
    };

    const handleViewOpen = (id) => {
        setViewNomineeId(id);  // This function will open the dialog with the specific nominee ID
    };

    return (
        <Container maxWidth="lg">
            <AppBar position="static">
                <Toolbar>
                    <Button color="inherit" onClick={() => navigate('/dashboard')} sx={{ marginRight: 2 }}>Dashboard</Button>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Welcome Recommender: {currentUser.full_name || 'User'}
                    </Typography>
                    <Button color="inherit" onClick={handleLogout}>Logout</Button>
                </Toolbar>
            </AppBar>
            <TableContainer component={Paper} sx={{ marginTop: 3 }}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Nominee Name</TableCell>
                            <TableCell>Nominator</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {nominees.map((nominee) => (
                            <TableRow key={nominee.id}>
                                <TableCell>{nominee.first_name} {nominee.last_name}</TableCell>
                                <TableCell>{nominee.nominator.first_name} {nominee.nominator.last_name}</TableCell>
                                <TableCell>
                                    <Button variant="contained" color="primary" onClick={() => handleViewOpen(nominee.id)}>View</Button>
                                    <Button variant="contained" color="secondary" onClick={() => navigate(`/recommend/new/`)} sx={{ ml: 1 }}>+ Recommend</Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            {viewNomineeId && (
                <Dialog open={Boolean(viewNomineeId)} onClose={handleViewClose} maxWidth="md" fullWidth>
                    <ViewNominee id={viewNomineeId} onClose={handleViewClose} />
                </Dialog>
            )}
        </Container>
    );
}

export default RecommenderDashboard;
