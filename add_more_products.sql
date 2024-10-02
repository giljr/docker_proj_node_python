-- Use the existing database
USE mysql_db;

-- Insert data into the products table
INSERT INTO products (name) VALUES 
    ('Sony WH-1000XM4'),
    ('Oculus Quest 2'),
    ('Dyson V11');

-- Show updated content of the products table
SELECT * FROM products;
