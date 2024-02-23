<?php
// Database configuration
$servername = "localhost";
$username = "root";
$password = "";
$database = "STUDENT_MARKS_MANAGEMENT";


// Create a connection
$connection = mysqli_connect($servername, $username, $password, $database);

// Check the connection
if (!$connection) {
    die("Connection failed: " . mysqli_connect_error());
}
?>
