<?php
require_once('src/Tests.php');
$dir_name = '.';
$tests = new Tests();
$longopts = array(
    "directory:",
    "recursive",
    "help",
    "parse-script:",
    "int-script:",
    "parse-only",
    "int-only",
    "jexamxml:"
);
if ($opts = getopt('', $longopts)){
    if (array_key_exists('help', $opts)){

        if (sizeof($opts) > 1){
            exit(10);
        }
        else{
            echo "Testovací skript pro automatické testování postupné aplikace parse.php a interpret.py.\n";
            echo "Tento skript pracuje s těmito paramety:\n";
            echo "     --help               - Zobrazí nápovědu\n";
            echo "     --directory=path     - Adresář, kde má hledat testy, implicitně aktuální adresář\n";
            echo "     --recursive          - Rekurzivní prohledávání adresářů\n";
            echo "     --parse-script=file  - Parsovací skript, implicitní hodnota: parse.php\n";
            echo "     --int-script=file    - Interpretovací skript, implicitní hodnota: interpret.py\n";
            echo "     --parse-only         - Testován bude pouze parsovací skript\n";
            echo "     --int-only           - Testován bude pouze interpretovací skript\n";
            echo "     --jexamxml=file      - soubor s JAR balíčkem JExamXML, imlicitní hodnota: /pub/courses/ipp/jexamxml/jexamxml.jar\n";
            exit(0);
        }
    }
    if (array_key_exists('directory', $opts)){
        $dir_name = $opts['directory'];
        if (!is_dir($dir_name)){
            exit(11);
        }
    }
    if (array_key_exists('parse-only', $opts)){
        if(array_key_exists('int-only', $opts) || array_key_exists('int-script', $opts)){
            exit(10);
        }
        $tests->parse_only = true;
    }
    else if (array_key_exists('int-only', $opts)){
        if(array_key_exists('parse-script', $opts)){
            exit(10);
        }
        $tests->int_only = true;
    }
    if (array_key_exists('recursive', $opts)){
        $tests->recursive = true;
    }
    if (array_key_exists('jexamxml', $opts)){
        $tests->jexam = $opts['jexamxml'];
        if (!file_exists($tests->jexam)){
            exit(11);
        }
    }
    if (array_key_exists('parse-script', $opts)){
        $tests->parse_script = $opts['parse-script'];
        if (!file_exists($tests->parse_script)){
            exit(11);
        }
    }
    if (array_key_exists('int-script', $opts)){
        $tests->int_script = $opts['int-script'];
        if (!file_exists($tests->int_script)){
            exit(11);
        }
    }
}
echo "<!DOCTYPE HTML>\n";
echo "<html lang=\"cs\">\n";
echo "<head>\n";
echo "<meta charset=\"utf-8\">\n";
echo "<title>Výsledek testovacího skriptu pro IPPcode20</title>\n";
echo "</head>\n";

echo "<body style='overflow: auto;'>\n";
echo "<h1 style='margin: auto;margin-bottom: 20px;'>Výsledky test.php </h1>\n";
echo "<h2 style='margin: auto;margin-bottom: 20px;'>Michal Sova (xsovam00@stud.fit.vutbr.cz)</h2>\n";
echo "<div style='overflow: auto;width: 90vw;margin: auto;height: 80vh;'>\n";
$tests->runTests($dir_name);
echo "</div>\n";
echo "<div style='display: inline;top: 0;'>\n";
echo "<h3 style='float: left;margin-right: 20px'>Total: " . $tests->test_counter . "</ps>\n";
echo "<h3 style='float: left;margin-right: 20px'>Passed: " . $tests->passed . "</h3>\n";
echo "<h3 style='float: left;margin-right: 20px'>Failed: " . $tests->failed . "</h3>\n";
echo "</div>\n";
echo "</body>\n";
echo "</html>\n";




