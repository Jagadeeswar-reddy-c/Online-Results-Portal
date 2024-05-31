<?php
// Database connection
include '../configuration.php';

$semester_id = $_POST['semester_id'];

// Retrieve form data or handle files directly without form submission

// File handling for internal marks
$internal_marks_file = $_FILES['internal_marks']['tmp_name'];
$internal_data = array_map('str_getcsv', file($internal_marks_file));

// File handling for external marks
$external_marks_file = $_FILES['external_marks']['tmp_name'];
$external_data = array_map('str_getcsv', file($external_marks_file));

// Insert data from internal marks
foreach ($internal_data as $key => $internal_row) {
    $student_id = $internal_row[0];
    $subject_code = $internal_row[1];


    if($subject_code != "SUBCODE"){
        // Fetch SUBJECT_NO based on SUBJECT_CODE from SUBJECT_TABLE
        $subject_query = "SELECT SUBJECT_NO FROM SUBJECT_TABLE WHERE SUBJECT_CODE = '$subject_code'";
        $subject_result = $conn->query($subject_query);

        if ($subject_result !== false && $subject_result->num_rows > 0) {
            $subject_data = $subject_result->fetch_assoc();
            $subject_no = $subject_data['SUBJECT_NO'];

            // Check if internal marks are present
            if (isset($internal_row[2])) {
                
                $internal_marks = $internal_row[2];
                if($internal_marks<0){
                    if($internal_marks==-7){
                        $internal_marks = '-';
                    }elseif($internal_marks == -1){
                        $internal_marks = 'AB';
                    }elseif($internal_marks == -2){
                        $internal_marks = 'MP';
                    }
                }
                if($internal_marks > 40) {
                    $internal_marks = 40;
                }
                
            } else {
                // Set internal marks as "NG" (Not Given) if absent
                $internal_marks = '-';
            }

            // Set external marks as "NG" (Not Given) for now
            $external_marks = '-';

            // Check if a record already exists for the student and subject
            $check_query = "SELECT * FROM STUDENT_MARKS WHERE USER_ID = '$student_id' AND SUBJECT_NO = '$subject_no'";
            $check_result = $conn->query($check_query);

            if ($check_result !== false && $check_result->num_rows > 0) {
                // Update the existing record with internal marks
                $update_sql = "UPDATE STUDENT_MARKS SET INTERNAL_MARKS = '$internal_marks' WHERE USER_ID = '$student_id' AND SUBJECT_NO = '$subject_no'";
                if ($conn->query($update_sql) !== TRUE) {
                    echo "Error updating record: " . $conn->error;
                }
            } else {
                // echo $subject_no." ";
                // Insert a new record for internal marks
                $insert_sql = "INSERT INTO STUDENT_MARKS (USER_ID, SUBJECT_NO, INTERNAL_MARKS, EXTERNAL_MARKS, SEM_ID) VALUES ('$student_id', '$subject_no', '$internal_marks', '$external_marks',$semester_id)";
                // echo $subject_no." ".$subject_code." ".$insert_sql;
                if ($conn->query($insert_sql) !== TRUE) {
                    echo "Error inserting record: " . $conn->error;
                }
            }
        } else {
            // echo "Subject code '$subject_code' not found or no corresponding SUBJECT_NO in the SUBJECT_TABLE.<br>";
        }
    }
}

// Insert data from external marks
foreach ($external_data as $key => $external_row) {
    $student_id = $external_row[0];
    $subject_code = $external_row[1];

    if($subject_code != "SUBCODE"){
        // Fetch SUBJECT_NO based on SUBJECT_CODE from SUBJECT_TABLE
        $subject_query = "SELECT SUBJECT_NO FROM SUBJECT_TABLE WHERE SUBJECT_CODE = '$subject_code'";
        $subject_result = $conn->query($subject_query);

        if ($subject_result !== false && $subject_result->num_rows > 0) {
            $subject_data = $subject_result->fetch_assoc();
            $subject_no = $subject_data['SUBJECT_NO'];

            // Set internal marks as "NG" (Not Given) for now
            $internal_marks = '-';

            // Check if external marks are present
            if (isset($external_row[2])) {
                $external_marks = $external_row[2];
                if($external_marks < 0){
                    if($external_marks==-1){
                        $external_marks = 'AB';
                    }elseif($external_marks==-2){
                        $external_marks = 'MP';
                    }elseif($external_marks==-7){
                        $external_marks = '-';
                    }
                }
                if($external_marks > 70) {
                    $external_marks = 70;
                }
            } else {
                // Set external marks as "NG" (Not Given) if absent
                $external_marks = '-';
            }

            

            // Check if a record already exists for the student and subject
            $check_query = "SELECT * FROM STUDENT_MARKS WHERE USER_ID = '$student_id' AND SUBJECT_NO = '$subject_no'";
            $check_result = $conn->query($check_query);


            if ($check_result !== false && $check_result->num_rows > 0) {
                // Update the existing record with external marks
                $update_sql = "UPDATE STUDENT_MARKS SET EXTERNAL_MARKS = '$external_marks' WHERE USER_ID = '$student_id' AND SUBJECT_NO = '$subject_no'";
                if ($conn->query($update_sql) !== TRUE) {
                    echo "Error updating record: " . $conn->error;
                }
            } else {
                // Insert a new record for external marks
                $insert_sql = "INSERT INTO STUDENT_MARKS (USER_ID, SUBJECT_NO, INTERNAL_MARKS, EXTERNAL_MARKS, SEM_ID) VALUES ('$student_id', '$subject_no', '$internal_marks', '$external_marks',$semester_id)";
                if ($conn->query($insert_sql) !== TRUE) {
                    echo "Error inserting record: " . $conn->error;
                }
            }
        } else {
            // echo "Subject code '$subject_code' not found or no corresponding SUBJECT_NO in the SUBJECT_TABLE.<br>";
        }
    }
}

// Close the database connection
$conn->close();
// Respond with a success message
echo "success";
exit();
?>

