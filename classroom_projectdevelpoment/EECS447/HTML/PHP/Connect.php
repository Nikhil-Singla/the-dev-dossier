<?php
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
    global $mysqli;

    $mysqli = new mysqli("localhost", "<USERNAME>", "<PASSWORD>", "<DATABASE>");
    
    if ( mysqli_connect_errno() ) 
    {
        printf("Connect failed: %s\n", $mysqli->connect_error);
        exit();
    }
?>