# David Barranquero
# Student Number: 4760396
# Student Login: db495
# CSCI203 Lab 4 Week 5

import sys

import numpy

data = numpy.empty(50, dtype=int)  # Stores the nodes

left = numpy.empty(50, dtype=int)

right = numpy.empty(50, dtype=int)

height = numpy.empty(50, dtype=int)

count = 0  # counts the amount of numbers we've read in

next_val = 0  # tracks the position of the next node


def avl_insert(node, value):  # Our function to insert the new node
    global next_val
    if node == -1:  # If there's no node, make a new one with invalid left/right children
        node = next_val
        next_val += 1
        data[node] = value  # And store node in data
        left[node] = -1
        right[node] = -1
        height[node] = 0
        return node

    if value == data[node]:  # If we get a duplicate, we don't need to store it
        return node

    if value < data[node]:  # If the value is less, traverse the left tree
        # And recursively look for it's position
        left[node] = avl_insert(left[node], value)
        if height[left[node]] - height[right[node]] > 1:  # We attempt to re-balance the tree
            if value < data[left[node]]:  # And check which side the imbalance is
                node = rotate_right(node)
            else:
                node = double_right(node)
        height[node] = max(height[left[node]], height[right[node]]) + 1  # And finally update the heights again
        return node

    # If the value is more than current node, traverse the right tree
    if value > data[node]:
        right[node] = avl_insert(right[node], value)
        if height[left[node]] - height[right[node]] < -1:  # We attempt to re-balance the tree
            if value < data[right[node]]:  # And check which side the imbalance is
                node = double_left(node)
            else:
                node = rotate_left(node)
        height[node] = max(height[left[node]], height[right[node]]) + 1  # And finally update the heights again
        return node


def rotate_right(node):  # Our function to fix an imbalance in the left subtree of the left child
    x = left[node]
    left[node] = right[x]
    right[x] = node
    height[node] = max(height[left[node]], height[right[node]]) + 1
    height[x] = max(height[left[x]], height[right[x]]) + 1
    node = x
    return node


def rotate_left(node):  # Our function to fix an imbalance in the right subtree of the right child
    x = right[node]
    right[node] = left[x]
    left[x] = node
    height[node] = max(height[left[node]], height[right[node]]) + 1
    height[x] = max(height[left[x]], height[right[x]]) + 1
    node = x
    return node


def double_right(node):  # Our function to fix an imbalance in the right subtree of the left child
    left[node] = rotate_left(left[node])
    node = rotate_right(node)
    return node


def double_left(node):  # Our function to fix an imbalance in the left subtree of the right child
    right[node] = rotate_right(right[node])
    node = rotate_left(node)
    return node


def in_order(node):  # Our in order traversal function
    global count
    if node == -1:
        return
    in_order(left[node])  # First traverse the left branches
    print("{0:>5}".format(data[node]), end="")  # When we reach a leaf, we print it out
    count += 1
    if count == 10:
        print()
        count = 0
    in_order(right[node])  # Then traverse the right branches
    return


def main():  # Our main function

    user_file = input("Please enter the name of the input file: ")  # We request the user's file name

    try:
        file = open(user_file)  # We attempt to open the file

    except FileNotFoundError:  # And exit the program if we get an error
        sys.exit("Error opening file. Program will exit.")

    root = -1

    while True:
        line = file.readline().strip().lower()
        if not line:
            break
        else:
            node = int(line)
            root = avl_insert(root, node)

    print()
    in_order(root)
    print()


main()
