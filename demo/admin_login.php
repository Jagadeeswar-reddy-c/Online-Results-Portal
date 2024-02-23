<?php
// Start the session
session_start();

// Establish connection to MySQL database
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "STUDENT_MARKS_MANAGEMENT";

$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve input values from login form
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    if(strlen($username) > 8) {
        $sql = "SELECT * FROM USERID WHERE STUDENT_ID='$username' AND PASSWORD='$password'";
        $result = $conn->query($sql);

        if ($result->num_rows == 1) {
            // Login successful
            $_SESSION['user_id'] = $username; // Store user ID in session
            header("Location: stdLogin.html");
            exit();
        } else {
            // Login failed
            echo "Invalid username or password";
        }
    } elseif (strlen($username) < 8) {
        // Query to check if the user exists in the database
        $sql = "SELECT * FROM ADMINS WHERE username='$username' AND password='$password'";
        $result = $conn->query($sql);

        if ($result->num_rows == 1) {
            // Login successful
            $_SESSION['user_id'] = $username; // Store user ID in session
            header("Location: adminLogin.html");
            exit();
        } else {
            // Login failed
            echo "Invalid username or password";
        }
    }
}

$conn->close();
?>
