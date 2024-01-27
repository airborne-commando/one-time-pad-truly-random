<?php
/**
 * Run a test of the oneTimePad class.
 *
 * The oneTimePad class is defined in the ./one-time-pad.php file and has a series of methods that are designed to
 * show you how the One Time Pad encryption cipher works.  One Time Pad is also known variously as either the Vernam
 * Cipher or the Perfect Cipher, owing to its mathematically unbreakable encryption (if implemented correctly).
 *
 * @author Michael Hall <mike@unrivaledcreations.com>
 * @license UNLICENSE
 * @version 1.0
 */

use unrivaled\OneTimePad\OneTimePadModulo26\OneTimePadModulo26;

require __DIR__ . '/src/OneTimePadModulo26.php';

// Check if the --help argument is provided
if (in_array('--help', $argv) || in_array('-h', $argv)) {
    echo "Usage: php script.php [--help]\n";
    echo "--help -h:   Display this help message.\n";
    exit;
}

$cipher = new OneTimePadModulo26;

// Check if user input is provided as a command-line argument
if ($argc > 1) {
    // Get user input from the command line argument
    $userInput = strtoupper($argv[1]);

    // Save user input to plaintext.txt
    file_put_contents('./text/plaintext.txt', $userInput);
}

// Generate random values for the number of times to run the script
$die1 = random_int(0, 5);
$die2 = random_int(0, 5);

echo "Result of Die 1: $die1\n";
echo "Result of Die 2: $die2\n";

// Calculate the total number of times to run the script
$total = $die1 + $die2;
echo "Total: $total\n";

// Loop to run the script $total times
for ($i = 0; $i < $total; $i++) {
    // Generate random plain text and cipher key using the shell script
    $plainText = shell_exec('./letters.sh'); // 256 random letters
    $cipherKey = shell_exec('./letters.sh'); // 256 random letters

    // For demonstration purposes, let's just use these text files as the source of our message and cipher keys.
    $plainText = preg_replace('/[^A-Z]/', '', strtoupper(file_get_contents('./text/plaintext.txt')));
    $cipherKey = preg_replace('/[^A-Z]/', '', strtoupper(file_get_contents('./text/cipherkey.txt')));

    // For demonstration purposes, let's just print the random plain text and cipher key
    echo "Random Plain Text: $plainText\n";
    echo "Random Cipher Key: $cipherKey\n";
    echo str_repeat('-', 50) . "\n";
}

// Encrypt and then immediately decrypt the plain text message to test the one-time pad.
if (
    (false === $cipherText = $cipher->encrypt($cipherKey, $plainText)) ||
    (false === $decodedPlainText = $cipher->decrypt($cipherKey, $cipherText))
) {
    echo('For perfect encryption in the one-time pad, the key length must be equal to, or greater than, the message length.');
}

file_put_contents('./text/ciphertext.txt', $cipher->tty($cipherText));

// Displays a "vigenere table," also known as a "tabula recta."
echo $cipher->get_vigenere_table();

// Displays the plain text message, the one-time pad cipher key, and the resulting safe-to-transmit cipher text.
$messageLength = strlen($plainText);
$cipherKeyUsed = substr($cipherKey, 0, $messageLength);

echo 'Plain:  ' . $cipher->tty($plainText) . " (message)\n";
echo 'Key:    ' . $cipher->tty($cipherKeyUsed) . " (secret)\n";
echo '        ' . $cipher->tty(str_repeat('-', $messageLength)) . "\n";
echo 'Cipher: ' . $cipher->tty($cipherText) . " (cipher)\n";

// Clear the screen after the script finishes
if (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN') {
    // For Windows
    system('cls');
} else {
    // For Unix-like systems
    system('clear');
}
