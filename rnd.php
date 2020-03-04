<?php
while (!feof(STDIN)) {
    $text = fgets(STDIN);

    preg_match('/string@(?:\\\\\d{3})*/', $text, $array);
    var_dump($array);
}