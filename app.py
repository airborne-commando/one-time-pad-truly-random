from flask import Flask, render_template, request, send_file
import os
import re
import random
import string

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    cipher = OneTimePadModulo26()
    user_input = request.form['plaintext'].upper()
    
    # Ensure the 'text' directory exists
    os.makedirs('text', exist_ok=True)

    with open('./text/plaintext.txt', 'w') as file:
        file.write(user_input)

    # Generate random letters for cipher key
    random_cipher_key = generate_random_letters()
    with open('./text/cipherkey.txt', 'w') as file:
        file.write(random_cipher_key)

    plain_text = re.sub(r'[^A-Z]', '', user_input)
    cipher_key = random_cipher_key.upper()

    cipher_text = cipher.encrypt(cipher_key, plain_text)
    
    if cipher_text is False:
        return "Error: The key must be at least as long as the plaintext."

    with open('./text/ciphertext.txt', 'w') as file:
        file.write(cipher.tty(cipher_text))

    message_length = len(plain_text)
    cipher_key_used = cipher_key[:message_length]

    return render_template('result.html', 
                           plain_text=cipher.tty(plain_text),
                           cipher_key=cipher.tty(cipher_key_used),
                           cipher_text=cipher.tty(cipher_text),
                           vigenere_table=cipher.get_vigenere_table())

@app.route('/decrypt', methods=['POST'])
def decrypt():
    cipher = OneTimePadModulo26()
    
    if 'ciphertext_file' in request.files:
        ciphertext_file = request.files['ciphertext_file']
        if ciphertext_file.filename != '':
            cipher_text = ciphertext_file.read().decode('utf-8').upper()
        else:
            cipher_text = request.form['ciphertext'].upper()
    else:
        cipher_text = request.form['ciphertext'].upper()
    
    if 'key_file' in request.files:
        key_file = request.files['key_file']
        if key_file.filename != '':
            key = key_file.read().decode('utf-8').upper()
        else:
            key = request.form['key'].upper()
    else:
        key = request.form['key'].upper()

    # Clean up the input
    cipher_text = re.sub(r'[^A-Z]', '', cipher_text)
    key = re.sub(r'[^A-Z]', '', key)

    # Ensure the key is long enough
    if len(key) < len(cipher_text):
        return "Error: The key must be at least as long as the ciphertext."

    decrypted_text = cipher.decrypt(key, cipher_text)

    return render_template('decrypt_result.html', 
                           decrypted_text=cipher.tty(decrypted_text))

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'./text/{filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
