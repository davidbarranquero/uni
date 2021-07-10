# Program which reads in data in format specified in .txt file
# Program calculates the shortest and second shortest paths between start and goal vertices
# Program uses A* algorithm to achieve task


import numpy

import sys

# Arrays
adj_matrix = numpy.empty(0)  # Our adjacency matrix

vertices = numpy.empty(0)  # Our array to store the vertices

candidate = numpy.empty(0)  # Our array to store the vertices to be selected

distance = numpy.empty(0)  # Our array to store the distances from the starting vertex

parent_array = numpy.empty(0)  # Our array to store the parent index of each vertex

path = numpy.empty(0)  # Our array to store the changing paths

shortest_path = numpy.empty(0)  # Our array to store the final shortest path

second_shortest_path = numpy.empty(0)  # Our array to store the final second shortest path

heuristic = numpy.empty(0)  # Our array to store our heuristic calculations


# Variables

starting_vertex = 0  # Our starting vertex

goal_vertex = 0  # Our goal vertex

infinity = numpy.inf  # Our infinity value

n_vertices = 0  # The number of vertices

n_edges = 0  # The number of edges

vertex_index = 0  # An index for our vertices array

heap_size = 0  # A counter to keep track of the size of our heap

path_index = 0  # Our index for the path array

shortest_path_length = 0  # A counter for the shortest path length

second_shortest_path_length = 0  # A counter for the second shortest path length

shortest_path_index = 0  # An index for the shortest path array

second_shortest_path_index = 0  # An index for the second shortest path array


def create_paths():  # Our function to create the path and display it
    global path_index, starting_vertex, goal_vertex
    parent_search = goal_vertex - 1  # We keep track of the index of the parent of the current vertex
    path[path_index] = parent_search  # We are storing the index of the parent
    path_index += 1

    while parent_array[parent_search] != starting_vertex - 1:  # Loop through the parent array
        parent_search = parent_array[parent_search]  # Setting the next index as the value stored in parent array slot
        path[path_index] = parent_search  # Add it to our path array
        path_index += 1  # And increment the counter

    parent_search = parent_array[parent_search]  # Then store the source vertex
    path[path_index] = parent_search


def display_paths(s, g):
    global path_index
    print("\nWe have travelled from Vertex {0} to Vertex {1}.".format(s, g))

    print("\nShortest Path:")

    print("\n   Length:    {0}".format(shortest_path_length))  # Display the shortest path length

    print("\n   Number of Vertices:  {0}".format(shortest_path_index + 1))  # Display the number of vertices

    print("\n   Vertices:  ", end="")

    # Now we loop backwards through the path array to display the path from start to goal
    for i in range(shortest_path_index, -1, -1):
        if i == 0:
            print(shortest_path[i] + 1)
        else:
            print(shortest_path[i] + 1, end=" > ")

    if shortest_path_length == infinity:  # In case no path exists
        print("\nAs path length is infinite. No path exists. Nor a second shortest path.\n")

    else:
        print("\nSecond Shortest Path:")

        print("\n   Length:    {0}".format(second_shortest_path_length))  # display the second shortest path length

        print("\n   Number of Vertices:  {0}".format(second_shortest_path_index + 1))  # Display the number of vertices

        print("\n   Vertices:  ", end="")

        # Again loop backwards through the path array to display the path from start to goal
        for i in range(second_shortest_path_index, -1, -1):
            if i == 0:
                print(second_shortest_path[i] + 1)
            else:
                print(second_shortest_path[i] + 1, end=" > ")

        print()


def calculate_heuristics(s, g):  # Our function to calculate the Euclidean distances
    global heuristic, distance

    for i in range(0, n_vertices):  # For every vertex in our candidate set

        # Calculate the Euclidean distance from that vertex i to our goal vertex g
        h = ((vertices[i][1] - vertices[g - 1][1]) ** 2 + (vertices[i][2] - vertices[g - 1][2]) ** 2) ** 0.5

        heuristic[i] = h  # Store the heuristic in our array for later use in finding the 2nd shortest path

        # And then we populate the candidate, distance and parent arrays
        candidate[i] = i+1

        distance[i] = adj_matrix[s-1][i]

        parent_array[i] = s - 1


def makeheap():  # Our function to make the heap
    for i in range(((heap_size // 2) - 1), -1, -1):  # Range is from the midpoint of our filled spaces until index[0]
        siftdown(i)
    return candidate


def siftup(i):  # Our function to sift up values
    global candidate
    if i == 0:  # If this is the front of the heap, stop
        return
    parent = (i-1)//2  # Calculate the parent index
    if distance[candidate[parent]-1] + heuristic[candidate[parent]-1] < \
            distance[candidate[i]-1] + heuristic[candidate[i]-1]:  # If the parent value is smaller, then its a heap
        return
    else:
        candidate = swap(i, parent)  # If not swap the values
        siftup(parent)  # And then siftup the parent


def siftdown(i):  # Our function to siftdown the values
    global candidate
    child = (i * 2) + 1  # Set the child value
    if child < heap_size:  # We ensure that we do not fall off the end of the array
        if child + 1 < heap_size:  # We check to see whether there is a left and right child or just a left
            if (distance[candidate[child]-1] + heuristic[candidate[child]-1]) > \
                    (distance[candidate[child+1]-1] + heuristic[candidate[child+1]-1]):
                child += 1  # For the min heap, if the left child is larger than the right, use the right child
        if (distance[candidate[i]-1] + heuristic[candidate[i]-1]) > \
                (distance[candidate[child]-1] + heuristic[candidate[child]-1]):
            candidate = swap(i, child)  # If the parents bigger than the child, we swap them
            siftdown(child)  # Then recursively call siftdown


def swap(a, b):  # Our function to swap our values
    candidate[a], candidate[b] = candidate[b], candidate[a]
    return candidate


def a_star():
    global adj_matrix, vertex_index, heap_size, starting_vertex, goal_vertex

    swap(starting_vertex-1, heap_size-1)  # We take our source vertex out of the heap

    heap_size -= 1  # Reduce the heap size by 1

    makeheap()  # And then restore the heap property

    while True:  # While we haven't found our goal vertex

        vertex_index = candidate[0] - 1  # The vertex index is the next in the heap

        swap(0, heap_size - 1)  # Swap it out with what's not in the heap

        heap_size -= 1  # Reduce the heap by 1

        if vertex_index+1 == goal_vertex:  # If we just selected the goal vertex, we can stop
            break

        siftdown(0)  # And now siftdown the value to restore the heap

        for u in range(0, heap_size):  # If not, we're going to calculate the new minimum distances from s

            # If this new vertex can get us to another vertex better than our current path
            if distance[vertex_index] + adj_matrix[vertex_index][candidate[u]-1] < distance[candidate[u]-1]:

                # We update the distance array to have a new minimum distance
                distance[candidate[u] - 1] = distance[vertex_index] + adj_matrix[vertex_index][candidate[u]-1]

                # And update the parent array to point to the parent of this vertex
                parent_array[candidate[u] - 1] = vertex_index

                siftup(u)  # And now it's likely our value is too low in the heap, so we sift it up


def reset_arrays():  # Our function to reset the arrays
    global candidate, parent_array, path, heap_size

    heap_size = n_vertices  # We reset the heap size

    for i in range(0, n_vertices):  # We have to remake the candidate, distance and parent arrays

        candidate[i] = i+1

        distance[i] = adj_matrix[starting_vertex-1][i]

        parent_array[i] = starting_vertex - 1  # And we fill the parent array with the index of the starting vertex


def second_shortest():  # Our function to calculate the second shortest path
    global path_index, second_shortest_path_length, starting_vertex, goal_vertex
    global shortest_path_index, second_shortest_path_index

    shortest_path_index = path_index  # We note the amount of edges in our shortest path
    path_index = 0  # And reset the path index, to override the path array with the different second shortest paths
    old_path_length = infinity  # And set our variable to hold the best path length we've seen so far

    for edge in range(0, shortest_path_index):  # For each edge in our shortest path
        i, j = shortest_path[edge], shortest_path[edge + 1]  # Get the indices for our adjacency matrix
        temp = (i, j, adj_matrix[i][j])  # Store the edge we just removed
        adj_matrix[i][j] = infinity  # And then set the adjacency matrix edges to infinity
        adj_matrix[j][i] = infinity  # For both entries
        reset_arrays()  # We reset our arrays and calculate the new distances with the amended adjacency matrix
        a_star()  # Call A* on this new graph
        create_paths()  # And create this second shortest path

        new_path_length = distance[vertex_index]  # We look at the length of this new path
        if new_path_length < old_path_length:  # If it's shorter than the old path
            for q in range(0, path_index + 1):  # We copy our 2nd shortest path into the 2nd shortest path array
                second_shortest_path[q] = path[q]
            second_shortest_path_length = new_path_length  # And store the length
            old_path_length = new_path_length  # The old path length is now the new path length
            second_shortest_path_index = path_index
        path_index = 0  # Reset the path_index to go again

        adj_matrix[i][j] = temp[2]  # Finally fix the adjacency matrix, to go again with the next edge
        adj_matrix[j][i] = temp[2]


def main():
    global adj_matrix, vertices, candidate, parent_array, path, distance
    global shortest_path, second_shortest_path, heuristic
    global starting_vertex, goal_vertex, shortest_path_length, second_shortest_path_length
    global n_vertices, n_edges, heap_size, path_index

    user_file = input("\nPlease enter the name of the input file: ")  # Request file name from user

    try:
        file = open(user_file)  # Try to open the file

    except FileNotFoundError:  # If it fails, close
        sys.exit("Error opening file. Program will exit.")

    line = file.readline().strip()  # Read in the first line

    n_vertices, n_edges = line.split()  # Record the number of vertices and edges

    n_vertices, n_edges = int(n_vertices), int(n_edges)

    heap_size = n_vertices  # Set the heap size

    # Adjust all our arrays with the correct dimensions
    adj_matrix = numpy.full((n_vertices, n_vertices), infinity, dtype=object)

    vertices = numpy.empty(n_vertices, dtype=object)

    candidate = numpy.empty(n_vertices, dtype=int)

    distance = numpy.empty(n_vertices, dtype=float)

    heuristic = numpy.empty(n_vertices, dtype=float)

    parent_array = numpy.empty(n_vertices, dtype=int)

    path = numpy.empty(n_vertices, dtype=int)

    shortest_path = numpy.empty(n_vertices, dtype=int)

    second_shortest_path = numpy.empty(n_vertices, dtype=int)

    for vertex in range(0, n_vertices):  # We read in all the vertices and store them in a vertices array
        line = file.readline().strip()
        label, x_pos, y_pos = line.split()
        label, x_pos, y_pos = int(label), float(x_pos), float(y_pos)
        vertices[vertex] = (label, x_pos, y_pos)

    for diagonal in range(0, n_vertices):  # We create a leading diagonal of 0's for the adjacency matrix
        adj_matrix[diagonal][diagonal] = 0

    for edge in range(0, n_edges):  # We read in all the edges and fill in the adjacency matrix with the information
        line = file.readline().strip()
        i, j, w = line.split()
        i, j, w = int(i), int(j), float(w)
        adj_matrix[i - 1][j - 1] = w
        if adj_matrix[j - 1][i - 1] < w:  # We check to see if there's two path length's and pick the shorter of the two
            adj_matrix[i - 1][j - 1] = adj_matrix[j - 1][i - 1]
        else:
            adj_matrix[j - 1][i - 1] = w  # Making sure our graph is mirrored around the leading diagonal

    line = file.readline().strip()
    s_vertex, g_vertex = line.split()  # Finally we read in our starting vertex and goal vertex
    s_vertex, g_vertex = int(s_vertex), int(g_vertex)

    starting_vertex, goal_vertex = s_vertex, g_vertex  # And store them in the variables

    calculate_heuristics(starting_vertex, goal_vertex)  # Calculate the heuristics

    a_star()  # Call our A* Algorithm Function for the shortest path

    create_paths()  # When we've found our goal vertex, call the function to create the shortest path

    for p in range(0, path_index + 1):  # We copy our shortest path into the shortest path array
        shortest_path[p] = path[p]

    shortest_path_length = distance[vertex_index]  # We store the shortest path length

    if shortest_path_length == infinity:  # Safeguards against no path existing, no second shortest path
        display_paths(starting_vertex, goal_vertex)
    else:
        second_shortest()  # If a path did exist. Call our array to work out the second shortest path.
        display_paths(starting_vertex, goal_vertex)  # And finally, we display the paths


main()  # Calling our main function
