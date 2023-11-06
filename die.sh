#!/bin/bash

# Function to generate a random number between 1 and 6 (inclusive)
roll_die() {
    local random_bytes
    local random_number
    local range=256

    # Read 1 byte from /dev/urandom (256 possibilities)
    random_bytes=$(od -An -N1 -tu1 < /dev/urandom)
    
    # Calculate the random number within the desired range
    let "random_number = $random_bytes % $range + 1"
    
    # If the random number is greater than 6, roll again to ensure fairness
    if [ "$random_number" -gt 6 ]; then
        roll_die
    else
        echo "$random_number"
    fi
}

# Roll the die
result=$(roll_die)

echo "You rolled: $result"
