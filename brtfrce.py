import itertools
import string
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from multiprocessing import Pool, cpu_count, set_start_method

class OneTimePadModulo26:
    def __init__(self):
        self.alphabet = string.ascii_uppercase

    def decrypt(self, key, ciphertext):
        return ''.join([self.alphabet[(self.alphabet.index(c) - self.alphabet.index(k)) % 26] 
                        for c, k in zip(ciphertext, key)])

    def tty(self, text):
        return ''.join([char for char in text if char in self.alphabet])

def score_text(text, model, tokenizer, device):
    inputs = tokenizer(text, return_tensors='pt').to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs['input_ids'])
        loss = outputs.loss
        return -loss.item()

def decrypt_and_score(args):
    perm, ciphertext, model_name = args
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    otp = OneTimePadModulo26()
    possible_key = ''.join(perm)
    decrypted = otp.decrypt(possible_key * (len(ciphertext) // len(possible_key) + 1), ciphertext)
    score = score_text(decrypted, model, tokenizer, device)
    return score, possible_key, decrypted

def brute_force_decrypt(ciphertext, key, model_name):
    otp = OneTimePadModulo26()
    ciphertext = otp.tty(ciphertext.upper())
    key = otp.tty(key.upper())

    best_score = float('-inf')
    best_key = None
    best_decrypted_text = None

    lengths = range(1, len(key) + 1)
    num_cpus = cpu_count()

    for length in lengths:
        permutations = list(itertools.permutations(key[:length]))
        
        with Pool(processes=num_cpus) as pool:
            args = [(perm, ciphertext, model_name) for perm in permutations]
            results = pool.map(decrypt_and_score, args)

        for score, possible_key, decrypted in results:
            if score > best_score:
                best_score = score
                best_key = possible_key
                best_decrypted_text = decrypted
    
    return best_key, best_decrypted_text

def main():
    set_start_method('spawn')

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    model_name = 'gpt2'
    
    with open('text/cipherkey.txt', 'r') as f:
        key = f.read().strip()
    
    with open('text/ciphertext.txt', 'r') as f:
        ciphertext = f.read().strip()
    
    found_key, decrypted_text = brute_force_decrypt(ciphertext, key, model_name)
    
    if found_key:
        print(f"Possible key found: {found_key}")
        print(f"Decrypted text: {decrypted_text[:100]}...")  # Print first 100 characters
    else:
        print("No valid key found.")

if __name__ == "__main__":
    main()
