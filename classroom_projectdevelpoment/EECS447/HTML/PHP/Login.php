<?php

    session_start();
    ob_start();

    include 'Connection.php';
    if ( !isset($_POST['uname'], $_POST['psw']) ) 
    {
      exit('Please fill both the username and password fields!');
    }
    
    $uname = $_POST['uname'];
    $password = $_POST['psw'];

    $query = "SELECT * from users WHERE username='$uname';";
    
    if ($result = $mysqli->query($query)) 
    {
      while ($entity = $result->fetch_assoc()) 
      {
        if($entity["password"] == $password) 
        {
          $flag = TRUE;
          
          $_SESSION['<LOGIN CONDITION>'] = True;
          $_SESSION['id'] = $entity["id"];
          $_SESSION['username'] = $entity["username"];

          if (isset($_SESSION['loginSuccessful'])) 
          {
            echo "<p> You have successfully logged in! </p>";
            header('<LOCATION>');
            exit;
          }
        }
      }
      $result->free();
    }
    echo "<p> Failed Authentication! </p>";
    echo "<a href='./SignIn.html'>Try again</a>";
    $mysqli->close();
?>