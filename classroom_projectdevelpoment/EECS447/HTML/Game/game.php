<?php

session_start();
	if (isset($_SESSION['user_id'])) 
	{
		$mysqli = require __DIR__ . "/../PHP/Connect.php";
		$id = $_SESSION['user_id'];
		$user_name = $_SESSION["user_name"];

		$statement = "SELECT * FROM users WHERE id = '$id'";	
		$result = $mysqli->query($statement);
		$user = $result->fetch_assoc();

		$statement = "SELECT * FROM playersinfo WHERE username = '$user_name'";	
		$inforesult = $mysqli->query($statement);

		$statement = "SELECT player_achievements.player_id, player_achievements.achievement_id, achievements.name
		FROM player_achievements
		JOIN achievements ON player_achievements.achievement_id = achievements.id
		WHERE player_achievements.player_id = '?'";

		$statement = "SELECT name FROM listofitems";
		$stmt = $mysqli->prepare($statement);
		$stmt->execute();
		$listofitems = [];
		foreach ($stmt->get_result() as $row)
		{
			$listofitems[] = $row['name'];
		}
		// print_r($listofitems);
		// Array ( [0] => sword [1] => shield [2] => gauntlets [3] => chestplate [4] => leggings [5] => boots [6] => greatsword ) 


		$statement = "SELECT player_achievements.player_id, player_achievements.achievement_id, achievements.name
		FROM player_achievements
		JOIN achievements ON player_achievements.achievement_id = achievements.id
		WHERE player_achievements.player_id = '?'";

		if($inforesult->num_rows == 0)
		{
			$stats = array("levelStart"=>"1", "goldStart"=>"0", "healthStart"=>"10", "buytextStart"=>"10", "dmgStart"=>"1",);
		}
		else
		{
			$stats = $inforesult->fetch_assoc();
		}
	}
	else
	{
		$stats = array("levelStart"=>"1", "goldStart"=>"0", "healthStart"=>"10", "buytextStart"=>"10", "dmgStart"=>"1",);
	}

?>


<!DOCTYPE html>
<html>
<head>

    <link rel="stylesheet" type="text/css" href="style.css">
	<title>Monster Adventure</title>
	<meta name="userNAME" content="<?= htmlspecialchars($user["username"]) ?>">
	<meta name="levelStart" content="<?= htmlspecialchars($stats["levelStart"]) ?>">
    <meta name="goldStart" content="<?= htmlspecialchars($stats["goldStart"]) ?>">
    <meta name="healthStart" content="<?= htmlspecialchars($stats["healthStart"]) ?>">
	<meta name="buytextStart" content="<?= htmlspecialchars($stats["buytextStart"]) ?>">
	<meta name="dmgStart" content="<?= htmlspecialchars($stats["dmgStart"]) ?>">

	<script>
		var passedArray = 
		<?php 
			echo json_encode($listofitems); 
		?> ;
	</script>

	<meta name="count" content="<?= htmlspecialchars($user["username"]) ?>">

	<script src="script.js"></script>

</head>

<body>

	<?php if (isset($user)): ?>    
        <h1>Monster Adventure | Player : <?= htmlspecialchars($user["username"]) ?></h1>
        <p><a href="../PHP/Logout.php">Disconnect</a></p>
    <?php else: ?>
        <p><a href="../main.php">Log in</a> or <a href="../SignUp/signupPage.html">Sign Up</a> to connect progress</p>
    <?php endif; ?>


	<h2>Click the monster to fight!</h2>

	<button onclick="fight()">Fight</button>
	<button onclick="buy()"><div id="buytext">Buy: <?= htmlspecialchars($stats["buytextStart"]) ?></div></button>
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
				<p> <span id="items"></span> </p>
			</div>
			
			<div id ="item-message"> </div>
		
		</div>
		<div id="boxes">

			<p>Achievements:</p>
			<p>Kill 1 Enemy</p>
			<p>Get 100 Gold</p>

		</div>
	
	</div>
	<br>
	<div id="dmg">Current Damage: 1</div>
</body>
</html>



