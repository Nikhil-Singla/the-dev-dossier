<?php

session_start();

if (isset($_SESSION['user_id'])) 
{
	$mysqli = require __DIR__ . "/Connect.php";

	$sql = "UPDATE playersinfo
	INNER JOIN users ON users.username = playersinfo.username 
	SET playersinfo.levelStart = ?, playersinfo.goldStart = ?, playersinfo.healthStart = ?, playersinfo.buytextStart = ?, playersinfo.dmgStart = ?
	WHERE users.id = ?";

	$stmt = $mysqli->stmt_init();

	if ( ! $stmt->prepare($sql)) {
		die("SQL error: " . $mysqli->error);
	}

	$level = $_COOKIE['level'];
	$gold = $_COOKIE['gold'];
	$health = $_COOKIE['health'];
	$buytext = $_COOKIE['buytext'];
	$dmg = $_COOKIE['dmg'];
	$name = $_SESSION['user_id'];


	$achieve_one = $_COOKIE['achievement1'];
	$achieve_two = $_COOKIE['achievement2'];
	$achievements = array();
	$achievements = array_push($achieve_one, $achieve_two);

	foreach ($achievements as &$code) 
	{
		$code = intval($code);
	}

	

	$stmt->bind_param("iiiiis", $level, $gold, $health, $buytext, $dmg, $name);
	$stmt->execute();
}

if(isset($_SESSION['user_id']))
{
	unset($_SESSION['user_id']);
}

session_destroy();

header("Location: ../Game/game.php");

?>