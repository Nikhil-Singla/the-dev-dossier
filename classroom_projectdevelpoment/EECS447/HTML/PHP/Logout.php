<?php

session_start();

if (isset($_SESSION['user_id'])) 
{
	$mysqli = require __DIR__ . "/Connect.php";

	$sql = "UPDATE playersinfo
	SET playersinfo.levelStart = ?, playersinfo.goldStart = ?, playersinfo.healthStart = ?, playersinfo.buytextStart = ?, playersinfo.dmgStart = ?
	WHERE playersinfo.username = ?";

	$stmt = $mysqli->stmt_init();

	if ( ! $stmt->prepare($sql)) {
		die("SQL error: " . $mysqli->error);
	}

	$level = $_COOKIE['level'];
	$gold = $_COOKIE['gold'];
	$health = $_COOKIE['health'];
	$buytext = $_COOKIE['buytext'];
	$dmg = $_COOKIE['dmg'];
	$name = $_COOKIE['username'];

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