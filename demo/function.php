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

$sql = "CREATE TABLE IF NOT EXISTS ROLE_USER (
    USER_NUM INT PRIMARY KEY,
    USER_ROLE VARCHAR(15)
)";

// Execute table creation query
if ($conn->query($sql) === TRUE) {
    echo "Table 'ROLE_USER' created successfully<br>";
} else {
    echo "Error creating table 'ROLE_USER': " . $conn->error;
}

$sql = "INSERT INTO ROLE_USER (USER_NUM,USER_ROLE) VALUES (1,'STUDENT'),(2,'FACULTY'),(3,'FACULTY_ADMIN')";

if ($conn->query($sql) === TRUE) {
    echo "Table 'ROLE_USER' data is created successfully<br>";
} else {
    echo "Error creating table 'ROLE_USER': " . $conn->error;
}


$sql = "CREATE TABLE IF NOT EXISTS USER_DETAILS (
    USER_ID VARCHAR(10) PRIMARY KEY NOT NULL,
    USER_NAME VARCHAR(40),
    USER_GENDER VARCHAR(2),
    USER_DOB VARCHAR(8),
    USER_PH VARCHAR(10),
    BRANCH_ID INT,
    USER_BATCH INT,
    USER_NUM INT,
    FOREIGN KEY (USER_NUM) REFERENCES ROLE_USER(USER_NUM),
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
    USER_ID VARCHAR(10),
    SUBJECT_NO INT,
    INTERNAL_MARKS VARCHAR(3),
    EXTERNAL_MARKS VARCHAR(3),
    SEM_ID INT,
    FOREIGN KEY (USER_ID) REFERENCES USER_DETAILS(USER_ID),
    FOREIGN KEY (SUBJECT_NO) REFERENCES SUBJECT_TABLE(SUBJECT_NO)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'STUDENT_MARKS' created successfully<br>";
} else {
    echo "Error creating table 'STUDENT_MARKS': " . $conn->error;
}

$sql = "CREATE TABLE IF NOT EXISTS USERID (
    USER_ID VARCHAR(10) PRIMARY KEY,
    PASSWORD VARCHAR(255) NOT NULL,
    FOREIGN KEY (USER_ID) REFERENCES USER_DETAILS(USER_ID)
)";

if ($conn->query($sql) === TRUE) {
    echo "Table 'USERID' created successfully<br>";
} else {
    echo "Error creating table 'ADMINS': " . $conn->error;
}

$sql = "INSERT INTO BRANCH_ID_DETAILS (BRANCH_ID, BRANCH_NAME) VALUES (1, 'CIVIL')";

if($conn->query($sql)===TRUE){
    echo "Table 'BATCHID' Data inserted successfully<br>";
}else{
    echo  "Error inserting data into 'ADMINS' table: " . $conn->error;
}

$sql = "INSERT INTO USER_DETAILS (USER_ID, USER_NAME, USER_GENDER, USER_DOB, USER_PH, BRANCH_ID, USER_BATCH, USER_NUM) 
        VALUES ('ce', 'ce', 'M', '00000000', '', 1, 2020, 3),
               ('ace1', 'ace1', 'M', '00000000', '', 1, 2020, 3),
               ('ace2', 'ace2', 'M', '00000000', '', 1, 2020, 3),
               ('ace3', 'ace3', 'M', '00000000', '', 1, 2020, 3),
               ('staff', 'staff', 'M', '00000000', '', 1, 2020, 2)";


if($conn->query($sql)===TRUE){
    echo "Table 'ADMINS and STAFF' Data inserted successfully<br>";
}else{
    echo  "Error inserting data into 'ADMINS' table: " . $conn->error;
}

$sql = "INSERT INTO USERID (USER_ID, PASSWORD) VALUES ('ce', 'ksrm@1234'),('ace1', 'ksrm@1234'),('ace2', 'ksrm@1234'),('ace3', 'ksrm@1234'),('staff', 'ksrm@1234')";

if($conn->query($sql)===TRUE){
    echo "Table 'ADMINS and STAFF' ID inserted successfully<br>";
}else{
    echo  "Error inserting data into 'ADMINS' table: " . $conn->error;
}

// $sql = "INSERT INTO USER_DETAILS (USER_ID,USER_NAME,USER_GENDER,USER_DOB,USER_PH,BRANCH_ID,USER_BATCH,USER_NUM) VALUES ('FACULTY','FACULTY','M','00000000','',0,2020,2)";

// if($conn->query($sql)===TRUE){
//     echo "Table 'FACULTY' Data inserted successfully<br>";
// }else{
//     echo  "Error inserting data into 'ADMINS' table: " . $conn->error;
// }

// $sql = "INSERT INTO USERID (USER_ID, PASSWORD) VALUES ('FACULTY', '00000000')";

// if($conn->query($sql)===TRUE){
//     echo "Table 'FACULTY' ID inserted successfully<br>";
// }else{
//     echo  "Error inserting data into 'ADMINS' table: " . $conn->error;
// }

// Close connection
$conn->close();
?>
