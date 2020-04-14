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

##
