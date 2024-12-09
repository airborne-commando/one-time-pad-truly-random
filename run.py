import os
import sys
import re
import random
import string

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

def generate_random_letters(length=2048):
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

def main():
    cipher = OneTimePadModulo26()

    if len(sys.argv) < 2:
        print("Error: No input provided. Use '-e -f <file_path>', '-e -t <your_text>', or '-d' as arguments.")
        return

    command = sys.argv[1]

    if command == '-e':
        if len(sys.argv) < 4:
            print("Error: Invalid input for encryption. Use '-e -f <file_path>', '-e -t <your_text>', or '-d' as arguments.")
            return

        input_type = sys.argv[2]
        if input_type == '-f' and os.path.exists(sys.argv[3]):
            with open(sys.argv[3], 'r') as file:
                user_input = file.read().upper()
        elif input_type == '-t':
            user_input = ' '.join(sys.argv[3:]).upper()  # Join all arguments after 'text' into a single string
        else:
            print("Error: Invalid input. Use '-e -f <file_path>', '-e -t <your_text>', or '-d' as arguments.")
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

        print(cipher.get_vigenere_table())

        message_length = len(plain_text)
        cipher_key_used = cipher_key[:message_length]

        print(f"Plain:  {' '.join(cipher.tty(plain_text))} (message)")
        print(f"Key:    {' '.join(cipher.tty(cipher_key_used))} (secret)")
        print(f"        {'-' * (message_length * 2 - 1)}")
        print(f"Cipher: {' '.join(cipher.tty(cipher_text))} (cipher)")

    elif command == '-d':
        ciphertext_file = "./text/ciphertext.txt"
        key_file = "./text/cipherkey.txt"
        decrypt_with_key_from_file(ciphertext_file, key_file)

    elif command == '-/?':
            print("Commands are as follows:\n"
                "Use '-e' to encrypt a file '-f' or text '-t'\n"
                "Use '-d' to decrypt a file '-f' or just pass '-d' to decrypt the ./text directory\n"
                "randomness: will ask the user if you'd want to scramble the ciphertext around\n"
                "complexity: will ask the user if it wants to add a random cipher\n"
                "Will also ask the user to add additional complexity to the randomness\n"
                "the script will devide the text into random segments and reverses each segment\n"
                "selects random segments and swaps their positions with other random segments\n"
                "script replaces a few random characters in the text with other random characters from the alphabet")
            return

    else:
        print("Error: Invalid command. Use '-e' or '-d'.")

if __name__ == "__main__":
    main()
