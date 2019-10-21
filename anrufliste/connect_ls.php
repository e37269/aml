<?php
$ls = mysqli_connect('192.168.155.155', 'aml', 'YA2lS8OA', 'leitstelle');
if(!$ls)
{
	exit("Verbindungsfehler Datenbank leitstelle: ".mysqli_connect_error());
}
?>

