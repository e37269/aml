<?php
$ls = mysqli_connect('host', 'user', 'passwort', 'datenbank');
if(!$ls)
{
	exit("Verbindungsfehler Datenbank leitstelle: ".mysqli_connect_error());
}
?>

