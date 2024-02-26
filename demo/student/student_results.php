<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Marks</title>
</head>
<body>
    <h2>Student Marks</h2>

    <form action="" method="post">
        <!-- Remove the input field for student_id -->
        <!-- The student ID will be automatically retrieved from the session -->

        <label for="sem_id">Select Semester:</label>
        <select id="sem_id" name="sem_id" required>
            <!-- Replace the values and labels below with your actual semester values -->
            <option value="1">Semester 1</option>
            <option value="2">Semester 2</option>
            <option value="3">Semester 3</option>
            <option value="4">Semester 4</option>
            <option value="5">Semester 5</option>
            <option value="6">Semester 6</option>
            <option value="7">Semester 7</option>
            <option value="8">Semester 8</option>
            <!-- Add more options as needed -->
        </select>

        <br>
        <button type="submit" name="displayMarks">Display Marks</button>
    </form>

    <?php
    // Start the session
    session_start();

    // Include the PHP code here
    if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["displayMarks"])) {
        // Database connection parameters
        $servername = "localhost";
        $username = "root";
        $password = "";
        $dbname = "STUDENT_MARKS_MANAGEMENT";

        // Create connection
        $connection = new mysqli($servername, $username, $password, $dbname);

        // Check connection
        if ($connection->connect_error) {
            die("Connection failed: " . $connection->connect_error);
        }

        // Get input values from the form
        $student_id = $_SESSION["user_id"]; // Retrieve user ID from session
        $sem_id = $_POST["sem_id"];

        // Your SQL query
        $sql = "SELECT ST.SUBJECT_CODE, ST.SUBJECT_NAME, SM.INTERNAL_MARKS, SM.EXTERNAL_MARKS, ST.SUBJECT_CREDITS
                FROM USER_DETAILS SD
                INNER JOIN STUDENT_MARKS SM ON SD.USER_ID = SM.USER_ID
                INNER JOIN SUBJECT_TABLE ST ON SM.SUBJECT_NO = ST.SUBJECT_NO
                WHERE SD.USER_ID = '$student_id' AND SM.SEM_ID = $sem_id";
        
        // Execute the query
        $result = $connection->query($sql);

        // $student_name = $connection->query("SELECT SD.STUDENT_NAME FROM STUDENT_DETAILS SD WHERE SD.STUDENT_ID = '$student_id'");
        $nameResult = $connection->query("SELECT SD.USER_NAME FROM USER_DETAILS SD WHERE SD.USER_ID = '$student_id'");


        if ($nameResult) {
            // Fetch the result row
            $nameRow = $nameResult->fetch_assoc();
        
            // Display the student name
            $student_name = $nameRow['USER_NAME'];
        } else {
            // Handle the error if query fails
            echo "Error fetching student name: " . $connection->error;
        }

        // Check if there are any results
        if ($result) {
            // Display the results in a table
            echo "<h3>Student ID: $student_id  &nbsp&nbsp Student Name: $student_name</h3>";
            echo "<h3>Sem ID: $sem_id</h3>";
            echo "<h3>Student Marks</h3>";
            echo "<table border='1'>
                    <tr>
                        <th>Subject Code</th>
                        <th>Subject Name</th>
                        <th>Internal Marks</th>
                        <th>External Marks</th>
                        <th>Subject Credits</th>
                    </tr>";

            while ($row = $result->fetch_assoc()) {
                echo "<tr>
                        <td>{$row['SUBJECT_CODE']}</td>
                        <td>{$row['SUBJECT_NAME']}</td>
                        <td>{$row['INTERNAL_MARKS']}</td>
                        <td>{$row['EXTERNAL_MARKS']}</td>
                        <td>{$row['SUBJECT_CREDITS']}</td>
                    </tr>";
            }

            echo "</table>";
        } else {
            echo "Error executing the query: " . $connection->error;
        }

        // Close the database connection
        $connection->close();
    }
    ?>
</body>
</html>
