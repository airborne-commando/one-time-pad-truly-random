import os
import sys
import re
import random
import string

#Author Nthompson096 on gitgub

class OneTimePadModulo26:
    def __init__(self):
        self.alphabet = string.ascii_uppercase

    def encrypt(self, key, plaintext):
        if len(key) < len(plaintext):
            return False
        return ''.join([self.alphabet[(self.alphabet.index(p) + self.alphabet.index(k)) % 26] 
                        for p, k in zip(plaintext, key)])

    def decrypt(self, key, ciphertext):
        if len(key) < len(ciphertext):
            return False
        return ''.join([self.alphabet[(self.alphabet.index(c) - self.alphabet.index(k)) % 26] 
                        for c, k in zip(ciphertext, key)])

    def tty(self, text):
        return ''.join([char for char in text if char in self.alphabet])

    def get_vigenere_table(self):
        table = []
        for i in range(26):
            row = self.alphabet[i:] + self.alphabet[:i]
            table.append(' '.join(row))
        return '\n'.join(table)

def generate_random_letters(length=2048):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def decrypt_with_key_from_file(ciphertext_file, key_file):
    with open(ciphertext_file, 'r') as file:
        cipher_text = file.read()
    with open(key_file, 'r') as file:
        key = file.read()
    
    decrypt_with_key(cipher_text, key)

def decrypt_with_key(cipher_text, key):
    cipher = OneTimePadModulo26()

    # Clean up the input
    cipher_text = re.sub(r'[^A-Z]', '', cipher_text.upper())
    key = re.sub(r'[^A-Z]', '', key.upper())

    # Ensure the key is long enough
    if len(key) < len(cipher_text):
        print("Error: The key must be at least as long as the ciphertext.")
        return

    decrypted_text = cipher.decrypt(key, cipher_text)

    # Output the results
    print(f"{'':12}{'-' * len(cipher_text)}")
    print(f"Decrypted:  {' '.join(cipher.tty(decrypted_text))} (decrypted)")

def main():
    cipher = OneTimePadModulo26()

    if len(sys.argv) < 2:
        print("Error: No input provided. Use 'encrypt file <file_path>', 'encrypt text <your_text>', or 'decrypt' as arguments.")
        return

    command = sys.argv[1]

    if command == 'encrypt':
        if len(sys.argv) < 4:
            print("Error: Invalid input for encryption. Use 'encrypt file <file_path>' or 'encrypt text <your_text>' as arguments.")
            return

        input_type = sys.argv[2]
        if input_type == 'file' and os.path.exists(sys.argv[3]):
            with open(sys.argv[3], 'r') as file:
                user_input = file.read().upper()
        elif input_type == 'text':
            user_input = ' '.join(sys.argv[3:]).upper()  # Join all arguments after 'text' into a single string
        else:
            print("Error: Invalid input. Use 'encrypt file <file_path>' or 'encrypt text <your_text>' as arguments.")
            return

        # Ensure the 'text' directory exists
        os.makedirs('text', exist_ok=True)

        with open('./text/plaintext.txt', 'w') as file:
            file.write(user_input)

        # Generate random letters for cipher key
        random_cipher_key = generate_random_letters()
        with open('./text/cipherkey.txt', 'w') as file:
            file.write(random_cipher_key)

        with open('./text/plaintext.txt', 'r') as file:
            plain_text = re.sub(r'[^A-Z]', '', file.read().upper())

        with open('./text/cipherkey.txt', 'r') as file:
            cipher_key = re.sub(r'[^A-Z]', '', file.read().upper())

        cipher_text = cipher.encrypt(cipher_key, plain_text)
        decoded_plain_text = cipher.decrypt(cipher_key, cipher_text)

        if cipher_text is False or decoded_plain_text is False:
            print("For perfect encryption in the one time pad, the key length must be equal to, or greater than, the message length.")
            return

        with open('./text/ciphertext.txt', 'w') as file:
            file.write(cipher.tty(cipher_text))

        print(cipher.get_vigenere_table())

        message_length = len(plain_text)
        cipher_key_used = cipher_key[:message_length]

        print(f"Plain:  {' '.join(cipher.tty(plain_text))} (message)")
        print(f"Key:    {' '.join(cipher.tty(cipher_key_used))} (secret)")
        print(f"        {'-' * (message_length * 2 - 1)}")
        print(f"Cipher: {' '.join(cipher.tty(cipher_text))} (cipher)")

    elif command == 'decrypt':
        ciphertext_file = "./text/ciphertext.txt"
        key_file = "./text/cipherkey.txt"
        decrypt_with_key_from_file(ciphertext_file, key_file)

    else:
        print("Error: Invalid command. Use 'encrypt' or 'decrypt'.")

if __name__ == "__main__":
    main()
