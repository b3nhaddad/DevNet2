<?php
// Error logging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
ini_set('log_errors', 1);
ini_set('error_log', '/s/bach/l/under/carter64/public_html/php_errors.log');
error_reporting(E_ALL);

$target_dir = "/s/bach/l/under/carter64/public_html/uploads";

// Check if file is uploaded
if (!isset($_FILES["fileToUpload"]) || $_FILES["fileToUpload"]["error"] != 0) {
    echo "Error: No file uploaded or there was an upload error.";
    exit;
}

$target_file = $target_dir . "/" . time() . "_" . basename($_FILES["fileToUpload"]["name"]);
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

// Verify the file is an image
$check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
if ($check === false) {
    echo "Error: File is not an image.";
    exit;
}
// Restrict file types to JPG, JPEG, and PNG
$allowed_types = array("jpg", "jpeg", "png");
if (!in_array($imageFileType, $allowed_types)) {
    echo "Error: Only JPG, JPEG, and PNG files are allowed.";
    exit;
}

// Move the file and process with Python if upload is successful
if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
    $command = "/usr/local/anaconda3/2022.08/bin/python3.9 /s/bach/l/under/carter64/public_html/upload.py " . escapeshellarg($target_file) . " 2>&1";
    $output = shell_exec($command);

    if ($output) {
        echo htmlspecialchars($output);
    } else {
        echo "Error: No output from Python script.";
    }
} else {
    echo "Error: Failed to upload the file.";
}
?>
