<?php


class Regex_IPP_match
{
    private $regex;
    public $matches;

    //initialization of regular expression used for comparison input string($text)
    public function __construct()
    {
        $label = '(?:[_\-$&%*!?a-zA-Z]+)';
        $var = '((?:GF|LF|TF)@' . $label . ')';
        $symb = '(?:' . $var . '|(nil@nil|int@[+-]?\d+|bool@(?:true|false)|string@(?:\\\\\d{3}|[^\\\\\s#])*))';

        $frame = '(?i:CREATEFRAME)|(?i:PUSHFRAME)|(?i:POPFRAME)';
        $call_label_jump = '(?i:CALL|LABEL|JUMP)\s+(' . $label . ')';
        $defvar = '(?i:DEFVAR)\s+' . $var;
        $pushs_pops_write_exit_dprint = '(?i:PUSHS|POPS|WRITE|EXIT|DPRINT)\s+' . $symb;
        $add_sub_mul_idiv_lt_gt_eq_and_or_str2int_concat_getchar_setchar = '(?i:ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STR2INT|CONCAT|GETCHAR|SETCHAR)\s+' . $var . '\s+' . $symb . '\s+' . $symb;
        $not_int2char_strlen_type_move = '(?i:NOT|INT2CHAR|STRLEN|TYPE|MOVE)\s+' . $var . '\s+' . $symb;
        $jumpifeq_jumpifneq = '(?i:JUMPIFEQ|JUMPIFNEQ)\s+(' . $label . ')\s+' . $symb . '\s+' . $symb;
        $read = '(?i:READ)\s+' . $var . '\s+' . '(bool|int|string|nil)';

        $instruction = $frame . '|' . $defvar . '|' . $call_label_jump . '|' . $pushs_pops_write_exit_dprint .  '|' . $add_sub_mul_idiv_lt_gt_eq_and_or_str2int_concat_getchar_setchar . '|' . $not_int2char_strlen_type_move . '|' . $read . '|'. $jumpifeq_jumpifneq . '|(?i:BREAK)|(?i:RETURN)';
        $comment = '(?:#.*)?';
        $this->regex = '/^\s*(?:' . $instruction . ')?\s*' . $comment . '$/';
    }
    public function match_header($text){
        if(preg_match('/^\s*\.IPPcode20\s*(#.*)?$/i', $text)) {
			return 0;//matches header

        }
        else {
            if(preg_match('/(^\s*#.*$)|(^\s*$)/', $text)){
				return 2;//matches comment at the beginning(or empty line)
			}
			return 1;//not any match
        }
    }
    public function ready_array($array){
        $array = array_merge(array_diff($array, array("")));
        foreach ($array as $k => &$value) {
            if($k < 1) {

                $value = preg_replace('/\s*(\w+).*/', '$1', $value);
                $value = trim($value);
                $value = strtoupper($value);
                continue;
            }
            if(preg_match('/(GF|LF|TF).*/', $value)) {
                $value = 'var@' . $value;
            }
            if(strpos($value, '@') === false) {
                $value = 'type@' . $value;
            }
        }
        unset ($value);
        return $array;
    }
    public function match_instruction($text) {
        if(preg_match($this->regex, $text, $this->matches)){
            //comment or next line
            if(preg_match('/(^\s*#.*$)|(^\s*$)/', $this->matches[0])) {
                return 2;
            }
            //everythink is OK
            return 0;
        }
        else {
            //no match
            return 1;
        }
    }

    public function return_err_code($text) {
        if(preg_match('/\s*(?i:MOVE|CREATEFRAME|PUSHFRAME|POPFRAME|DEFVAR|CALL|RETURN|PUSHS|POPS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|READ|WRITE|CONCAT|STRLEN|GETCHAR|SETCHAR|TYPE|LABEL|JUMP|JUMPIFEQ|JUMPIFNEQ|EXIT|DPRINT|BREAK)(\s+.*)|(\s*$)/', $text)) {
            //unknown opcode or wrong opcode
            return 23;
        }
        else {
            //another synt. error
            return 22;
        }
    }
}
