<?php
// Start the session
session_start();

// Check if user is logged in and session variable is set
if (!isset($_SESSION['user_id'])) {
    // Redirect user to login page or handle unauthorized access
    header("Location: login.php"); // Redirect to login page
    exit(); // Stop script execution
}

// Establish database connection
include '../configuration.php';

// Validate user input
function validateInput($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Retrieve and validate form data
$user_id = $_SESSION['user_id']; // Get user_id from session

$old_password = validateInput($_POST['old_password']);
$new_password = validateInput($_POST['new_password']);
$confirm_password = validateInput($_POST['confirm_password']);

// Check if any field is empty
if (empty($old_password) || empty($new_password) || empty($confirm_password)) {
    echo "All fields are required.";
    exit;
}

// Query to check old password
$sql = "SELECT * FROM USERID WHERE USER_ID='$user_id' AND PASSWORD='$old_password'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Old password is correct
    if ($new_password == $confirm_password) {
        // Update the password
        $update_sql = "UPDATE USERID SET PASSWORD='$new_password' WHERE USER_ID='$user_id'";
        if ($conn->query($update_sql) === TRUE) {
            echo "Password updated successfully";
        } else {
            echo "Error updating password: " . $conn->error;
        }
    } else {
        // New password and confirmation password do not match
        echo "New password and confirmation password do not match";
    }
} else {
    // Old password is incorrect
    echo "Old password is incorrect";
}

$conn->close();
?>
