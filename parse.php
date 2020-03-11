<?php
require_once('Regex_IPP_match.php');
require_once ('Xml_IPP_writer.php');
ini_set('display_errors', 'stderr');

// zobrazeni napovedy
if($argc > 1) {
	if($argv[1] === "--help" || $argv[1] === "-h") {
	echo "Skript typu filtr (v jazyce PHP 7.4) načte ze standardního vstupu zdrojový kód v IPPcode20, zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standardní
výstup XML reprezentaci programu dle specifikace kódu.\n";
	echo "Použití: \$php7.4 parse.php <file.in >file.out\n";
    exit(0);
	}
	else {
	    // zadne jine argumenty nejsou podporovany
		exit(10);
	}
}

$preg = new Regex_IPP_match();
// kontrola hlavicky
while(!feof(STDIN)) {
	$text = fgets(STDIN);
	$header = $preg->match_header($text);
	if($header == 0) {
		break;// hlavicka nalezena
	}
	if($header == 1) {
    	exit(21);// hlavicka chybi (je tam napriklad uz instrukce)
	}
	// prazdny radek nebo komentar -> pokracuj v hledani hlavicky
}

$xml = new Xml_IPP_writer();
while(!feof(STDIN)) {
    // nacteni radku
    $text = fgets(STDIN);

    // kontrola instrukce
    $match = $preg->match_instruction($text);
    if($match == 0) {// instrukce nalezena -> uprava pole + zapsani do XMLWriteru
        $preg->matches = $preg->ready_array($preg->matches);
        $xml->xml_write($preg->matches);
    }
    else {// instrukce nenalezena -> muze jit o komentar nebo prazdny radek
        if($match == 2) {// prazdny radek nebo (jen) komentar na radku
            continue;
        }
        else {// spatna instrukce
            $exit_code = $preg->return_err_code($text);
            exit($exit_code);
        }
    }
}
