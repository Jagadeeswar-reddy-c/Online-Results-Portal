<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Student Details</title>
    <link rel="stylesheet" href="./stylesheet/button.css">
</head>
<body>
    <h2>Edit Student Details</h2>

    <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
        <label for="student_id">Enter Student ID:</label>
        <input type="text" name="student_id" required>
        <br>

        <button  class="button-5" role="button" type="submit">Search</button>
    </form>

    <?php
        // Check if the form is submitted
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            // Include your database connection file
            include 'db_connection.php';

            // Get the input value
            $studentId = $_POST["student_id"];

            // Retrieve student details from the database
            $query = "SELECT * FROM USER_DETAILS WHERE USER_ID = '$studentId'";
            $result = mysqli_query($connection, $query);

            if ($result && mysqli_num_rows($result) > 0) {
                $row = mysqli_fetch_assoc($result);
    ?>
                <!-- Display the student details with edit form -->
                <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
                    <input type="hidden" name="student_id" value="<?php echo $row['USER_ID']; ?>">
                    <label for="student_name">Name:</label>
                    <input type="text" name="student_name" value="<?php echo $row['USER_NAME']; ?>" required>
                    <br>

                    <label for="student_gender">Gender:</label>
                    <input type="text" name="student_gender" value="<?php echo $row['USER_GENDER']; ?>" required>
                    <br>

                    <label for="student_phone">Phone Number:</label>
                    <input type="text" name="student_phone" value="<?php echo $row['USER_PH']; ?>" required>
                    <br>

                    <button class="button-5" role="button" type="submit" name="edit_submit">Update</button>
                </form>
    <?php
            } else {
                echo "<p>Student with ID $studentId not found.</p>";
            }

            // Close the database connection
            mysqli_close($connection);
        }
    ?>

    <?php
        // Check if the edit form is submitted
        if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["edit_submit"])) {
            // Include your database connection file
            include 'db_connection.php';

            // Get the input values
            $editedId = $_POST["student_id"];
            $editedName = $_POST["student_name"];
            $editedGender = $_POST["student_gender"];
            $editedPhone = $_POST["student_phone"];

            // Update student details in the database
            $updateQuery = "UPDATE USER_DETAILS SET USER_NAME='$editedName', USER_GENDER='$editedGender', USER_PH='$editedPhone' WHERE USER_ID='$editedId'";
            $updateResult = mysqli_query($connection, $updateQuery);

            if ($updateResult) {
                echo "<p>Student details updated successfully.</p>";
            } else {
                echo "<p>Error updating student details: " . mysqli_error($connection) . "</p>";
            }

            // Close the database connection
            mysqli_close($connection);
        }
    ?>
</body>
</html>
