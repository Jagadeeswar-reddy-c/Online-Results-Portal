<?php
// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve student ID from the form
    $student_id = $_POST['student_id'];

    // Change these credentials to match your MySQL server
    include '../configuration.php';

    // Query to reset password based on USER_DOB
    $sql = "SELECT USER_ID FROM USER_DETAILS WHERE USER_ID = '$student_id'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        $user_id = $row["USER_ID"];

        // Assuming USER_DOB is stored in the format 'YYYYMMDD'
        $sql = "UPDATE USERID SET PASSWORD = USER_DOB WHERE USER_ID = '$user_id'";
        
        if ($conn->query($sql) === TRUE) {
            echo "Password reset successfully. Your new password is your date of birth (YYYYMMDD).";
        } else {
            echo "Error resetting password: " . $conn->error;
        }
    } else {
        echo "Student ID not found.";
    }

    // Close connection
    $conn->close();
}
?>
