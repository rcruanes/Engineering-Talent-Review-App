const express = require('express');
const mysql = require('mysql');

const app = express();
const PORT = process.env.PORT || 3001;

// Create MySQL connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'your_mysql_username',
  password: 'your_mysql_password',
  database: 'your_database_name'
});

// Connect to MySQL
db.connect((err) => {
  if (err) {
    throw err;
  }
  console.log('Connected to MySQL database');
});

// Create a route to handle talent review submissions
app.post('/submit-review', (req, res) => {
  // Extract talent review data from request body
  const { name, department, skills, comments } = req.body;

  // Insert data into MySQL database
  const sql = 'INSERT INTO talent_reviews (name, department, skills, comments) VALUES (?, ?, ?, ?)';
  db.query(sql, [name, department, skills, comments], (err, result) => {
    if (err) {
      console.error('Error inserting talent review:', err);
      res.status(500).send('Error submitting talent review');
    } else {
      console.log('Talent review submitted successfully');
      res.status(200).send('Talent review submitted successfully');
    }
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
