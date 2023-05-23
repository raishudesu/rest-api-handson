# Flask MySQL API

This is a simple Flask API project that utilizes MySQL database to perform CRUD operations. It provides endpoints to interact with a MySQL database table.

## Dependencies

Make sure you have the following dependencies installed:

- Flask
- Flask-MySQL
- Flask-Cors

## Major Files

The major files in this project are:

- `config.py`: Contains the configuration settings for the MySQL database.
- `app.py`: Initializes the Flask application and sets up the routes and database connection.
- `main.py`: The main entry point for running the application.

## Instructions

Follow the steps below to set up and run the application:

### Step 1: Create MySQL Database Table

Create your own MySQL database table to perform operations. You can use any MySQL client or command-line tool to create the table structure.

### Step 2: Install Dependencies

Install the required dependencies by running the following commands:

- `pip install flask`
- `pip install -U flask-cors`
- `pip install flask-mysql`


### Step 3: Modify Python Scripts

Modify the Python scripts to match your database configuration. In particular, update the following details in `config.py`:

- `HOST`: Set it to the hostname of your MySQL database.
- `USER`: Set it to the username for accessing your MySQL database.
- `PASSWORD`: Set it to the password for the specified user.
- `DATABASE`: Set it to the name of your MySQL database.
- `TABLE`: Set it to the name of the table you created in Step 1.

### Step 4: Run the Application

To run the application, use the following terminal command:

`python main.py`


Once the application is running, you can perform CRUD operations using Postman or any other HTTP client. Follow these steps:

1. Copy the API link printed in the terminal.
2. Open Postman or any other HTTP client.
3. Paste the API link in the URL field.
4. Perform CRUD operations by sending HTTP requests to the appropriate endpoints.

That's it! You can now use the Flask MySQL API to interact with your MySQL database.
