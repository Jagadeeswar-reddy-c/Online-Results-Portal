<?php
// Change these credentials to match your MySQL server
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "STUDENT_MARKS_MANAGEMENT";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Create database
$sql = "CREATE DATABASE IF NOT EXISTS $dbname";
if ($conn->query($sql) === TRUE) {
    echo "Database created successfully<br>";
} else {
    echo "Error creating database: " . $conn->error;
}

// Connect to the created database
$conn = new mysqli($servername, $username, $password, $dbname);

// SQL query to create tables
$sql = "CREATE TABLE IF NOT EXISTS BRANCH_ID_DETAILS (
    BRANCH_ID INT PRIMARY KEY NOT NULL,
    BRANCH_NAME VARCHAR(35)
)";

// Execute table creation query
if ($conn->query($sql) === TRUE) {
    echo "Table 'BRANCH_ID_DETAILS' created successfully<br>";
} else {
    echo "Error creating table 'BRANCH_ID_DETAILS': " . $conn->error;
}

$sql = "CREATE TABLE IF NOT EXISTS STUDENT_DETAILS (
    STUDENT_ID VARCHAR(10) PRIMARY KEY NOT NULL,
    STUDENT_NAME VARCHAR(40),
    STUDENT_GENDER VARCHAR(2),
    STUDENT_DOB VARCHAR(8),
    STUDENT_PH VARCHAR(10),
    BRANCH_ID INT,
    STUDENT_BATCH INT,
    FOREIGN KEY (BRANCH_ID) REFERENCES BRANCH_ID_DETAILS(BRANCH_ID)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'STUDENT_DETAILS' created successfully<br>";
} else {
    echo "Error creating table 'STUDENT_DETAILS': " . $conn->error;
}

$sql = "CREATE TABLE IF NOT EXISTS SUBJECT_TABLE (
    SUBJECT_NO INT AUTO_INCREMENT PRIMARY KEY,
	SUBJECT_CODE VARCHAR(10) NOT NULL,
    SUBJECT_NAME VARCHAR(50),
    SUBJECT_CREDITS FLOAT(10,2)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'SUBJECT_TABLE' created successfully<br>";
} else {
    echo "Error creating table 'STUDENT_MARKS': " . $conn->error;
}

$sql = "CREATE TABLE IF NOT EXISTS STUDENT_MARKS (
    STUDENT_ID VARCHAR(10),
    SUBJECT_NO INT,
    INTERNAL_MARKS VARCHAR(3),
    EXTERNAL_MARKS VARCHAR(3),
    SEM_ID INT,
    FOREIGN KEY (STUDENT_ID) REFERENCES STUDENT_DETAILS(STUDENT_ID),
    FOREIGN KEY (SUBJECT_NO) REFERENCES SUBJECT_TABLE(SUBJECT_NO)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'STUDENT_MARKS' created successfully<br>";
} else {
    echo "Error creating table 'STUDENT_MARKS': " . $conn->error;
}

$sql = "CREATE TABLE IF NOT EXISTS ADMINS (
    username VARCHAR(50) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'ADMINS' created successfully<br>";
} else {
    echo "Error creating table 'ADMINS': " . $conn->error;
}

$sql = "INSERT INTO ADMINS (username,password) values ('ADMIN','root')";
if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}


$sql = "CREATE TABLE IF NOT EXISTS USERID (
    STUDENT_ID VARCHAR(10) PRIMARY KEY NOT NULL,
    PASSWORD VARCHAR(255) NOT NULL
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'USERID' created successfully<br>";
} else {
    echo "Error creating table 'ADMINS': " . $conn->error;
}

// Close connection
$conn->close();
?>
