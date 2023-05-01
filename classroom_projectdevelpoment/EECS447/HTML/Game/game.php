<?php

session_start();

	if (isset($_SESSION["user_id"])) 
	{
		
		$mysqli = require __DIR__ . "../PHP/Connect.php";
		
		$sql = "SELECT * FROM users
				WHERE id = {$_SESSION["user_id"]}";
				
		$result = $mysqli->query($sql);
		
		$user = $result->fetch_assoc();
	}

?>


<!DOCTYPE html>
<html>
<head>

    <link rel="stylesheet" type="text/css" href="style.css">
    <script src="script.js"></script>
	<title>Monster Adventure</title>
	
</head>

<body>

	<h1>Monster Adventure |  	
	<?php if (isset($user)): ?>    
        Player : <?= htmlspecialchars($user["username"]) ?>
        <p><a href="../PHP/Logout.php">Disconnect</a></p>
    <?php else: ?>
        <p><a href="../main.php">Log in</a> or <a href="../SignUp/signupPage.html">Sign Up</a> to connect progress</p>
    <?php endif; ?>

	</h1>

	<h2>Click the monster to fight!</h2>

	<button onclick="fight()">Fight</button>
	<button onclick="buy()"><div id="buytext">Buy: 10</div></button>
	<br>
	<div>
	
		<div id="boxes">

			<p>Level: <span id="level">1</span></p>
			<p>Gold: <span id="gold">0</span></p>
			<p>Health: <span id="health">10</span></p>
		
		</div>

		<div id="itemboxes">

			<p>Items:</p>
			<div id="itemnames">
				<p>ABC</p>
				<p>DEF</p>
			</div>
			
			<div id ="item-message"> </div>
		
		</div>
		<div id="boxes">

			<p>Achievements:</p>
			<p>UNLOCKED!</p>

		</div>
	
	</div>
	<br>
	<div id="dmg">Current Damage: 1</div>
</body>
</html>



