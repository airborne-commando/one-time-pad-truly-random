import os
import sys
import re
import random
import string
import argparse

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
        segment_size = random.randint(2, max(2, len(text_list)//5))
        for i in range(0, len(text_list), segment_size):
            text_list[i:i + segment_size] = reversed(text_list[i:i + segment_size])
        
        for _ in range(random.randint(1, max(1, len(text_list)//10))):
            start1 = random.randint(0, len(text_list) - 1)
            start2 = random.randint(0, len(text_list) - 1)
            if start1 != start2:
                end1 = min(start1 + segment_size, len(text_list))
                end2 = min(start2 + segment_size, len(text_list))
                text_list[start1:end1], text_list[start2:end2] = text_list[start2:end2], text_list[start1:end1]

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
    cipher_text = re.sub(r'[^A-Z]', '', cipher_text.upper())
    key = re.sub(r'[^A-Z]', '', key.upper())

    if len(key) < len(cipher_text):
        print("Error: The key must be at least as long as the ciphertext.")
        return

    decrypted_text = cipher.decrypt(key, cipher_text)
    print(f"{'':12}{'-' * len(cipher_text)}")
    print(f"Decrypted:  {' '.join(cipher.tty(decrypted_text))} (decrypted)")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="One-time pad encryption/decryption tool", add_help=False)
    parser.add_argument('-e', '--encrypt', action='store_true', help='Encrypt mode')
    parser.add_argument('-d', '--decrypt', action='store_true', help='Decrypt mode')
    parser.add_argument('-c', '--challenge', action='store_true', help='Challenge mode')
    parser.add_argument('-f', '--file', help='Input file path')
    parser.add_argument('-t', '--text', nargs='+', help='Input text')
    parser.add_argument('-s', '--scramble', choices=['y', 'n'], help='Scramble ciphertext (y/n)')
    parser.add_argument('-r', '--random-chars', choices=['y', 'n'], help='Add random characters (y/n)')
    parser.add_argument('-co', '--complexity', choices=['y', 'n'], help='Add complexity (y/n)')
    parser.add_argument('-/?', '--usage', action='store_true', help='Show usage information')

    args = parser.parse_args()

    if args.usage:
        print("Usage:")
        print("  Encryption: python run.py -e [-c] [-s y/n] [-r y/n] [-co y/n] (-f <file_path> | -t <your_text>)")
        print("  Decryption: python run.py -d")
        print("\nOptions:")
        print("  -e, --encrypt     Encrypt mode")
        print("  -d, --decrypt     Decrypt mode")
        print("  -c, --challenge   Challenge mode")
        print("  -f, --file        Input file path")
        print("  -t, --text        Input text")
        print("  -s, --scramble y/n    Force scramble option (y/n)")
        print("  -r, --random-chars y/n Force random chars option (y/n)")
        print("  -co, --complexity y/n  Force complexity option (y/n)")
        print("  -/?, --usage      Show usage information")
        print("\nExamples:")
        print("  python run.py -e -t \"secret\" --scramble y --random-chars n --complexity y")
        print("  python run.py -e -c -f input.txt --scramble n --random-chars y --complexity n")
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

        if args.challenge:
            clear_screen()

        os.makedirs('text', exist_ok=True)
        with open('./text/plaintext.txt', 'w') as file:
            file.write(user_input)

        plain_text = re.sub(r'[^A-Z]', '', user_input)
        random_cipher_key = generate_random_letters(len(plain_text))
        with open('./text/cipherkey.txt', 'w') as file:
            file.write(random_cipher_key)

        cipher_text = cipher.encrypt(random_cipher_key, plain_text)
        
        if cipher_text is False:
            print("For perfect encryption in the one-time pad, the key length must be equal to or greater than the message length.")
            return

        if args.scramble:
            scramble = args.scramble == 'y'
            add_random = args.random_chars == 'y' if args.random_chars else False
            add_complex = args.complexity == 'y' if args.complexity else False
            
            if scramble:
                print(f"Do you want to scramble the ciphertext? (n/y): {args.scramble}")
                if args.random_chars:
                    print(f"Do you want to add random ciphertext at a random chance? (n/y): {args.random_chars}")
                if args.complexity:
                    print(f"Do you want to add additional complexity to the randomness? (n/y): {args.complexity}")
                
                cipher_text = scramble_text(cipher_text, add_random_chars=add_random, add_complexity=add_complex)
        else:
            scramble_option = input("Do you want to scramble the ciphertext? (n/y): ").lower()
            if scramble_option == 'y':
                add_random_option = input("Do you want to add random ciphertext at a random chance? (n/y): ").lower()
                add_complexity_option = input("Do you want to add additional complexity to the randomness? (n/y): ").lower()
                cipher_text = scramble_text(cipher_text, 
                                          add_random_chars=(add_random_option == 'y'), 
                                          add_complexity=(add_complexity_option == 'y'))

        with open('./text/ciphertext.txt', 'w') as file:
            file.write(cipher.tty(cipher_text))

        message_length = len(plain_text)
        with open('./text/output.txt', 'w') as output_file:
            output_file.write("Vigenere Table:\n")
            output_file.write(cipher.get_vigenere_table() + "\n\n")

            if not args.challenge:
                output_file.write(f"Plain:  {' '.join(cipher.tty(plain_text))} (message)\n")
            output_file.write(f"Key:    {' '.join(cipher.tty(random_cipher_key[:message_length]))} (secret)\n")
            output_file.write(f"Cipher: {' '.join(cipher.tty(cipher_text))} (cipher)\n")

        print("Encryption details have been saved to ./text/output.txt")
        if args.challenge:
            print("Challenge mode: Plaintext not included in output")

    elif args.decrypt:
        ciphertext_file = "./text/ciphertext.txt"
        key_file = "./text/cipherkey.txt"
        decrypt_with_key_from_file(ciphertext_file, key_file)

    else:
        print("Error: Please specify either encryption (-e) or decryption (-d) mode.")

if __name__ == "__main__":
    main()
