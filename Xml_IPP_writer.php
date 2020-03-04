<?php


class Xml_IPP_writer
{
    private $xw;
    private $counter;

    public function __construct()
    {
        $this->counter = 1;
        $this->xw = xmlwriter_open_memory();
        xmlwriter_set_indent($this->xw, 1);
        $res = xmlwriter_set_indent_string($this->xw, '    ');
        xmlwriter_start_document($this->xw, '1.0', 'UTF-8');
        xmlwriter_start_element($this->xw, 'program');
        xmlwriter_start_attribute($this->xw, 'language');
        xmlwriter_text($this->xw, 'IPPcode20');
        xmlwriter_end_attribute($this->xw);

    }
    public function __destruct()
    {

        xmlwriter_end_element($this->xw);//program
        xmlwriter_end_document($this->xw);
        echo xmlwriter_output_memory($this->xw);
    }

    public function xml_write($array) {

        //instruction element
        xmlwriter_start_element($this->xw, 'instruction');
        //attributes of instruction element
        xmlwriter_start_attribute($this->xw, 'order');
        xmlwriter_text($this->xw, $this->counter);
        xmlwriter_end_attribute($this->xw);
        xmlwriter_start_attribute($this->xw, 'opcode');
        xmlwriter_text($this->xw, $array[0]);
        xmlwriter_end_attribute($this->xw);

        foreach ($array as $k => $value) {
            if ($k < 1) {
                continue;
            }
            //child element(arg[$k])
            xmlwriter_start_element($this->xw, 'arg' . $k);
            xmlwriter_start_attribute($this->xw, 'type');
            xmlwriter_text($this->xw, substr($value, 0, strpos($value, '@')));
            xmlwriter_end_attribute($this->xw);
            xmlwriter_text($this->xw, substr($value, strpos($value, '@') + 1));
            xmlwriter_end_element($this->xw); //arg[$k]
        }

        xmlwriter_end_element($this->xw); // instruction
        echo xmlwriter_output_memory($this->xw);
        $this->counter++;
    }


}
