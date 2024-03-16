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

    $sql = "SELECT * FROM USERID WHERE USER_ID='$username' AND PASSWORD='$password'";
    $result = $conn->query($sql);

    if ($result->num_rows == 1) {
        $userNumResult = $conn->query("SELECT USER_NUM FROM USER_DETAILS WHERE USER_ID='$username'");

        $row = $userNumResult->fetch_assoc();
        $userNum = $row['USER_NUM'];

        if ($userNum == 1 || $userNum == 2 || $userNum == 3) {
            $_SESSION['user_id'] = $username;
            
            // Retrieve user's name from the database
            $userNameResult = $conn->query("SELECT USER_NAME FROM USER_DETAILS WHERE USER_ID='$username'");
            $row = $userNameResult->fetch_assoc();
            $userName = $row['USER_NAME'];
        
            $to = $username . '@ksrmce.ac.in'; // User's email address
            $subject = "Login Notification";
            $message = "Hello, you have successfully logged in.";
            $headers = "From: college"; // Your email address
        
            // Send email
            mail($to, $subject, $message, $headers);
        
            // Return success response with user role and name
            echo "success$userNum $userName"; 
        } else {
            // Login failed
            echo "Invalid username or password";
        }        
    } else {
        // Login failed
        echo "Invalid username or password";
    }
}

$conn->close();
?>
