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

// Include PHPMailer classes
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'phpmailer/src/Exception.php';
require 'phpmailer/src/PHPMailer.php';
require 'phpmailer/src/SMTP.php';

// Retrieve input values from login form
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $user_id = $username;
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

            if ($userNum == 1) {
        
                // Create a new PHPMailer instance
                $mail = new PHPMailer(true);

                // SMTP settings
                $mail->isSMTP();
                $mail->Host = 'smtp.gmail.com';
                $mail->SMTPAuth = true;
                $mail->Username = '209y1a0542@ksrmce.ac.in'; // Your email address
                $mail->Password = 'towcmfxkhiiabhdr'; // Your email password
                $mail->SMTPSecure = 'ssl';
                $mail->Port = 465;

                // Sender and recipient
                $mail->setFrom('209y1a0542@ksrmce.ac.in');
                $to = $user_id . '@ksrmce.ac.in'; // User's email address
                $mail->addAddress($to);

                // Email content
                $mail->isHTML(true);
                $mail->Subject = "Login Notification";
                $mail->Body = "Hello $userName, you have successfully logged in.";
            }
            
            // Send email
            if ($userNum == 2 || $userNum == 3) {
                echo "success$userNum $userName"; 
            } else if ($userNum == 1) {
                if($mail->send()){
                    echo "success$userNum $userName";
                }
                // Return success response with user role and name
                 
            } else {
                // Login failed
                echo "Mail sending failed";
            }
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
