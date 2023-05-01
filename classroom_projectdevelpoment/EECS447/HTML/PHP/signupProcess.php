<?php
print_r($_POST);

if (empty($_POST["usr"])) {
    die("Name is required");
}

if (strlen($_POST["psw"]) < 6) {
    die("Password must be at least 6 characters");
}

if ( ! preg_match("/[a-z]/i", $_POST["psw"])) {
    die("Password must contain at least one letter");
}

if ($_POST["psw"] !== $_POST["psw-repeat"]) {
    die("Passwords must match");
}

$mysqli = require __DIR__ . "/Connect.php";

$sql = "INSERT INTO users (username, password) VALUES (?, ?)";

$stmt = $mysqli->stmt_init();

if ( ! $stmt->prepare($sql)) {
    die("SQL error: " . $mysqli->error);
}

$stmt->bind_param("ss",
                  $_POST["usr"],
                  $_POST["psw"]);

                  if ($stmt->execute()) {

                    header("Location: ../main.php");
                    exit;
                    
                } else {
                    
                    if ($mysqli->errno === 1062) {
                        die("Name already taken");
                    } else {
                        die($mysqli->error . " " . $mysqli->errno);
                    }
                }                

?>