const express = require('express');
const mysql = require('mysql2');

const app = express();
const port = 3000;

// Create MySQL connection
var connection = mysql.createConnection({
  host: 'mysql-service', // Updated to match the service name in docker-compose.yml
  user: 'root',
  password: 'password', // Updated to match the password in docker-compose.yml
  database: 'mysql_db', // Updated to match the database name in docker-compose.yml
  port: 3306
});

// Connect to MySQL
connection.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err.stack);
    return;
  }
  console.log('Connected to MySQL as id ' + connection.threadId);
});

// Define route
app.get('/', (req, res) => {
  connection.query('SELECT * FROM products', (error, results) => {
    if (error) {
      return res.status(500).send('Error querying the database');
    }

    if (results.length > 0) {
      const productNames = results.map(product => product.name).join(', ');
      res.send(`node-service:<br>Products: ${productNames}`);
    } else {
      res.send('No products found in the database.');
    }
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});

// Optionally, end the connection when the app is stopped
process.on('SIGINT', () => {
  connection.end((err) => {
    if (err) {
      console.error('Error closing MySQL connection:', err.stack);
    } else {
      console.log('MySQL connection closed.');
    }
    process.exit();
  });
});
