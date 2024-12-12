import os
import sys
import re
import random
import string
import argparse

# Author airborne-commando on github

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

def generate_random_letters(length):
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))

def scramble_text(text, add_random_chars=False, add_complexity=False):
    text_list = list(text)
    random.shuffle(text_list)
    
    if add_random_chars:
        insert_positions = random.sample(
            range(len(text_list)), 
            k=random.randint(1, max(1, len(text_list)//10))
        )
        for pos in insert_positions:
            text_list.insert(pos, random.choice(string.ascii_uppercase))

    if add_complexity:
        # Reverse segments of the text
        segment_size = random.randint(2, max(2, len(text_list)//5))
        for i in range(0, len(text_list), segment_size):
            text_list[i:i + segment_size] = reversed(text_list[i:i + segment_size])
        
        # Interchange random segments of the text
        for _ in range(random.randint(1, max(1, len(text_list)//10))):
            start1 = random.randint(0, len(text_list) - 1)
            start2 = random.randint(0, len(text_list) - 1)
            if start1 != start2:
                end1 = min(start1 + segment_size, len(text_list))
                end2 = min(start2 + segment_size, len(text_list))
                text_list[start1:end1], text_list[start2:end2] = text_list[start2:end2], text_list[start1:end1]

        # Replace some characters with random characters
        replace_positions = random.sample(
            range(len(text_list)),
            k=random.randint(1, max(1, len(text_list)//10))
        )
        for pos in replace_positions:
            text_list[pos] = random.choice(string.ascii_uppercase)

    return ''.join(text_list)

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

def clear_screen():
    # Cross-platform screen clearing
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="One-time pad encryption/decryption tool", add_help=False)
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt mode')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('-c', '--challenge', action='store_true', help='Challenge mode')
    parser.add_argument('-f', '--file', help='Input file path')
    parser.add_argument('-t', '--text', nargs='+', help='Input text')
    parser.add_argument('-/?', '--usage', action='store_true', help='Show usage information')

    args = parser.parse_args()

    if args.usage:
        print("Usage:")
        print("  Encryption: python run.py -e [-c] (-f <file_path> | -t <your_text>)")
        print("  Decryption: python run.py -d")
        print("\nOptions:")
        print("  -e, --encrypt     Encrypt mode")
        print("  -d, --decrypt     Decrypt mode")
        print("  -c, --challenge   Challenge mode (clears screen and excludes plaintext from output)")
        print("  -f, --file        Input file path")
        print("  -t, --text        Input text (use quotes for multi-word input)")
        print("  -/?, --usage      Show this usage information")
        print("\nExample:")
        print("  python run.py -e -c -t \"This is a secret message\"")
        return

    cipher = OneTimePadModulo26()

    if args.encrypt:
        if args.file:
            if os.path.exists(args.file):
                with open(args.file, 'r') as file:
                    user_input = file.read().upper()
            else:
                print(f"Error: File '{args.file}' does not exist.")
                return
        elif args.text:
            user_input = ' '.join(args.text).upper()
        else:
            print("Error: Please provide either a file (-f) or text (-t) for encryption.")
            return

        challenge_mode = args.challenge

        if challenge_mode:
            clear_screen()

        # Ensure the 'text' directory exists
        os.makedirs('text', exist_ok=True)

        with open('./text/plaintext.txt', 'w') as file:
            file.write(user_input)

        # Clean the input text
        plain_text = re.sub(r'[^A-Z]', '', user_input)

        # Generate random letters for cipher key with the same length as plain_text
        random_cipher_key = generate_random_letters(len(plain_text))
        with open('./text/cipherkey.txt', 'w') as file:
            file.write(random_cipher_key)

        cipher_text = cipher.encrypt(random_cipher_key, plain_text)
        
        if cipher_text is False:
            print("For perfect encryption in the one-time pad, the key length must be equal to or greater than the message length.")
            return

        # Ask if the user wants to scramble the ciphertext
        scramble_option = input("Do you want to scramble the ciphertext? (n/y): ").lower()
        add_random_chars = False
        add_complexity = False
        if scramble_option == 'y':
            add_random_option = input("Do you want to add random ciphertext at a random chance? (n/y): ").lower()
            add_random_chars = add_random_option == 'y'
            add_complexity_option = input("Do you want to add additional complexity to the randomness? (n/y): ").lower()
            add_complexity = add_complexity_option == 'y'
            cipher_text = scramble_text(cipher_text, add_random_chars, add_complexity)

        with open('./text/ciphertext.txt', 'w') as file:
            file.write(cipher.tty(cipher_text))

        message_length = len(plain_text)

        # Create a new file to store the output
        with open('./text/output.txt', 'w') as output_file:
            # Write the Vigenere table
            output_file.write("Vigenere Table:\n")
            output_file.write(cipher.get_vigenere_table() + "\n\n")

            # Write the key and ciphertext, but not the plaintext in challenge mode
            if not challenge_mode:
                output_file.write(f"Plain:  {' '.join(cipher.tty(plain_text))} (message)\n")
            output_file.write(f"Key:    {' '.join(cipher.tty(random_cipher_key[:message_length]))} (secret)\n")
            output_file.write(f"Cipher: {' '.join(cipher.tty(cipher_text))} (cipher)\n")

        print("Encryption details have been saved to ./text/output.txt")
        if challenge_mode:
            print("Challenge mode: Plaintext not included in output")

    elif args.decrypt:
        ciphertext_file = "./text/ciphertext.txt"
        key_file = "./text/cipherkey.txt"
        
        decrypt_with_key_from_file(ciphertext_file, key_file)

    else:
        print("Error: Please specify either encryption (-e) or decryption (-d) mode.")

if __name__ == "__main__":
    main()
