<?php
require_once('Regex_IPP_match.php');
require_once ('Xml_IPP_writer.php');

//TODO: --help or -h (arguments of program)
if(argv[1] === "--help" || argv[1] == -h){
	echo "usage: \$php7.4 parse.php\n";
	echo "program parses code IPPcode20(stdin) to xml(stdout)\n";
	exit(0);
}

$preg = new Regex_IPP_match();
//checking for header
if( !$preg->match_header(fgets(STDIN)) ) {
    //missing header
    fwrite(STDERR,  "missing header\n");
    exit(21);
}

$xml = new Xml_IPP_writer();

while(!feof(STDIN)) {
    $text = fgets(STDIN);
    $match = $preg->match_instruction($text);


    if($match == 0) {
        $preg->matches = $preg->ready_array($preg->matches);
        $xml->xml_write($preg->matches);
    }
    else {

        if($match == 2) { //it is comment or empty line
            continue;
        }
        else { //wrong instruction
            $exit_code = $preg->return_err_code($text);
            fwrite( STDERR, "no match\n");
            exit($exit_code);

        }

    }
}
