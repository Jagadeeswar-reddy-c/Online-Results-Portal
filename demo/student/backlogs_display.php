<?php

session_start();

include '../configuration.php';

// Function to retrieve failed subjects for a given user ID
function getFailedSubjects($conn, $userID) {
    // SQL query to retrieve failed subjects with subject code and semester information
    $sql = "SELECT SUBJECT_TABLE.SUBJECT_CODE, SUBJECT_TABLE.SUBJECT_NAME, STUDENT_MARKS.SEM_ID
            FROM STUDENT_MARKS
            INNER JOIN SUBJECT_TABLE ON STUDENT_MARKS.SUBJECT_NO = SUBJECT_TABLE.SUBJECT_NO
            WHERE USER_ID = '$userID'
            AND (CAST(STUDENT_MARKS.INTERNAL_MARKS AS INT) + CAST(STUDENT_MARKS.EXTERNAL_MARKS AS INT)) < 40
            AND STUDENT_MARKS.EXTERNAL_MARKS != '-'"; // Exclude rows with EXTERNAL_MARKS as '-'

    // Execute the query
    $result = $conn->query($sql);

    // Check if there are failed subjects
    if ($result->num_rows > 0) {
        echo "<h2>Failed Subjects:</h2>";
        echo "<table border='1'>";
        echo "<tr><th>Subject Code</th><th>Subject Name</th><th>Semester</th></tr>";
        // Output each failed subject with subject code, name, and semester in a table row
        while ($row = $result->fetch_assoc()) {
            echo "<tr><td>" . $row["SUBJECT_CODE"] . "</td><td>" . $row["SUBJECT_NAME"] . "</td><td>" . $row["SEM_ID"] . "</td></tr>";
        }
        echo "</table>";
    } else {
        echo "<h2>No failed subjects found for this student.</h2>";
    }
}

// Assuming you have a session variable for user ID
// Replace 'your_user_id' with the actual user ID from your session
$userID = $_SESSION['user_id'];

// Call the function to get failed subjects
getFailedSubjects($conn, $userID);

// Close the database connection
$conn->close();

?>
