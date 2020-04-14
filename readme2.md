# Implementační dokumentace k 2. úloze do IPP 2019/2020
Jméno a příjmení: Michal Sova
Login: xsovam00
## Interpret
Interpret dle parametrů příkazové řádky načte vstup programu, XML reprezentaci programu a program interpretuje a generuje na výstup. Jelikož interpret potřebuje XML reprezentaci programu a vstup programu, musí alespoň 1 z parametrů `--source=`*file* a `--input=`*file* obsahovat soubor s XML reprezentací (parametr `--source`) nebo soubor se vstupem programu (parametr `--input`).
### Implementace
Interpret nejdříve načte a zpracuje celou XML reprezentaci programu, poté zpracuje návěští a nakonec zpracovává jednotlivé instrukce.
Pro zpracování XML reprezentace jsem vytvořil třídu Parse v souboru `XmlParse.py` s funkcí `parse(xml_file)`, která zpracuje soubor *xml_file* a instrukce programu s argumenty seřadí ve vzestupném pořadí do seznamu 'instructions' třídy Parse.
Seznam instrukcí je dále zpracován v samotném `interpret.py`. Zde se nejprve najdou všechny návěští. Poté už se zpracovává instrukce za instrukcí.
U každé instrukce se nejdříve zkontroluje správnost argumentů. Získá se v případě proměnné její hodnota (a typ) provede se daná instrukce.
### Třída Label
Třída Label v souboru `Labels.py` uchovává všechna návěští programu. Navíc uchovává zásobník pořadí instrukcí, na jejímž vrcholu se nachází pořadí instrukce, kam se má program vrátit při provedení instrukce RETURN. Při redefinici návěští (funkce `set_label(self, arg, pos)`) nebo chybějícího návěští (funkce `get_label(name)`) funkce vracejí záporná pořadí.
### Třída Variables
Tato třída uchovává rámce s proměnnými. Dále pomocí funkcí `check(arg, ref)` a `check_none(arg)` kontroluje jednotlivé argumenty instrukcí. Třída obsahuje také zásobník hodnot pro instrukce PUSHS a POPS.
Další významné funkce, které pracují s proměnnými jsou `get_var(var)` - získání hodnoty proměnné, `update_var(var, value)`- aktualizace hodnoty proměnné a `create_var(var)` - vytvoření neinicializované proměnné.
## Testovací skript
Testovací skript automaticky testuje aplikace skriptů `parse.php` a `interpret.py` jazyka IPPcode20. Jména skriptů se dají změnit pomocí parametrů skriptu `--parse-script=`*file* (změna parsovacího skriptu) a `--int-script=`*file* (změna interpretu).
Skript na výstup vygeneruje html s výsledky testů. Neúspěšné testy zobrazí na html stránce a po přejetí zobrazí podrobnější informace. Úspěšné testy se nijak negenerují, jen v dolní části se objeví počet těchto úspěšných testů.
V dolní části html stránky se vygeneruje celkový počet testů, počet úspěšných testů a počet neúspěšných testů.
### Parametry
Parametr `--directory=`*path* určuje cestu, kde jsou testy. Implicitně skript hledá `*.src` soubory v aktuálním adresáři.
Parametr `--jexamxml=`*file* slouží ke změně souboru s JAR balíčkem JExamXML. Implicitní hodnota je ` /pub/courses/ipp/jexamxml/jexamxml.jar`.
Parametry `--int-only` a `--parse-only` nesmí být zadány najednou a určují, zda se bude testovat jen parsovací skript (`--parse-only`), interpret (`--int-only`) nebo oba skripty (bez `--parse-only` ani `--int-only`).
Při použití parametru `--recursive` skript hledá `*.src` soubory i v podsložkách testovací složky.
### Třída Tests
Testovací skript má 1 třídu, která prochází testy a případně doplní prázdné soubory `*.in`, `*.out` a `*.rc` soubor, který bude obsahovat návratový kód '0'. V případě neúspěchu testu vygeneruje část html, oznamující o tomto neúspěšném testu.
