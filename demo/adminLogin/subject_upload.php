<?php
// Establish database connection
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "STUDENT_MARKS_MANAGEMENT";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}



// Check if file has been uploaded
if (isset($_FILES['csv_file']['name'])) {
    $file_name = $_FILES['csv_file']['name'];
    $file_temp = $_FILES['csv_file']['tmp_name'];

    // Read the CSV file
    if (($handle = fopen($file_temp, "r")) !== FALSE) {
        // Loop through each row in the CSV file
        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            $subject_code = $conn->real_escape_string($data[0]); // Assuming first column contains subject code
            $subject_name = $conn->real_escape_string($data[1]); // Assuming second column contains subject name
            $subject_credits = $conn->real_escape_string($data[2]); // Assuming third column contains subject credits

            if ($subject_name != "SUBJECT_NAME") {
                // Insert data into database
                $sql = "INSERT INTO SUBJECT_TABLE (SUBJECT_CODE, SUBJECT_NAME, SUBJECT_CREDITS) VALUES ('$subject_code', '$subject_name', $subject_credits)";
                if ($conn->query($sql) !== TRUE) {
                    echo "Error: " . $sql . "<br>" . $conn->error;
                }
            }
        }
        fclose($handle);
        header("Location: subject_upload.html?notification=CSV%20file%20data%20imported%20successfully!");
        exit();
    } else {
        echo "Error: Unable to open file.";
    }
} else {
    // Handle manual form submission
    $subject_code = $conn->real_escape_string($_POST['subject_code']);
    $subject_name = $conn->real_escape_string($_POST['subject_name']);
    $subject_credits = $conn->real_escape_string($_POST['subject_credits']);

    // Insert data into database
    $sql = "INSERT INTO SUBJECT_TABLE (SUBJECT_CODE, SUBJECT_NAME, SUBJECT_CREDITS) VALUES ('$subject_code', '$subject_name', $subject_credits)";
    if ($conn->query($sql) !== TRUE) {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    header("Location: subject_upload.html?notification=Manual%20data%20imported%20successfully!");
    exit();
}

// Close database connection
$conn->close();
?>
