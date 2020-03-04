<?php
require_once('Regex_IPP_match.php');
require_once ('Xml_IPP_writer.php');

//TODO: --help or -h, --stats, --loc,... (getopt??)
if($argc > 1) {
	if($argv[1] === "--help" || $argv[1] === "-h") {
	echo "Script of type filter (parse.php in PHP 7.4 programming language) reads from standard input source code IPP-
code20, checks syntactic and lexical correctness of the code and prints on standard output XML representation of the code.\n";
	echo "usage: \$php7.4 parse.php <file.in >file.out\n";
    exit(0);
	}
	else {
		exit(10);
	}
}

$preg = new Regex_IPP_match();

//checking for header
while(!feof(STDIN)) {
	$text = fgets(STDIN);
	$header = $preg->match_header($text);
	if($header == 0) {
		break;//matches header
	}
	if($header == 1) {
    	exit(21);//missing header
	}
	//else -> comment or empty line -> continue matching header
}

$xml = new Xml_IPP_writer();

while(!feof(STDIN)) {
    //read line
    $text = fgets(STDIN);

    //check for instruction
    $match = $preg->match_instruction($text);
    if($match == 0) {// match -> edit array and write XML representation to STDOUT
        $preg->matches = $preg->ready_array($preg->matches);
        $xml->xml_write($preg->matches);
    }
    else {
        if($match == 2) {// it is comment or empty line
            continue;
        }
        else {//wrong instruction
            $exit_code = $preg->return_err_code($text);
            exit($exit_code);
        }

    }
}
