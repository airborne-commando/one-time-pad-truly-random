#!/bin/bash

# Function to generate a random letter
generate_random_letter() {
    local random_byte
    local random_letter
    local alphabet="abcdefghijklmnopqrstuvwxyz"

    # Read 1 byte from /dev/urandom
    random_byte=$(od -An -N1 -tu1 < /dev/urandom)

    # Calculate the index within the alphabet range (0-25)
    let "index = $random_byte % 26"

    # Get the random letter from the alphabet
    random_letter=${alphabet:index:1}
    
    echo -n "$random_letter"
}

# Generate 2048 random letters, you can add/decrease by editing i<value
#EXAMPLE a 512 ciphertext:
#random_letters=""
#for ((i=0; i<512; i++)); do
#    random_letters+=$(generate_random_letter)
#done

random_letters=""
for ((i=0; i<2048; i++)); do
    random_letters+=$(generate_random_letter)
done

echo "$random_letters" > text/cipherkey.txt

echo "Random letters saved to cipherkey.txt"
