# Program to fill hash table with open addressing and table doubling

import numpy

import sys

m = 100

prime = 300737933844030629

inserted = 0

hash_table = numpy.zeros(m, dtype=int)  # Our dictionary to store our values we read in

new_hash_table = numpy.zeros(m, dtype=int)


def insert_hash(value):  # Our function to create and store the hashed value
    global inserted
    count = 0
    while count != m:
        probe = hash_function(value, count)
        if hash_table[probe] == 0:
            hash_table[probe] = value
            break
        else:
            count += 1

    if count == m:
        print("Value {0} Not Inserted.".format(value))
    else:
        inserted += 1
        if inserted > (m//2):
            table_double()


def insert_new_hash(value):
    count = 0
    while count != m:
        probe = hash_function(value, count)
        if new_hash_table[probe] == 0:
            new_hash_table[probe] = value
            break
        else:
            count += 1
    if count == m:
        print("Error with {0}.".format(value))


def hash_function(k, i):
    return (hash_1(k) + i*hash_2(k)) % m


def hash_1(key):
    return (key % prime) % m


def hash_2(key):
    return (2*hash_3(key)+1) % m


def hash_3(key):  # Universal Hashing Function, using two random integers
    return ((42370*key + 12379) % prime) % m


def table_double():  # Our function to double the array
    global m, hash_table, new_hash_table

    m *= 2  # Set the new size

    new_hash_table = numpy.zeros(m, dtype=int)  # We create a new array of twice the current size

    for i in range(0, m // 2):  # We copy the data from the old stack to the new stack
        if hash_table[i] != 0:
            insert_new_hash(hash_table[i])

    print("Table doubled from {0} to {1}".format((m // 2), m))

    hash_table = new_hash_table  # And we make the old stack now equal to the new stack

    return


def main():  # Our main function

    user_file = input("Please enter the name of the input file: ")  # Request file name from user

    try:
        file = open(user_file)  # Try to open the file

    except NameError or FileNotFoundError:  # Catch any errors
        sys.exit("Error opening file. Program will exit.")

    while True:
        number = file.readline().strip()  # Our number that we read in

        if not number:  # If we get to the end of the file, break
            break

        value = int(number)  # Cast it to an int

        insert_hash(value)  # Insert the value into our hash table

    print("Number of empty spaces: {0}".format(m-inserted))

    print(hash_table)


main()
