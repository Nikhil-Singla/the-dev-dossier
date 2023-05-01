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
    
    
>