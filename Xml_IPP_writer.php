<?php


class Xml_IPP_writer
{
    private $xw;
    private $counter;//poradnik instrukci

    // po vytvoreni tridy se nastavi citac instrukci na 1
    // a v XMLWriteru se nastavi indentace, kodovani a element program
    public function __construct()
    {
        $this->counter = 1;
        $this->xw = new XMLWriter();

        //nastaveni xmlWriteru
        $this->xw->openMemory();
        $this->xw->setIndent(true);
        $this->xw->setIndentString("  ");//indentace

        //zacatek dokumentu + element program
        $this->xw->startDocument('1.0', 'UTF-8');
        $this->xw->startElement('program');
        $this->xw->startAttribute('language');
        $this->xw->text('IPPcode20');
        $this->xw->endAttribute();
    }

    // ukonceni elementu program a tim padem celeho dokumentu + zapsani na STDOUT
    public function __destruct()
    {
        //konec elementu program
        $this->xw->endElement();
        $this->xw->endDocument();

        //zapsani celeho xml na STDOUT
        echo preg_replace('/(.*)(\')(.*)/', '$1&apos;$3', $this->xw->outputMemory());//XMLWriter neprevadi "'" do specialniho znaku
    }

    // zapsani instrukce a poradi instrukce do XMLWriteru
    public function xml_write($array) {

        //zacatek instrukce
        $this->xw->startElement('instruction');

        //poradi instrukce
        $this->xw->startAttribute('order');
        $this->xw->text($this->counter);
        $this->xw->endAttribute();

        //operacni kod (e.g. MOVE)
        $this->xw->startAttribute('opcode');
        $this->xw->text($array[0]);
        $this->xw->endAttribute();

        //argumenty
        foreach ($array as $k => $value) {
            if ($k < 1) {
                continue;
            }
            //start elementu arg $k
            $this->xw->startElement( 'arg' . $k);
            //typ argumentu (bool, string, type,...)
            $this->xw->startAttribute('type');
            $this->xw->text(substr($value, 0, strpos($value, '@')));
            $this->xw->endAttribute();
            //hodnota argumentu
            $this->xw->text(substr($value, strpos($value, '@') + 1));
            $this->xw->endElement(); //konec elementu arg $k
        }

        //konec instrukce
        $this->xw->endElement();
        $this->counter++;
    }
}
