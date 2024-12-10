# "One Time Pad" (OTP)
##### _The only known encryption which is mathematically unbreakable._

### CHANGES:
* Added in `run.py` with the arguments Use 'encrypt file <file_path>', 'encrypt text <your_text>', or 'decrypt' as arguments.
* Add in flask, to run set up a python virtual environment and install flask; then run app.py
* Added in a help option `-/?` for the user to see a list of commands

## Perfect Encryption
**One Time Pad**, variously known as the **Vernam Cipher** and the **Perfect Cipher**, is the only existing encryption which is mathematically unbreakable.  And it was born in the late 1800's.

This mini-project was inspired by the article by Dirk Rijmenants and posted on his website under the title, ["One-time Pad."](http://users.telenet.be/d.rijmenants/en/onetimepad.htm)

In short, the one time pad is unbreakable if:
1. The cipher key is at least as long as the message text.
2. The cipher key is _truly random_.
3. The cipher key is _never re-used_ and _never repeated_.
4. ["Modular arithmetic"](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic) is used to compute the cipher text.  
5. The cipher key is destroyed by both parties after use.  _(This is where the term &ldquo;one time pad&rdquo; originates from; note pads have pages of cipher keys written on them, which are torn out and destroyed after being used only once.)_

## Setup Instructions

### Installation

Clone or download the files into a machine with PHP from the github repository.

### Running the Demonstration Script

1. Enter the source root directory from the shell (`cd /path/to/repository`).
2. you will also need to define an agrunment before running Use 'file <file_path>' or 'text <your_text>' as arguments. 

IE `python run.py 'encrypt file <file_path>'` or `python run.py encrypt text <your_text>`

You also have an option to scramble the ciphertext; to add a layer of security.

### Running the dcryption tool

1. Enter the source root directory from the shell (`cd /path/to/repository`).
2. edit the cipherkey.txt and ciphertext.txt (secret)
3. Do `python run.py decrypt` from the command line.
4. It should run the decryption correctly.

### Brute force tool
For those with a scrambled key there are two ways of solving this:
- Brute Force
- Manual intervention

With a scrambled ciphertext however this will take forever to solve.

With the brute force tool you'll need to install the following:

    pip3 install transformers torch

This will require a nvidia card however, otherweise you'll run on CPU; will also have to tell you this requires at least 8GB vram and uses the gpt2 model for lang.

Example
cipherkey.txt:
```
Key:    H I W O U   Z K E K C   Q R R T N   J W T E R   M P Z B (secret)
```
```
hiwouzkekcqrrtnjwtermpzbxbgujdhhoubqwmcqizqfetffqlwlrxzullyicvr
```
ciphertext.txt
```
Cipher: L D A F S   F Y S N D   E P U X F   N N O I J   R D N E (cipher)
```
```
LDAFS FYSND EPUXF NNOIJ RDNE
```

To decrypt a message provided you have the right ciphertext.


## About the Demonstration Script and Files

### What It Does

`python run.py` loads the cipher key from the file `/text/cipherkey.txt`; loads the plain text from the file `/text/plaintext.txt`; performs a modulo 26 (alphabetic) one time pad using those loaded values; and then saves the result to `/text/ciphertext.txt`. It also displays a Vigenere table, sometimes called the "tabula recta," to the screen with the plain text, cipher key and cipher text immediately below it for your study.

This is a PHP script written to run from the command line strictly to demonstrate the mathemetics behind the one time pad; namely, the modulo 26 method.  Modulo 10 (numerals) and modulo 2 (binary) also work; but this demonstration is for modulo 26.

### File Structure

| File Name | File Description |
| --- | --- |
| `./run.py` | The script on which you can encrypt/decrypt your text/console input output. |
| `./brtfrce.py` | This script will attempt to brute force a scrambled ciphertext, as long as you have a valid key pair. |
| `/text/cipherkey.txt`  | This file contains the cipher key:  A random sequence of alphabetic characters in uppercase, from A through Z. _This file is replaced every time the script is run._   |
| `/text/ciphertext.txt`  | This file contains output from the script showing the encrypted message.  _This file is replaced every time the script is run._  |
| `/text/plaintext.txt`  | The source (unencrypted, plain text) message. _This file is replaced every time the script is run._   |
| `/text/vigenere-*.txt`  | The Vigenere table, also known as the &ldquo;tabula recta,&rdquo; in monospace text in case you want to try doing the one time pad by hand or simply to study.  |

## About the One Time Pad

[Dirk Rijmenants&rsquo; article about the one time pad](http://users.telenet.be/d.rijmenants/en/onetimepad.htm) is an excellent resource to learn more about the history and mathematics behind the 135-year-old encryption algorithm that is mathematically unbreakable to this very day.  This article is filled with intrigue, history and the mathematics behind the one time pad.

### Key and Message Length
The one time pad uses a unique one letter cipher key for each letter in the message, so the encryption key as a whole must be at least as long as the message itself. One could conceivably re-use an encryption key in a round robin fashion (going back to the first element of the key after reaching the end), but this creates a &ldquo;pattern&rdquo; which is easily spotted by cryptographers and renders the key useless.

### Generating a Cipher Key

Just run ``python run.py`` and it should generate the cipherekey for you.


## Modular Arithmetic

Okay, let's make this super simple for a 4-year-old:

Imagine you have a special alphabet wheel with all the letters on it.
When you want to send a secret message, you:
1. Pick a letter from your message
2. Spin the wheel a little bit
3. Write down the new letter you see

To read the secret message:

1. Look at the secret letter
2. Spin the wheel back the same amount
3. Now you see the real letter!

It's like a fun game where you change letters into other letters to keep secrets!

the TL:DR


["Modular arithmetic"](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic) is used to derive the cipher text from the plain text message using the cipher key, one letter at a time.

In normal arithmetic, division takes place when you divide a _dividend_ by a _divisor_ to compute the _quotient:  **A &divide; B = Q**_.  You will have a _remainder_ If the _dividend_ is not evenly divisible by the _divisor:  **A &divide; B = Q <sup>remainder R</sup>**_.

**Modular arithmetic** is simply division whereupon the _quotient_ is ignored, and the _remainder_ is the result.

Thus, _**A mod B = R**_ (the _quotent **Q**_ is dropped and ignored, and the _remainder **R**_ is the result).

If the _modulus_ (what we call the _divisor_ in modular arithmetic) is 26, the _**remainder R &isin; { 0, 1, 2, ..., 25 }**_.  In other words, we get a whole number from 0 to 25 &mdash; a set of 26 numbers representing the 26 letters of the alphabet.

Thus, _**A mod 26 = R  &isin; { 0, 1, 2, ..., 25 }**_

### Modular Arithmetic for Encryption
The algorithm used in this demonstration of the one time pad takes the letters of a plain text message, converts that to a _whole number &isin; { 0, 1, 2, ..., 25 } **m**_; then takes the corresponding letters of the cipher key, converts that to a _whole number &isin; { 0, 1, 2, ..., 25 } **k**_; then adds _**m + k**_ to produce the _cipher text result_.

The problem is that the _cipher text result_ might be greater than 25!

The solution is modular arithmetic: _**(m + k) mod 26 = c**_

This produces a _cipher text result **c**_ between 0 and 25, which easily translates into a letter from A to Z.

### Modular Arithmetic for Decryption
To decrypt the cipher text back to the plain text message, we reverse the calculation &mdash; again relying on modular arithmetic to produce a letter of the alphabet from 0 to 25 (A-Z).

Simply put, if you add the plain text message letter _**m**_ to the cipher key letter _**k**_ to produce the cipher text letter _**c**_, you can reverse the process to decrypt the message by taking the cipher text letter _**c**_ and subtracting the cipher key letter _**k**_ to arrive at the original plain text message letter _**m**_.

if _**m + k = c**_, then _**c - k = m**_.

But there&rsquo;s a wrinkle.  You could end up with a negative value, anywhere from -25 to 0!

The solution is modular arithmetic: _**(c - k + 26) mod 26 = m**_
 
Since the +26 we added to the _dividend_ is evenly divisible by the modulus, zero is added to the remainder _**m**_ which, of course,  does not affect the result.  Adding +26 to the _dividend_ ensures that the calculation is made using a _whole number_ {&ge;0}.

This produces a result between 0 and 25, which easily translates into a letter from A to Z.
