<!-- The below code has been adapted to execute on older php versions (specifically 5.x) --> 

<?php

$is_invalid = false;
if ($_SERVER["REQUEST_METHOD"] === "POST") 
{
    
    $mysqli = require __DIR__ . "/PHP/Connect.php";    
    $sqlStatement = sprintf("SELECT * FROM users
                    WHERE username = '%s'",
                    $mysqli->real_escape_string($_POST["uname"]));
    
    $returnQuery = $mysqli->query($sqlStatement);
    $user = $returnQuery->fetch_assoc();
    
    if ($user) 
    {
        
        if ($_POST["psw"] == $user["password"]) 
        {    
            session_start();   
            session_regenerate_id();
            
            $_SESSION["user_id"] = $user["id"];
            $_SESSION["user_name"] = $user["username"];

            header("Location: Game/game.php");
            exit;
        }
    }
    $is_invalid = true;
}

?>

<!DOCTYPE html>
<html>
<head>
	<title>Login</title>
	<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <div class="container">
        
        <h2>Login</h2>
        
        <?php if ($is_invalid): ?>
            <em>Invalid login</em>
        <?php endif; ?>

        <form method="post">
            
            <label for="uname"><b>Username</b></label>
            <input type="text" placeholder="Enter Username" name="uname" required value="<?= htmlspecialchars(isset($_POST["uname"]) ? $_POST["uname"] : "") ?>">

            <label for="psw"><b>Password</b></label>
            <input type="password" placeholder="Enter Password" name="psw" required>

            <div class="button-container">
                <button type="submit">Login</button>
                <button type="button" class="signup" id="SIGNUP">SignUp</button>
            </div>
        
        </form>
    
    </div>
</body>
<script>
    document.getElementById("SIGNUP").onclick = function () 
    {
        location.href = "SignUp/signupPage.html";
    };
</script>
</html>
