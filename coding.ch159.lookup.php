<?php
	$cdir = dirname(__FILE__) . '/crackstation-hashdb';
	require_once($cdir . '/LookupTable.php');
	if (count($argv) != 2) {
		die("usage: php " . $argv[0] . " <sha1>\n");
	}
	$lt = new LookupTable($cdir . '/len6-sha1.idx', $cdir . '/len6.dat', 'sha1');
	$result = $lt->crack($argv[1]);
	if ($result !== false) {
		echo $result[0] . "\n";
	}
?>
