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
        $command = "python3 /s/bach/l/under/carter64/public_html/upload.py " . escapeshellarg($target_file) . " 2>&1";
        $output = shell_exec($command);

        if ($output) {
            $message = htmlspecialchars($output);
        } else {
            $message = "No output from Python script.";
        }
    } else {
        $message = "Sorry, there was an error uploading your file.";
    }
} else {
    $message = "Sorry, your file was not uploaded.";
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Classification Result</title>
</head>
<body>
    <h1>Upload an Image</h1>
    <form action="uploadpy.php" method="post" enctype="multipart/form-data">
        <label for="image">Choose an image to upload:</label>
        <input type="file" name="fileToUpload" id="fileToUpload" required>
        <input type="submit" value="Upload Image" name="submit">
    </form>

    <!-- Display the classification result -->
    <?php if (isset($message)): ?>
        <p><strong>Result:</strong> <?php echo $message; ?></p>
    <?php endif; ?>
</body>
</html>
