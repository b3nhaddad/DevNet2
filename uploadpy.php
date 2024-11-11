<?php
$target_dir = "/s/bach/l/under/carter64/public_html/uploads";
$target_file = $target_dir . time() . "_" . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

// Check if file is an image
if (isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if ($check !== false) {
        echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}

// Additional file validations can go here

// Call the Python script if the upload is valid
if ($uploadOk == 1) {
    // Move the uploaded file to a temporary location
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        // Execute the Python script, passing the file path as an argument
        $command = escapeshellcmd("python3 /s/bach/l/under/carter64/public_html/upload.py " . escapeshellarg($target_file));
        $output = shell_exec($command);

        echo $output; // Display the output from the Python script
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
} else {
    echo "Sorry, your file was not uploaded.";
}
?>