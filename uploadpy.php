<?php
$target_dir = "/s/bach/l/under/carter64/public_html/uploads";
$target_file = $target_dir . "/" . time() . "_" . basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file, PATHINFO_EXTENSION));

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

if (isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if ($check !== false) {
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}

$allowed_types = array("jpg", "jpeg", "png");
if (!in_array($imageFileType, $allowed_types)) {
    echo "Only JPG, JPEG, and PNG files are allowed.";
    $uploadOk = 0;
}

if ($uploadOk == 1) {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        // Execute the Python script with error capture
        $command = "python3 /s/bach/l/under/carter64/public_html/upload.py " . escapeshellarg($target_file) . " 2>&1";
        $output = shell_exec($command);
        
        if ($output) {
            echo htmlspecialchars($output);
        } else {
            echo "No output from Python script.";
        }
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
} else {
    echo "Sorry, your file was not uploaded.";
}
?>
