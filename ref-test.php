<?php
/**
 *
 * @file    test.php
 * @author	Filip Kocica <xkocic01@stud.fit.vutbr.cz>
 * @date    17/2/2018
 *
 * IPP project 1
 *
 */

/** Test counters */
$test_counter = 1;
$testPassed = 0;
$testFailed = 0;
		
/** Runs the arguments check and extract + runs the test on default or input directory
    if some function throws error we may catch them and write error to stderr + return correct error code */
try
{
	CArguments::parseArgs($argv);
	if(CArguments::$help)
	{
		display_help();
		die(0);
	}

	echo "<!DOCTYPE HTML>";
	echo "<html>";
	echo "<head>";
		echo "<meta charset=\"utf-8\">";
		echo "<meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\">";
		echo "<title>IPP project</title>";
	echo "</head>";
	echo "<body>";

	echo "<font size=\"3\" color=\"blue\">IPP project -- test.php -- Filip Kocica [xkocic01@fit.vutbr.cz]</font>";
	CTests::runTests(CArguments::$dir);
	
	echo "<br><br><br>Summary: <br>------------<br>";
	$test_counter--;
	echo "<font size=\"2\" color=\"black\">Tests total: " . $test_counter . "</font><br>";
	echo "<font size=\"2\" color=\"black\">Tests passed: " . $testPassed . "</font><br>";
	echo "<font size=\"2\" color=\"black\">Tests failed: " . $testFailed . "</font><br>";
	
	echo "</body>";
	echo "</html>";
}
catch(CRuntimeErrEx $e)
{
	$e->what();
	die($e->ec);
}


/** Runs tests and saves data */
class CTests
{
	public static function runTests($dir)
	{
		$dirHandle = opendir($dir);
		
		while($file = readdir($dirHandle))
		{
			if(is_dir($dir . "/" . $file) && $file !== '.' && $file !== '..')
			{
				if (CArguments::$recurs)
				{
					self::runTests($dir . "/" . $file);
				}
			}
			else if ($file === '.' && $file === '..')
			{
				// Skip
			}
			else
			{
				$ext = pathinfo($file, PATHINFO_EXTENSION);
				$filename = basename($file, $ext);
				
				if ($ext === 'src')
				{
					self::runTest($dir, $filename);
				}
			}
		}
	}
	
	public static function runTest($dir, $filename)
	{
		global $test_counter;
		global $testFailed;
		global $testPassed;
		
		$in = FALSE;
		$out = FALSE;
		$rc = FALSE;
		
		$dirHandle = opendir($dir);
		while($file = readdir($dirHandle))
		{
			if(is_dir($dir . "/" . $file) && $file !== '.' && $file !== '..')
			{
				// Skip
			}
			else if ($file === '.' && $file === '..')
			{
				// Skip
			}
			else
			{
				$ext = pathinfo($file, PATHINFO_EXTENSION);
				$fn = basename($file, $ext);
				
				if ($filename === $fn AND $ext === 'in')
				{
					$in = TRUE;
				}
				elseif ($filename === $fn AND $ext === 'out')
				{
					$out = TRUE;
				}
				elseif ($filename === $fn AND $ext === 'rc')
				{
					$rc = TRUE;
				}
			}
		}
		
		echo "<br><br><br><font size=\"2\" color=\"black\">Test #" . $test_counter . " (Path: " . $dir . "/" . $filename . ")</font><br>";
		$test_counter++;
		
		if ($in === FALSE)
		{
			shell_exec('touch ' . $dir . "/" . $filename . 'in');
		}
		if ($out === FALSE)
		{
			shell_exec('touch ' . $dir . "/" . $filename . 'out');
		}
		if ($rc === FALSE)
		{
			shell_exec('touch ' . $dir . "/" . $filename . 'rc');
			shell_exec('echo "0" >> ' . $dir . "/" . $filename . 'rc');
		}
		
		shell_exec('touch ./tempf1');
		shell_exec('touch ./tempf2');

		exec('php5.6 ' . CArguments::$parse_scrpt . ' < ' . $dir . "/" . $filename . 'src > ./tempf1', $wth, $rc);

		$testRC = exec('cat ' . $dir . "/" . $filename . 'rc');

		if ($rc !== 0)
		{
			if ($testRC !== (string)$rc)
			{
				echo "<font size=\"2\" color=\"red\">FAIL: Return codes of parse.php and .rc file doesnt match. Is: " . (string)$rc . " (Expected: " . $testRC . ")</font><br>";
				$testFailed++;
				shell_exec('rm -rf ./tempf1');
				shell_exec('rm -rf ./tempf2');
				return;
			}
		}
		
		exec('python3.6 ' . CArguments::$int_scrpt . ' --source=./tempf1 < ' . $dir . "/" . $filename . 'in > ./tempf2', $wth, $rc);

		if ($testRC !== (string)$rc)
		{
			echo "<font size=\"2\" color=\"red\">FAIL: Return codes of interpret.py and .rc file doesnt match. Is: " . (string)$rc . " (Expected: " . $testRC . ")</font><br>";
			$testFailed++;
			shell_exec('rm -rf ./tempf1');
			shell_exec('rm -rf ./tempf2');
			return;
		}
		
		if ($rc === 0)
		{
			exec('diff ./tempf2 ' . $dir . "/" . $filename . 'out', $wth, $rc);
			if (empty($wth))
			{
				echo "<font size=\"2\" color=\"red\">FAIL: Output from interpret.py and .out doesnt match</font><br>";
				$testFailed++;
				shell_exec('rm -rf ./tempf1');
				shell_exec('rm -rf ./tempf2');
				return;
			}
		}
		
		shell_exec('rm -rf ./tempf1');
		shell_exec('rm -rf ./tempf2');

		echo "<font size=\"2\" color=\"green\">OK</font><br>";
		$testPassed++;
	}
}
 
/** Class which checks arguments validity and extracts important data from them saving to member variables */
class CArguments
{
	static $help = FALSE;
	static $recurs = FALSE;
	
	static $dir_set = FALSE;
	static $parse_scrpt_set = FALSE;
	static $int_scrpt_set = FALSE;
	
	static $dir;
	static $parse_scrpt;
	static $int_scrpt;
	

	public static function parseArgs(array $argv)
	{
		unset($argv[0]);
		
		foreach($argv as $arg)
		{
			if($arg === '--help')
			{
				if(self::$help)
				{
					throw new CRuntimeErrEx("Wrong input args.", 10);
				}
				self::$help = TRUE;
			}
			elseif($arg === '--recursive')
			{
				if(self::$recurs)
				{
					throw new CRuntimeErrEx("Wrong input args.", 10);
				}
				self::$recurs = TRUE;
			}
			elseif(substr($arg, 0, 15) === '--parse-script=')
			{
				if(self::$parse_scrpt_set)
				{
					throw new CRuntimeErrEx("Wrong input args.", 10);
				}
				self::$parse_scrpt_set = TRUE;
				self::$parse_scrpt = substr($arg, 15);
			}
			elseif(substr($arg, 0, 13) === '--int-script=')
			{
				if(self::$int_scrpt_set)
				{
					throw new CRuntimeErrEx("Wrong input args.", 10);
				}
				self::$int_scrpt_set = TRUE;
				self::$int_scrpt = substr($arg, 13);
			}
			elseif(substr($arg, 0, 12) === '--directory=')
			{
				if(self::$dir_set)
				{
					throw new CRuntimeErrEx("Wrong input args.", 10);
				}
				self::$dir_set = TRUE;
				self::$dir = substr($arg, 12);
			}
			else
			{
				throw new CRuntimeErrEx("Wrong input args.", 10);
			}
		}
		
		if (self::$help AND (self::$recurs OR self::$dir_set OR self::$parse_scrpt_set OR self::$int_scrpt_set))
		{
			throw new CRuntimeErrEx("Wrong input args.", 10);
		}
		if (self::$dir_set === FALSE)
		{
			self::$dir = getcwd();
		}
		if (self::$int_scrpt_set === FALSE)
		{
			self::$int_scrpt = getcwd();
			self::$int_scrpt .= '/interpret.py';
		}
		if (self::$parse_scrpt_set === FALSE)
		{
			self::$parse_scrpt = getcwd();
			self::$parse_scrpt .= '/parse.php';
		}
	}
}



/** Exception derived from standard exception containing error message and error code */
class CRuntimeErrEx extends Exception
{
	public $ec;
	public $msg;
	public function __construct($msg, $ec)
	{
		$this->msg = $msg;
		$this->ec = $ec;
	}
	public function what()
	{
		fwrite(STDERR, "Runtime error: " . $this->msg . " Exit code = " . $this->ec . ".\n");
	}
}

/** Function which prints help to stdout */
function display_help()
{
	echo "  php5.6 test.php [--help] [--recursive] [--parse-script=] [--int-script=] [--directory=]\n";
	echo "     --help     		- Zobrazi napovedu\n";
	echo "     --recursive      - Recursivni prohledavani adresaru\n";
	echo "     --parse-script   - Parsovaci script, defaultne parse.php\n";
	echo "     --int-script     - Interpretovaci script, defaultne interpret.py\n";
	echo "     --directory      - Kde ma hledat testy, defaultne aktualni adresar\n";
}
?>
