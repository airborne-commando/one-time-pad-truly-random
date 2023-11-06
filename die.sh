#!/bin/bash

# Function to generate a random number between 1 and 6 (inclusive)
roll_die() {
    local random_bytes
    local random_number
    local range=5

    # Read 1 byte from /dev/urandom (5 possibilities)
    random_bytes=$(od -An -N1 -tu1 < /dev/urandom)
    
    # Calculate the random number within the desired range (0 to 5)
    let "random_number = ($random_bytes % $range) + 1"
    
    echo "$random_number"
}

# Roll two dice
die1=$(roll_die)
die2=$(roll_die)

echo "Result of Die 1: $die1"
echo "Result of Die 2: $die2"

# Calculate the total
total=$((die1 + die2))
echo "Total: $total"
