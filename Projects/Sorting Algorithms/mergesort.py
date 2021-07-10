# Mergesort algorithm

import sys

import numpy

index = 0

data = numpy.empty(1000, dtype=int)


def mergesort(array):  # Our mergesort function
    if len(array) > 1:

        array_length = len(array)  # We'll need this for our loop reads

        midpoint = int(len(array)) // 2  # Our dividing position

        left_half = array[:midpoint]  # We have a left half of the array

        right_half = array[midpoint:]  # And a right half of the array

        left_half = mergesort(left_half)  # And recursively call mergesort on both halves

        right_half = mergesort(right_half)  # Until we have n arrays of size 1

        array = numpy.empty(array_length, dtype=int)  # We create a new array

        array_counter = 0  # With pointers and a counter

        left_index = 0

        right_index = 0

        while left_index < len(left_half) and right_index < len(right_half):
            # We test each element in one array against the other and store the highest value first in the new array
            if left_half[left_index] < right_half[right_index]:
                array[array_counter] = left_half[left_index]
                array_counter += 1
                left_index += 1

            else:
                array[array_counter] = right_half[right_index]
                array_counter += 1
                right_index += 1
        # If there's only one value left, store it and recursively move up to join the next two haves
        for i in range(left_index, len(left_half)):
            array[array_counter] = left_half[left_index]
            array_counter += 1
            left_index += 1

        for j in range(right_index, len(right_half)):
            array[array_counter] = right_half[right_index]
            array_counter += 1
            right_index += 1

    return array  # Return this newly sorted array


def main():  # Our main function
    global index, data

    user_file = input("Please enter the name of the input file: ")  # We request the user's file name

    try:
        file = open(user_file)  # We attempt to open the file

    except FileNotFoundError:  # And exit the program if we get an error
        sys.exit("Error opening file. Program will exit.")

    while True:
        line = file.readline().strip().lower()
        if not line:
            break
        else:
            value = int(line)
            data[index] = value
            index += 1
    trimmed = numpy.empty(index, dtype=int)
    for i in range(0, index):
        trimmed[i] = data[i]
    data = mergesort(trimmed)
    print(data)


main()
