# Heapsort algorithm

import sys

import numpy

heap = numpy.empty(1000, dtype=int)

count = 0


def siftdown(array, i, length):
    child = (i * 2) + 1
    if child < length:  # We ensure that we do not fall off the end of the array
        if child+1 < length:  # We check to see whether there is a left and right child or just a left
            if array[child] < array[child+1]:  # We test against the largest child
                child += 1
        if array[i] < array[child]:  # And check if we need to swap the values
            swap(i, child)  # If so, we swap and recursively repeat the siftdown function
            siftdown(array, child, length)


def swap(a, b):  # Our function to swap our values
    temp = heap[a]
    heap[a] = heap[b]
    heap[b] = temp
    return heap


def makeheap(): # Our function to make the heap
    for i in range(count//2-1, -1, -1): # Our range is from the midpoint of our filled spaces until index[0]
        siftdown(heap, i, count)


def heapsort():
    makeheap()
    print("\nHeap: ", heap[:count])
    for i in range(count-1, 0, -1):  # For all values in our heap
        swap(0, i)  # Swap the first and last, then reduce the heap by 1
        siftdown(heap[:i], 0, len(heap[:i])) # And remake the heap


def main():

    global count

    user_file = input("Please enter the name of the file: ")

    try:
        file = open(user_file)

    except FileNotFoundError:
        sys.exit("Error opening file. Program will exit.")

    while True:
        line = file.readline().strip()
        if not line:
            break
        value = int(line)
        heap[count] = value
        count += 1

    print("\nData: ", heap[:count])
    heapsort()
    print("\nSorted: ", heap[:count])


main()
