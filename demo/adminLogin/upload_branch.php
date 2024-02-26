<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (isset($_FILES['branchFile']) && $_FILES['branchFile']['error'] === UPLOAD_ERR_OK) {
        // CSV File Upload
        $fileTmpPath = $_FILES['branchFile']['tmp_name'];
        $fileName = $_FILES['branchFile']['name'];
        $fileSize = $_FILES['branchFile']['size'];
        $fileType = $_FILES['branchFile']['type'];

        $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));
        $allowedExtensions = ['csv'];

        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "STUDENT_MARKS_MANAGEMENT";

        if (in_array($fileExtension, $allowedExtensions)) {
            $csvData = array_map('str_getcsv', file($fileTmpPath));

            $conn = new mysqli($servername, $username, $password, $dbname);

            if ($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }

            $sql = "INSERT INTO BRANCH_ID_DETAILS (BRANCH_ID, BRANCH_NAME) VALUES (?, ?)";
            $stmt = $conn->prepare($sql);

            foreach ($csvData as $row) {
                $branchId = $row[0];
                $branchName = $row[1];
                if($branchName != "BRANCH_NAME"){
                    $stmt->bind_param("is", $branchId, $branchName);
                    $stmt->execute();
                }
            }

            $stmt->close();
            $conn->close();

            header("Location: upload_branch.html?success=true");
            exit();
        } else {
            echo "Invalid file extension. Please upload a CSV file.";
        }
    } elseif (isset($_POST['subjectNumber']) && isset($_POST['subjectCode'])) {
        // Manual Entry
        $subjectNumber = $_POST['subjectNumber'];
        $subjectCode = $_POST['subjectCode'];

        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "STUDENT_MARKS_MANAGEMENT";

        

        $conn = new mysqli($servername, $username, $password, $dbname);

        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }

        $sql = "INSERT INTO BRANCH_ID_DETAILS (BRANCH_ID, BRANCH_NAME) VALUES (?, ?)";
        $stmt = $conn->prepare($sql);

        $stmt->bind_param("is", $subjectNumber, $subjectCode);
        $stmt->execute();

        $stmt->close();
        $conn->close();

        header("Location: upload_branch.html?success=true");
        exit();
    } else {
        echo "File upload failed or no file was selected.";
    }
}
?>
