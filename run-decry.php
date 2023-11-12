<?php

use unrivaled\OneTimePad\OneTimePadModulo26\OneTimePadModulo26;

require __DIR__ . '/src/OneTimePadModulo26.php';

function decryptWithKeyFromFile($ciphertextFile, $keyFile)
{
    $cipherText = file_get_contents($ciphertextFile);
    $key = file_get_contents($keyFile);

    decryptWithKey($cipherText, $key);
}

function decryptWithKey($cipherText, $key)
{
    $cipher = new OneTimePadModulo26;

    // Clean up the input
    $cipherText = preg_replace('/[^A-Z]/', '', strtoupper($cipherText));
    $key = preg_replace('/[^A-Z]/', '', strtoupper($key));

    // Ensure the key is long enough
    if (strlen($key) < strlen($cipherText)) {
        echo "Error: The key must be at least as long as the ciphertext.\n";
        return;
    }

    $decryptedText = '';

    // Decrypt each character
    for ($i = 0; $i < strlen($cipherText); $i++) {
        $cipherChar = ord($cipherText[$i]) - ord('A');
        $keyChar = ord($key[$i % strlen($key)]) - ord('A');

        // Decrypt the character
        $decryptedChar = chr((26 + $cipherChar - $keyChar) % 26 + ord('A'));
        $decryptedText .= $decryptedChar;
    }

    // Output the results
    // echo 'Cipher:     ' . implode(' ', str_split($cipher->tty($cipherText))) . " (cipher)\n";
    // echo 'Key:        ' . implode(' ', str_split($cipher->tty($key))) . " (key)\n";
    echo '            ' . implode(' ', str_split(str_repeat('-', strlen($cipherText)))) . "\n";
    echo 'Decrypted:  ' . implode(' ', str_split($cipher->tty($decryptedText))) . " (decrypted)\n";
}

// Given filenames for ciphertext and a key
$ciphertextFile = "./text/ciphertext.txt";
$keyFile = "./text/cipherkey.txt";

decryptWithKeyFromFile($ciphertextFile, $keyFile);
