<?php

$host = "localhost";
$database = "login_db";
$name = "root";
$pass = "";

$mysqli = new mysqli(hostname: $host, username: $name, password: $pass, database: $database);
                     
if ($mysqli->connect_errno) 
{
    die("Connection error: " . $mysqli->connect_error);
}

return $mysqli;

?>