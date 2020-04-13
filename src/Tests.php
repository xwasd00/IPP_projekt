<?php
class Tests
{
    public $parse_script = 'parse.php';
    public $int_script = 'interpret.py';
    public $jexam = '/pub/courses/ipp/jexamxml/jexamxml.jar';
    public $recursive = false;
    public $parse_only = false;
    public $int_only = false;
    public $test_counter = 0;
    public $passed = 0;
    public $failed = 0;

    public function runTests($dir_name){
        $dir = opendir($dir_name);
        while(($file = readdir($dir)) !== false){
            if(is_dir($dir_name . '/' . $file) && $file !== '.' && $file !== '..'){
                if ($this->recursive) {
                    $this->runTests($dir_name . '/' . $file);
                }
            }
            else if($file === '.' || $file === '..'){

            }
            else {
                $ext = pathinfo($file, PATHINFO_EXTENSION);
                if($ext === 'src') {
                    $filename = basename($file, $ext);
                    if(!file_exists($dir_name . '/' . $filename . 'out')){
                        exec('touch '. $dir_name . '/' . $filename . 'out');
                    }
                    if(!file_exists($dir_name . '/' . $filename . 'in')){
                        exec('touch '. $dir_name . '/' . $filename . 'in');
                    }
                    if(!file_exists($dir_name . '/' . $filename . 'rc')){
                        exec('echo "0" >'. $dir_name . '/' . $filename . 'rc');
                    }
                    if ($this->parse_only) {
                        $this->test_parse($dir_name . '/' . $filename);
                    } else if ($this->int_only) {
                        $this->test_int($dir_name . '/' . $filename);
                    } else {
                        $this->test_both($dir_name . '/' . $filename);
                    }
                }
            }
        }
    }
    private function test_parse($file){
        exec('php ' . $this->parse_script . ' <' . $file . 'src >tmpf', $output,$ret);
        exec('cat ' . $file . 'rc', $rc);
        exec('java -jar /pub/courses/ipp/jexamxml/jexamxml.jar ' . $file . 'out tmpf diffs.xml', $diff_out, $diff_ret);
        $rc = $rc[0];
        if ($rc == $ret && $ret !=0) {
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else if ($rc == $ret && $diff_ret == 0){
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else{
            echo "<p style='color:red' title='";
            echo "navratove kody: ";
            echo "interpret: $ret, ref: $rc&#xA;&#xA;";
            echo file_get_contents('diffs.xml') . "'>";
            echo $file . "src: FAILED";
            echo "</p>\n";
            $this->failed++;
        }
        exec('rm tmpf diffs.xml');
        $this->test_counter++;
    }
    private function test_int($file){
        exec('python3 ' . $this->int_script . ' --input=' . $file . 'in --source=' . $file . 'src >tmpf', $output,$ret);
        exec('cat ' . $file . 'rc', $rc);
        exec('diff ' . $file . 'out tmpf', $diff_out, $diff_ret);
        $rc = $rc[0];
        if ($rc == $ret && $ret != 0) {
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else if($rc == $ret && $diff_ret == 0){
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else{
            echo "<p style='color:red' title='";
            echo "navratove kody: ";
            echo "interpret: $ret, ref: $rc&#xA;&#xA;";
            foreach ($diff_out as $line){
                echo $line . "&#xA;";
            }
            echo "'>";
            echo $file . "src: FAILED";
            echo "</p>\n";
            $this->failed++;
        }
        exec('rm tmpf');
        $this->test_counter++;
    }
    private function test_both($file){
        //echo "<p>$file</p>\n";
        exec('php ' . $this->parse_script . ' <' . $file . 'src | python3 ' . $this->int_script . ' --input=' . $file . 'in >tmpf', $output,$ret);
        exec('cat ' . $file . 'rc', $rc);
        exec('diff ' . $file . 'out tmpf', $diff_out, $diff_ret);
        $rc = $rc[0];
        if ($rc == $ret && $ret != 0) {
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else if($rc == $ret && $diff_ret == 0){
            echo "<p style='color:green'>";
            echo $file . "src: OK";
            echo "</p>\n";
            $this->passed++;
        }
        else{
            echo "<p style='color:red' title='";
            echo "navratove kody: ";
            echo "interpret: $ret, ref: $rc&#xA;&#xA;";
            foreach ($diff_out as $line){
                echo $line . "&#xA;";
            }
            echo "'>";
            echo $file . "src: FAILED";
            echo "</p>\n";
            $this->failed++;
        }
        exec('rm tmpf');
        $this->test_counter++;
    }
}