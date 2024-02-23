<?php
if (isset($_FILES['studentFile']) && $_FILES['studentFile']['error'] === UPLOAD_ERR_OK) {
    $fileTmpPath = $_FILES['studentFile']['tmp_name'];
    $fileName = $_FILES['studentFile']['name'];
    $fileSize = $_FILES['studentFile']['size'];
    $fileType = $_FILES['studentFile']['type'];

    $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
    $allowedExtensions = ['csv'];

    if (in_array($fileExtension, $allowedExtensions)) {
        $csvData = array_map('str_getcsv', file($fileTmpPath));

        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "STUDENT_MARKS_MANAGEMENT";

        $conn = new mysqli($servername, $username, $password, $dbname);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "INSERT INTO STUDENT_DETAILS (STUDENT_ID, STUDENT_NAME, STUDENT_GENDER, STUDENT_DOB, STUDENT_PH, BRANCH_ID, STUDENT_BATCH) VALUES (?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);

        foreach ($csvData as $row) {
            $studentId = $row[0];
            $studentName = $row[1];
            $studentGender = $row[2];
            $dobMDY = $row[3];
            $studentPhone = "";

            // echo $dobMDY."\n";

            if(empty($dobMDY)){
                $dobDMY = "0000-00-00";
            }


            // Check if the student ID already exists in the database
            $checkIfExistsQuery = "SELECT STUDENT_ID FROM STUDENT_DETAILS WHERE STUDENT_ID = ?";
            $checkIfExistsStmt = $conn->prepare($checkIfExistsQuery);
            $checkIfExistsStmt->bind_param("s", $studentId);
            $checkIfExistsStmt->execute();
            $checkIfExistsResult = $checkIfExistsStmt->get_result();

            if ($checkIfExistsResult->num_rows > 0 ) {
                // Student ID already exists, skip this iteration
                continue;
            }

            $dobYMD = substr($dobMDY, 0, 2) . substr($dobMDY, 3, 2) . substr($dobMDY, 6, 4);
            $branchId = substr($studentId, 7, 1);
            $year = (int) substr($studentId, 0, 2);
            $studentBatch = (substr($studentId, 4, 1) == 5) ? "20" . ($year - 1) : "20" . $year;

            // echo $dobYMD." ";
            

            if($studentId == "HTNO" || $servername == "STUDENTNAME"){
                continue;
            }

            $stmt->bind_param("sssssss", $studentId, $studentName, $studentGender, $dobYMD, $studentPhone, $branchId, $studentBatch);

            if (!$stmt->execute()) {
                die("Error inserting record: " . $stmt->error);
            }

            // Insert student ID as password into USERID table
            $sqlUserId = "INSERT INTO USERID (STUDENT_ID, PASSWORD) VALUES (?, ?)";
            $stmtUserId = $conn->prepare($sqlUserId);
            $stmtUserId->bind_param("ss", $studentId, $dobYMD);
            
            // echo " ".$studentId." ".$dobYMD;
            if (!$stmtUserId->execute()) {
                die("Error inserting record into USERID: " . $stmtUserId->error);
            }

            $stmtUserId->close();
            $stmt->reset();
        }

        $stmt->close();
        $conn->close();

        header("Location: student_details_upload.html?success=true");
        exit();
    } else {
        echo "Invalid file extension. Please upload a CSV file.";
    }
} else {
    echo "File upload failed or no file was selected.";
}
?>
