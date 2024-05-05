import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Typography, Container, Card, CardActionArea, Grid, CardContent, Paper, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom'; // To use with MUI Link
import { useAuth } from './AuthContext';

const Dashboard = () => {
  const [userName, setUserName] = useState('');
  const navigate = useNavigate();
  const { authToken, logout } = useAuth(); // Now using the useAuth hook

  useEffect(() => {
    if (!authToken) {
      navigate('/'); // Redirect to login if there is no authToken
    } else {
      fetch('http://127.0.0.1:5000/user/profile', {
        headers: {
          'Authorization': `Bearer ${authToken}`
        }
      })
      .then(response => response.json())
      .then(data => {
        if(data.first_name) {
          setUserName(data.first_name);
        } else {
          throw new Error('User not found');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        navigate('/'); // Redirect to login if the user data cannot be fetched
      });
    }
  }, [authToken, navigate]);

  const handleLogout = () => {
    logout();  // Now using logout from useAuth
    navigate('/');  // Redirect to the login page
  };

  return (
    <Container component="main" maxWidth="sm" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      <Paper elevation={3} style={{ padding: 20, flexGrow: 0, minWidth: 400 }}> {/* Adjusted width of the Paper component */}
        <Typography variant="h4" component="h1" align="center" gutterBottom>Welcome to the Dashboard</Typography>
        <Grid container spacing={2} justifyContent="center">
          <Grid item xs={12} sm={6} md={4}>
            <Card style={{ width: '100%' }}>
              <CardActionArea component={RouterLink} to="/nominee/dashboard">
                <CardContent>
                  <Typography variant="h6" align="center">Nominator Dashboard</Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card style={{ width: '100%' }}>
              <CardActionArea component={RouterLink} to="/recommender/dashboard">
                <CardContent>
                  <Typography variant="h6" align="center">Recommender Dashboard</Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Card style={{ width: '100%' }}>
              <CardActionArea component={RouterLink} to="/review/dashboard">
                <CardContent>
                  <Typography variant="h6" align="center">Review Committee Dashboard</Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        </Grid>
        <Box mt={2} display="flex" justifyContent="center">
          <Button variant="contained" color="error" onClick={handleLogout}>Logout</Button>
        </Box>
      </Paper>
    </Container>
  );
};

export default Dashboard;
