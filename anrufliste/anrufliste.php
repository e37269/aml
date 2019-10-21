<!DOCTYPE html>
<html lang="en">
<head>
	<title>AML-Geodaten</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" type="text/css" href="css/style.css">

<!--===============================================================================================-->
<meta http-equiv="refresh" content="10" > 
</head>

<body>

	<table>
		<caption>AML-Geodaten vom <?php echo date("d.m.Y", strtotime("-2 day")) . " - " . date("d.m.Y"); ?></caption>
			<thead>
				<tr>
					<th scope="col">Rufnummer</th>
					<th scope="col">Zeitpunkt Lokalisierung</th>
					<th scope="col">Anrufzeit</th>
					<th scope="col">Position</th>
					<th scope="col">Genauigkeit (in m)</th>
				</tr>
			</thead>
			<tbody>
<?php
echo "<BR>Aktualisierungsintervall: 10 Sekunden<br>";
echo "<BR>letzte Aktualisierung: ".date("d.m.Y - H:i:s")." Uhr";
?>

<?php

include('connect_ls.php');
$eintraege = mysqli_query($ls, "select count(*) from aml");
$row = mysqli_fetch_row($eintraege);
$datensaetze = $row[0];

$aml_tabelle = mysqli_query($ls, 'select number, location_time, concat(location_latitude, " ", location_longitude), location_accuracy, anrufzeit from aml WHERE date_format(location_time, "%Y-%m-%d") BETWEEN SUBDATE(CURDATE(), 2) AND CURDATE()order by location_time DESC');

while($row = mysqli_fetch_row($aml_tabelle))
       {
       $_spalte0 = htmlentities($row[0]);
       $_spalte1 = date("d.m.Y - H:i:s", strtotime(htmlentities($row[1])));
       $_spalte2 = date("d.m.Y - H:i:s", strtotime(htmlentities($row[4])));
       $_spalte3 = explode(" ", htmlentities($row[2]));
	   $_spalte4 = htmlentities(str_replace(".", ",", number_format($row[3], 2, ".", ",")));
	   
	   $l_anzeige = strlen($_spalte3[0]) > 10 ? substr($_spalte3[0],0,10)."..." : $_spalte3[0];
	   $b_anzeige = strlen($_spalte3[1]) > 10 ? substr($_spalte3[1],0,10)."..." : $_spalte3[1];
	   
	   
	   	
				echo '<tr>';
					echo "<td data-label=\"Rufnummer\">$_spalte0</td>";
					echo "<td data-label=\"Zeitpunkt Lokalisierung\">$_spalte1</td>";
					echo "<td data-label=\"Anrufzeit\">$_spalte2</td>";
					echo "<td data-label=\"Position\"><a href='http://192.168.155.211/#16/$_spalte3[0]/$_spalte3[1]' target=\"_blank\" style=\" color: black \" \">$l_anzeige<br>$b_anzeige</a></td>";
					echo "<td data-label=\"Genauigkeit (in m)\">$_spalte4</td>";
				echo '</tr>';
	   };
?>		
			



			</tbody>
	</table>
</body>

</html>
