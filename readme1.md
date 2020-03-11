# Implementační dokumentace k 1. úloze do IPP 2019/2020
Jméno a příjmení: Michal Sova
Login: xsovam00
## Popis
Skript parse.php zpracovává řádky ze vstupu v kódě IPPcode20. Instrukce ze vstupu analyzuje a v případě validního přepisuje pomocí XMLWriteru na výstup. Skript umožňuje pouze použití argumentů --help nebo -h.
## Implementace
Skript nejprve najde hlavičku na prvním neprázdném řádku (ignoruje komentáře). Hlavičku .IPPcode20 hledá pomocí funkce třídy Regex_IPP_match. Dále zpracovává řádek po řádku vstup, ignoruje prázdné řádky a komentáře. Jednotlivou instrukci pomocí preg_match převede do pole, kde první položka je operační kód a následující položky jsou argumenty. Funkce xml_write třídy Xml_IPP_writer z tohoto pole vypíše příslušnou instrukci do xml třídy a při ukončení programu vše vypíše na výstup. V tomto projektu jsou použity dvě vlastní třídy.
### Třída Xml_IPP_writer
Tato třída při svém vzniku inicializuje xml třídu, kterou si uchovává v proměnné $xw, inicializuje čítač instrukcí a vypíše do xml třídy začátek dokumentu a element program. Pomocí funkce xml_write zapisuje instrukce do xml třídy. Při zániku třídy Xml_IPP_writer se ukončí element program a následně se vypíše celý program IPPcode20 převedený do xml na výstup.
### Třída Regex_IPP_match
Při vytvoření třídy se nastaví regulární výraz, sloužící ke kontrole vstupního kódu. Funkce match_header hledá na daném řádku hlavičku .IPPcode20. Jestliže tato funkce hlavičku najde, řídící skript volá na každý řádek funkci match_instruction, která zapíše do pole $matches instrukci s argumenty. Následně se pomocí ready_array upraví pole $matches tak, aby první položka pole obsahovala operační kód a další položky argumenty.
## Použití
- Zobrazení nápovědy:
`$ php7.4 parse.php --help`
- Spuštění skriptu nad nějakým souborem:
`$ php7.4 parse.php <file.src`
