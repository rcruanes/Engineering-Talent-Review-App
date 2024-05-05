import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Typography, Button } from '@mui/material';

function ReviewCommitteeDashboard() {
    const [nominees, setNominees] = useState([]);
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const { data } = await axios.get('http://127.0.0.1:5000/review/dashboard', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('authToken')}` }
                });
                // Set data directly from the fetch to ensure structure consistency
                setNominees(data.all_nominees_nominator || []);  // Change to all_nominees_nominator if that's the correct data array with nominator info
                setUsers(data.all_users || []);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
        };

        fetchData();
    }, []);

    const handleBack = () => {
        navigate('/dashboard'); // Navigate back to the main dashboard
    };

    return (
        <div style={{ padding: '20px' }}>
            <Typography variant="h4" gutterBottom>Review Committee Dashboard</Typography>
            <Button variant="contained" color="primary" onClick={handleBack} style={{ marginBottom: '20px' }}>
                Back to Main Dashboard
            </Button>
            <TableContainer component={Paper}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Nominee Name</TableCell>
                            <TableCell>Nominator</TableCell>
                            <TableCell>Department</TableCell>
                            <TableCell>Job Category</TableCell>
                            <TableCell>Details</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {nominees.map((nominee) => (
                            <TableRow key={nominee.id}>
                                <TableCell>{nominee.first_name} {nominee.last_name}</TableCell>
                                <TableCell>{nominee.nominator ? `${nominee.nominator.first_name} ${nominee.nominator.last_name}` : 'N/A'}</TableCell>
                                <TableCell>{nominee.department_name}</TableCell>
                                <TableCell>{nominee.job_category}</TableCell>
                                <TableCell>
                                    <Button component={RouterLink} to={`/review/nominee/${nominee.id}/details`}>
                                        View Details
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
                Users List
            </Typography>
            <TableContainer component={Paper}>
                <Table aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>User Name</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>Role</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {users.map((user) => (
                            <TableRow key={user.id}>
                                <TableCell>{user.first_name} {user.last_name}</TableCell>
                                <TableCell>{user.email}</TableCell>
                                <TableCell>{user.role}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
}

export default ReviewCommitteeDashboard;
