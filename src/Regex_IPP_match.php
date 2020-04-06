<?php


class Regex_IPP_match
{
    // regularni vyraz pouzivany na kontrolu instrukci
    private $regex;
    // v pripade nalezeni instrukce je do tohoto pole zapsana samotna instrukce a argumenty jejiho operacniho kodu
    public $matches;

    //inicializace regularniho vyrazu(ulozeneho v promenne $regex) pouzivaneho pro vyhodnoceni, zda $text(STDIN) odpovida IPPcode20
    public function __construct()
    {
        $label = '(?:[_\-$&%*!?a-zA-Z]+)';
        $var = '((?:GF|LF|TF)@' . $label . ')';
        $symb = '(?:' . $var . '|(nil@nil|int@[+-]?\d+|bool@(?:true|false)|string@(?:\\\\\d{3}|[^\\\\\s#])*))';

        $frame = '(?i:CREATEFRAME)|(?i:PUSHFRAME)|(?i:POPFRAME)';
        $call_label_jump = '(?i:CALL|LABEL|JUMP)\s+(' . $label . ')';
        $defvar = '(?i:DEFVAR)\s+' . $var;
        $pushs_pops_write_exit_dprint = '(?i:PUSHS|POPS|WRITE|EXIT|DPRINT)\s+' . $symb;
        $add_sub_mul_idiv_lt_gt_eq_and_or_str2int_concat_getchar_setchar = '(?i:ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT|CONCAT|GETCHAR|SETCHAR)\s+' . $var . '\s+' . $symb . '\s+' . $symb;
        $not_int2char_strlen_type_move = '(?i:NOT|INT2CHAR|STRLEN|TYPE|MOVE)\s+' . $var . '\s+' . $symb;
        $jumpifeq_jumpifneq = '(?i:JUMPIFEQ|JUMPIFNEQ)\s+(' . $label . ')\s+' . $symb . '\s+' . $symb;
        $read = '(?i:READ)\s+' . $var . '\s+' . '(bool|int|string)';

        $instruction = $frame . '|' . $defvar . '|' . $call_label_jump . '|' . $pushs_pops_write_exit_dprint .  '|' . $add_sub_mul_idiv_lt_gt_eq_and_or_str2int_concat_getchar_setchar . '|' . $not_int2char_strlen_type_move . '|' . $read . '|'. $jumpifeq_jumpifneq . '|(?i:BREAK)|(?i:RETURN)';
        $comment = '(?:#.*)?';
        $this->regex = '/^\s*(?:' . $instruction . ')?\s*' . $comment . '$/';
    }

    // hledani hlavicky na zacatku
    // argument $text: 1 radek kodu IPPcode20
    // funkce vraci:
    // 0 pokud ji nasla
    // 2 pokud nasla prazdny radek nebo komentar
    // 1 pokud je zde neco jineho
    public function match_header($text)
    {
        if (preg_match('/^\s*\.IPPcode20\s*(#.*)?$/i', $text)) {
            return 0;//hlavicka nalezena
        } else {
            if (preg_match('/(^\s*#.*$)|(^\s*$)/', $text)) {
                return 2;//komentar nebo prazdny radek
            }
            return 1;//neco jineho
        }
    }

    // odstraneni prebytecnych bilych znaku, upraveni pole do XMLWriteru
    // pole $array: pole obsahujici 1 instrukci kodu IPPcode20, nalezenou funkci match_instruction()
    public function ready_array($array){
        $array = array_merge(array_diff($array, array("")));// kvuli preg_match --> nechava prazdne hodnoty v poli

        //odstraneni prazdnych radku a upravi pole tak, aby bylo pripraveno na zapsani pomoci XMLWriteru
        foreach ($array as $k => &$value) {
            //operacni kod
            if($k < 1) {
                $value = preg_replace('/\s*(\w+).*/', '$1', $value);// tato hodnota pole je cela instrukce (e.g. MOVE GF@a GF@b) <-- chci jen operacni kod
                $value = trim($value);
                $value = strtoupper($value);
                continue;
            }
            //argumenty
            if(preg_match('/(GF|LF|TF).*/', $value)) {// jedna se o promenou
                $value = 'var@' . $value;
            }
            if(strpos($value, '@') === false) {// jedna se o typ type (instrukce READ), nebo label
                if(preg_match('/(int|string|bool)/', $value)) {
					$value = 'type@' . $value;
				}
				else {
					$value = 'label@' . $value;
				}
            }
        }
        unset ($value);
        return $array;
    }

    // kontrola radku regularnim vyrazem
    // pokud funkce najde instrukci na danem radku, vypise ji do pole $matches spolu s argumenty
    // $text: jeden radek kodu IPPcode20
    // funkce vraci:
    // 0 pokud se jedna o instrukci jazyka IPPcode20
    // 2 pokud se jedna o samotny komentar nebo prazdny radek
    // 1 pokud je zde neco jineho
    public function match_instruction($text) {
        if(preg_match($this->regex, $text, $this->matches)){
            // je to komentar nebo prazdny radek
            if(preg_match('/(^\s*#.*$)|(^\s*$)/', $this->matches[0])) {
                return 2;
            }
            // je to instrukce
            return 0;
        }
        else {
            // zadna shoda
            return 1;
        }
    }

    // v pripade, ze nejde o instrukci IPPcode20
    // tato funkce urcuje spravny navratovy kod
    // $text: radek s neplatnou instrukci
    // 22 v pripade, ze neni rozpoznan operacni kod
    // 23 v pripade, ze jde o jinou synt. chybu (e.g. spatny pocet argumentu)
    public function return_err_code($text) {
        if(preg_match('/\s*(?i:MOVE|CREATEFRAME|PUSHFRAME|POPFRAME|DEFVAR|CALL|RETURN|PUSHS|POPS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|READ|WRITE|CONCAT|STRLEN|GETCHAR|SETCHAR|TYPE|LABEL|JUMP|JUMPIFEQ|JUMPIFNEQ|EXIT|DPRINT|BREAK)(\s+.*)/', $text)) {
            //jina syntakticka chyba
            return 23;
        }
        else {
            //neznamy operacni kod
            return 22;
        }
    }
}
