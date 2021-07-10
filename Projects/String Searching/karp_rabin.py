# Karp-Rabin String Searching

import sys

import numpy

t_max = 5000  # Our given max text size

s_max = 10  # Our given max string size

t = numpy.empty(t_max, dtype=str)  # Our array to store the text

s = numpy.empty(s_max, dtype=str)  # Our array to store the string we want to match

t_index = 0  # An index for t

t_len = 0  # A counter for the total values in array t

s_index = 0  # An index for s

s_len = 0  # A counter for the total values in array s

prime = 5  # Our prime for our hashing function

crunch = 5  # We always crunch our letter value

power = 1  # Pre-calculation of p^s_len-1

modulus = (2**32)/(2**5)  # We compute a large modulus result


def hash_function(array, counter):  # Our function to compute the hash of our text segment

    global prime, power, crunch

    hash_value = 0

    power = 1

    for i in range(0, counter):  # For every character in the text
        hash_value += (hash_value*prime + letter_value(array[i]) % crunch) % modulus  # Compute with Compact Evaluation
        power *= prime

    power /= prime

    return hash_value % modulus  # And return that value  MOD THIS TOO


def letter_value(letter):  # As we know our alphabet and it's short, we can just code it
    return ord(letter) % prime


def main():  # Our main function

    global t_index, s_index, t_len, s_len

    user_file = input("Please enter the name of the input file: ")  # Request file name from user

    try:
        file = open(user_file)  # Try to open the file

    except NameError or FileNotFoundError:  # Catch any errors
        sys.exit("Error opening file. Program will exit.")

    text = file.readline()  # Our number that we read in

    for character in text:  # We look at every character in the text file
        if character == "\n":
            break
        t[t_len] = character  # And insert it into our text array
        t_len += 1

    string = file.readline()

    for char in string:  # We get every character from our sequence
        if char == "\n":
            break
        s[s_len] = char  # And insert it into our string array
        s_len += 1

    hash_s = hash_function(s, s_len)  # We calculate the initial hash for the string

    hash_t = hash_function(t, s_len)  # And the same for our initial chunk of text

    for i in range(0, t_len - s_len):  # For every section of text until the end of our text
        if hash_s == hash_t:  # If we get a hash match
            same = True
            j = 0
            while j < s_len:  # We're going to brute force check the letters from a match
                if s[j] != t[i + j]:
                    same = False
                    break
                j += 1
            if same:  # If every one of our characters matched, then we found the sequence in our text
                print("Match found starting at T[" + str(i) + "]")

        hash_t = ((hash_t - power*(letter_value(t[i]) % crunch)) * prime) % modulus + letter_value(t[i+s_len]) % crunch

    file.close()


main()
