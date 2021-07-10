# Discrete Event Simulation of Airport Check-in System
# Program reads in data and runs two simulations
# First simulation, servers only serve their specific customer type
# Second simulation, first class servers can serve tourist customers if the first class queue is empty
#

import sys

import numpy  # We will use numpy arrays for our assignment

# Critical Values

sim = 1  # Keeps track of which simulation we are in

time = 0  # Keeps track of the time

final = False  # A boolean value over whether or not we have reached the end of the file

heap_size = 0  # Keeps track of our heap size

temp_event = (0, 0, 0, 0, 0)  # (Time, Customer Type {0,1}, Service Duration, Server ID {0..Nb/Nt}, Server Type {0,1})

n_business_servers = 0  # Counts the number of business servers

n_busy_business = 0  # Counts the number of busy business servers

n_tourist_servers = 0  # Counts the number of tourist servers

n_busy_tourist = 0  # Counts the number of busy tourist servers

total_busy = 0  # Counts the total amount of busy servers (used for event_heap index)

busy_servers = 0  # A variable for our business and tourist busy servers

servers = 0  # Either a business or tourist server

# Pointers for Queues

b_queue_start = 0  # Tracks the start of business queue

t_queue_start = 0  # Tracks the start of tourist queue

b_queue_index = 0  # Keeps track of the next slot in the business queue

t_queue_index = 0  # Keeps track of the next slot in the tourist queue

b_queue_capacity = 0  # Tracks how many people in the business queue

t_queue_capacity = 0  # Tracks how many people in the tourist queue

# Pointers for Stacks

b_stack_size = 0  # Tracks the size of the business server stack

t_stack_size = 0  # Tracks the size of the tourist server stack

b_stack_top = 0  # Tracks the next server to pop in the business server stack

t_stack_top = 0  # Tracks the next server to pop in the tourist server stack

# Arrays

event_heap = numpy.empty(41, dtype=object)  # Where we store the next event to occur

business_queue = numpy.empty(500, dtype=object)  # Where we store waiting business passengers

tourist_queue = numpy.empty(500, dtype=object)  # Where we store waiting tourist passengers

business_server_stack = numpy.empty(20, dtype=int)  # Where we store idle business servers

tourist_server_stack = numpy.empty(20, dtype=int)  # Where we store idle tourist servers

business_busy_start_time = numpy.zeros(21, dtype=float)  # Stores the time each business server becomes busy

tourist_busy_start_time = numpy.zeros(21, dtype=float)  # Stores the time each tourist server becomes busy

business_busy_cumulative_time = numpy.zeros(21, dtype=float)  # Stores the cumulative time each business server is busy

tourist_busy_cumulative_time = numpy.zeros(21, dtype=float)  # Stores the cumulative time each tourist server is busy

# Counters for Statistics

customer_counter = 0  # Counts the number of customers

b_queue_time = 0  # For calculating the average service and queue time of the business customers

t_queue_time = 0  # For calculating the average service and queue time of the tourist customers

b_queue_change_time = 0  # Stores the time since the last business queue length change

b_cumulative_length = 0  # Stores the cumulative length of the business queue

t_queue_change_time = 0  # Stores the time since the last tourist queue length change

t_cumulative_length = 0  # Stores the cumulative length of the tourist queue

queue_change_time = 0  # Stores the time since the last change in either queue

queues_cumulative_length = 0  # Stores the cumulative length of both queues

b_service_time = 0  # For calculating the service time of business customers

t_service_time = 0  # For calculating the service time of tourist customers

n_business_customers = 0  # Total number of business customers

n_tourist_customers = 0  # Total number of tourist customers

max_business = 0  # Max size of business queue

max_tourist = 0  # Max size of tourist queue

max_total = 0  # Max total size of queues


def push(element):  # Our function to push the server onto the stack
    global business_server_stack, b_stack_top, b_stack_size, tourist_server_stack, t_stack_top, t_stack_size

    if element[4] == 1:  # If this is a business server
        if b_stack_top == b_stack_size:  # Return if stack is full
            return
        business_server_stack[b_stack_top] = element[3]  # Else store them and increment the counter
        b_stack_top += 1
        return

    elif element[4] == 0:  # If this is a tourist server
        if t_stack_top == t_stack_size:  # Return if stack is full
            return
        tourist_server_stack[t_stack_top] = element[3]  # Else store them and increment the counter
        t_stack_top += 1
        return


def pop(priority):  # Our function to pop the top server off of the stack
    global business_server_stack, b_stack_top, tourist_server_stack, t_stack_top

    if priority == 1:  # If we want a business server
        if b_stack_top == 0:  # Return if stack is empty
            return
        else:
            b_stack_top -= 1  # Else pop the next business server
            return business_server_stack[b_stack_top]

    elif priority == 0:  # If we want a tourist server
        if t_stack_top == 0:  # Return if stack is empty
            return
        else:
            t_stack_top -= 1  # Else pop the next tourist server
            return tourist_server_stack[t_stack_top]


def siftup(i):  # Our function to restore the min heap
    global event_heap

    if i == 0:  # If this is in the first slot, return
        return

    parent = (i - 1) // 2  # Calculate the parent slot
    if event_heap[parent] < event_heap[i]:  # Return if the parent is smaller than the child
        return
    else:
        event_heap = swap(i, parent)  # Else swap the parent and the child
        siftup(parent)  # And recursively sort the parent into position


def siftdown(i):  # Our function to siftdown the values to restore the min heap
    global event_heap

    child = (i * 2) + 1  # Calculate the left child
    if child < heap_size:  # We ensure that we do not fall off the end of the array
        if child + 1 < heap_size:  # We check to see whether there is a left and right child or just a left
            if event_heap[child] > event_heap[child + 1]:  # We test against the smallest child
                child += 1
        if event_heap[i] > event_heap[child]:  # And check if we need to swap the values
            event_heap = swap(i, child)  # If so, we swap and recursively repeat the siftdown function
            siftdown(child)


def swap(a, b):  # Our function to swap our values
    event_heap[a], event_heap[b] = event_heap[b], event_heap[a]
    return event_heap


def max_queue_length(business, tourist):  # Our function to calculate the maximum length of each queue
    global max_business, max_tourist, max_total

    if business > max_business:  # Sets the new business max
        max_business = business
    if tourist > max_tourist:  # Sets the new tourist max
        max_tourist = tourist
    if (business + tourist) > max_total:  # Sets the new total max
        max_total = (business + tourist)


def enqueue(element):  # Our function to enqueue a customer
    global b_queue_index, b_queue_capacity, t_queue_index, t_queue_capacity, time
    global b_queue_change_time, t_queue_change_time, b_cumulative_length, t_cumulative_length
    global queues_cumulative_length, queue_change_time

    if element[1] == 1:  # If this is a business customer
        if b_queue_capacity == 500:  # If our queue is full, return
            return
        business_queue[b_queue_index] = element  # Place the customer in the queue and increment the counters
        b_queue_index += 1
        if b_queue_index > 499:  # If our index is over, go back to the start
            b_queue_index = 0
        b_cumulative_length += ((time - b_queue_change_time) * b_queue_capacity)  # Calculate the queue length changes
        b_queue_change_time = time  # And note the time it changed
        queues_cumulative_length += (
                    (time - queue_change_time) * (b_queue_capacity + t_queue_capacity))  # For both queues
        queue_change_time = time
        b_queue_capacity += 1  # Increment the business queue capacity
        max_queue_length(b_queue_capacity, t_queue_capacity)  # And check the max length of the queues
        return

    elif element[1] == 0:  # If this is a tourist passenger
        if t_queue_capacity == 500:  # If our queue is full, return
            return
        tourist_queue[t_queue_index] = element  # Place the customer in the queue and increment the counters
        t_queue_index += 1
        if t_queue_index > 499:  # If our index is over, go back to the start
            t_queue_index = 0
        t_cumulative_length += ((time - t_queue_change_time) * t_queue_capacity)  # Calculate the queue length changes
        t_queue_change_time = time  # And note the time it changed
        queues_cumulative_length += (
                    (time - queue_change_time) * (b_queue_capacity + t_queue_capacity))  # For both queues
        queue_change_time = time
        t_queue_capacity += 1  # Increment the tourist queue capacity
        max_queue_length(b_queue_capacity, t_queue_capacity)  # And check the max length of the queues
        return


def dequeue(priority):  # Our function to remove someone from the queue
    global b_queue_start, b_queue_index, b_queue_capacity, t_queue_start, t_queue_index, t_queue_capacity
    global time, b_queue_time, t_queue_time, queues_cumulative_length, queue_change_time
    global b_cumulative_length, b_queue_change_time, t_cumulative_length, t_queue_change_time

    if priority == 1:  # If we want to remove a business customer
        if b_queue_start == b_queue_index and b_queue_capacity == 0:  # Check if there's anyone there first
            return
        else:
            element = business_queue[b_queue_start]  # Grab the customer and increment the counters
            b_queue_start += 1
            if b_queue_start > 499:  # If our starting index is over, go back to the start
                b_queue_start = 0
            b_cumulative_length += ((time - b_queue_change_time) * b_queue_capacity)  # Add the cumulative busy time
            b_queue_change_time = time  # Note the time the queue changed size
            queues_cumulative_length += ((time - queue_change_time) * (b_queue_capacity + t_queue_capacity))
            queue_change_time = time  # Also doing so for the total queues
            b_queue_capacity -= 1  # Reduce the queue capacity
            b_queue_time += (time - element[0])  # Increment the queue time
            max_queue_length(b_queue_capacity, t_queue_capacity)  # Check max queue length
        return element  # Return the customer

    elif priority == 0:  # If we want to remove a tourist customer
        if t_queue_start == t_queue_index and t_queue_capacity == 0:  # Check if there's anyone there first
            return
        else:
            element = tourist_queue[t_queue_start]  # Grab the customer and increment the counters
            t_queue_start += 1
            if t_queue_start > 499:  # If our starting index is over, go back to the start
                t_queue_start = 0
            t_cumulative_length += ((time - t_queue_change_time) * t_queue_capacity)  # Add the cumulative busy time
            t_queue_change_time = time  # Note the time the queue changed size
            queues_cumulative_length += ((time - queue_change_time) * (b_queue_capacity + t_queue_capacity))
            queue_change_time = time  # Also doing so for the total queues
            t_queue_capacity -= 1  # Reduce the queue capacity
            t_queue_time += (time - element[0])  # Increment the queue time
            max_queue_length(b_queue_capacity, t_queue_capacity)  # Check max queue length
        return element  # Return the customer


def process_arrival(current_customer, next_arrival, priority, next_service):  # Our function to process a new customer
    global time, heap_size, n_busy_business, n_busy_tourist, total_busy, busy_servers, servers

    time = current_customer[0]  # Set the time to the time of the arrival
    next_customer = create_customer(next_arrival, priority, next_service)  # Create the next customer
    event_heap[0] = next_customer  # Store them in the first slot of the events
    siftdown(0)  # And sift them down to the correct position

    if temp_event[1] == 1:  # If the current customer is a business class customer
        busy_servers = n_busy_business  # We're referring to business servers
        servers = n_business_servers
    elif temp_event[1] == 0:  # If they're a tourist class customer
        busy_servers = n_busy_tourist  # We're referring to tourist servers
        servers = n_tourist_servers

    if busy_servers < servers:  # Check if there is an available server
        if temp_event[1] == 1:  # If we're serving a business customer
            n_busy_business += 1  # Make a business server busy
            total_busy = n_busy_business + n_busy_tourist  # Calculate total busy and store event at end of event heap
            event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(1), temp_event[1])
            business_busy_start_time[event_heap[total_busy][3]] = time  # Note the time this server starts being busy

        elif temp_event[1] == 0:  # If we're serving a tourist customer
            n_busy_tourist += 1  # Make a tourist server busy
            total_busy = n_busy_business + n_busy_tourist  # Calculate total busy and store event at end of event heap
            event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(0), temp_event[1])
            tourist_busy_start_time[event_heap[total_busy][3]] = time  # Note the time this server starts being busy

        heap_size += 1  # Increase the heap size
        siftup(total_busy)  # And place this new service in the appropriate chronological position

    else:  # If there's no one free
        if sim == 1:  # In our first run through we stick them in a queue
            enqueue(current_customer)
        elif sim == 2:  # In our second run through, if all our tourist servers are busy
            if n_busy_business < n_business_servers:  # If there's an idle business server
                n_busy_business += 1  # We make them busy
                total_busy = n_busy_business + n_busy_tourist  # And they serve this tourist customer
                event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(1), 1)
                business_busy_start_time[event_heap[total_busy][3]] = time  # We note the busy start time
                heap_size += 1  # Increment the heap size and restore the heap property
                siftup(total_busy)
            else:  # If no one is free, then we enqueue the customer as normal
                enqueue(current_customer)
    return


def queue_empty(priority):  # Our function to see if the appropriate queue is empty
    if priority == 1:
        return bool(b_queue_capacity == 0)  # Checks if business queue is empty
    elif priority == 0:
        return bool(t_queue_capacity == 0)  # Checks if tourist queue is empty


def process_service_end():  # Our function to process a service completion for Simulation 1
    global time, heap_size, final, n_busy_business, n_busy_tourist, total_busy
    global b_service_time, t_service_time

    time = event_heap[0][0]  # Set the time to the time the completion happens
    if event_heap[0][1] == 1:  # Check customer class and note service time for our stats
        b_service_time += event_heap[0][2]
    elif event_heap[0][1] == 0:
        t_service_time += event_heap[0][2]
    if queue_empty(event_heap[0][4]):  # Check the appropriate queue for more waiting customers
        if event_heap[0][4] == 1:  # If this is a business class server
            push(event_heap[0])  # Stick them back on their stack, and note the time for our stats
            business_busy_cumulative_time[event_heap[0][3]] += (time - business_busy_start_time[event_heap[0][3]])
            n_busy_business -= 1  # Reduce the busy count by 1
        elif event_heap[0][4] == 0:  # If this was a tourist server
            push(event_heap[0])  # Stick them back on their stack, and note the time for our stats
            tourist_busy_cumulative_time[event_heap[0][3]] += (time - tourist_busy_start_time[event_heap[0][3]])
            n_busy_tourist -= 1  # Reduce the busy count by 1
        if final:  # If we have already reached the end of file, we reduce the busy count first then adjust the heap
            total_busy -= 1
            event_heap[0] = event_heap[total_busy]
            heap_size -= 1
        else:  # If not, we adjust heap first, then reduce busy count
            event_heap[0] = event_heap[total_busy]
            total_busy -= 1
            heap_size -= 1
    else:  # If there are customers waiting
        next_customer = dequeue(event_heap[0][1])  # Get the next customer and add them to the event heap
        event_heap[0] = (
        time + next_customer[2], next_customer[1], next_customer[2], event_heap[0][3], next_customer[1])
    siftdown(0)  # Restore the min heap
    return


def process_service_end_2():  # Our function to process a service completion for Simulation 2
    global time, heap_size, final, n_busy_business, n_busy_tourist, total_busy
    global b_service_time, t_service_time

    time = event_heap[0][0]  # Set the time to the time the completion happens
    if event_heap[0][1] == 1:  # Check customer class and note service time for our stats
        b_service_time += event_heap[0][2]
    elif event_heap[0][1] == 0:
        t_service_time += event_heap[0][2]
    if queue_empty(event_heap[0][4]):  # Check the appropriate queue for more waiting customers
        if event_heap[0][4] == 1:  # If this is a business class server
            if queue_empty(0):  # If the tourist queue is empty
                push(event_heap[0])  # Then place them back on the stack and note the stats
                business_busy_cumulative_time[event_heap[0][3]] += (time - business_busy_start_time[event_heap[0][3]])
                n_busy_business -= 1  # Reduce the busy count by one
            else:
                next_customer = dequeue(0)  # If their are tourist customers waiting and a free business server
                event_heap[0] = (time + next_customer[2], next_customer[1], next_customer[2], event_heap[0][3], 1)
                siftdown(0)  # Get the next customer, add them to the event heap, and restore the heap property
                return
        elif event_heap[0][4] == 0:  # If this is instead a tourist server
            push(event_heap[0])  # Stick them back on their stack, and note the time for our stats
            tourist_busy_cumulative_time[event_heap[0][3]] += (time - tourist_busy_start_time[event_heap[0][3]])
            n_busy_tourist -= 1  # Reduce the busy count by one
        if final:  # If we have already reached the end of file, we reduce the busy count first then adjust the heap
            total_busy -= 1
            event_heap[0] = event_heap[total_busy]
            heap_size -= 1
        else:  # If not, we adjust heap first, then reduce busy count
            event_heap[0] = event_heap[total_busy]
            total_busy -= 1
            heap_size -= 1
    else:  # If there are customers waiting
        next_customer = dequeue(event_heap[0][4])  # Get the next customer and add them to the event heap
        event_heap[0] = (
        time + next_customer[2], next_customer[1], next_customer[2], event_heap[0][3], event_heap[0][4])
    siftdown(0)  # Restore the min heap
    return


def create_customer(next_arrival, priority, next_service):  # Our function to create a new customer
    customer = (next_arrival, priority, next_service, 0, priority)
    # (Time, Customer Type, Service Duration, Server ID, Server Type)
    return customer


def process_final(current_customer):  # Our function to process the final customer
    global time, heap_size, final, busy_servers, servers, total_busy, n_busy_business, n_busy_tourist

    time = current_customer[0]  # Set the time to the final customer
    final = True  # And change the boolean value

    if current_customer[1] == 1:  # Check the customer type to refer to the correct server type
        busy_servers = n_busy_business
        servers = n_business_servers
    elif current_customer[1] == 0:
        busy_servers = n_busy_tourist
        servers = n_tourist_servers

    if busy_servers < servers:  # If there's a free server
        if temp_event[1] == 1:  # If this is a business class server
            n_busy_business += 1  # Make them busy
            total_busy = n_busy_business + n_busy_business  # Adjust stats and stick them at the end of the event heap
            event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(1), temp_event[1])
            business_busy_start_time[event_heap[total_busy][3]] = time

        elif temp_event[1] == 0:  # If this is a tourist class server
            n_busy_tourist += 1  # Make them busy
            total_busy = n_busy_business + n_busy_tourist  # Adjust stats and stick them at the end of the event heap
            event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(0), temp_event[1])
            tourist_busy_start_time[event_heap[total_busy][3]] = time

        heap_size += 1  # Increment the heap size
        siftup(total_busy)  # Put them in the correct position

    else:  # If there's no one available
        if sim == 1:  # If this is Simulation 1, enqueue them
            enqueue(current_customer)
        elif sim == 2:  # If this is Simulation 2
            if n_busy_business < n_business_servers:  # See if there's a free business server
                n_busy_business += 1  # If there is, make them busy
                total_busy = n_busy_business + n_busy_tourist  # Adjust stats and stick them at the end of the heap
                event_heap[total_busy] = (time + temp_event[2], temp_event[1], temp_event[2], pop(1), 1)
                business_busy_start_time[event_heap[total_busy][3]] = time
                heap_size += 1  # Increment the heap size
                siftup(total_busy)  # And restore the heap property
            else:
                enqueue(current_customer)  # If there's no one free, enqueue them

    event_heap[0] = event_heap[total_busy]  # Now remove the arrival event of the customer we just processed
    heap_size -= 1
    siftdown(0)  # And restore the heap property
    return


def reset_counters():  # Our function to reset all of the counters for our second simulation run
    global time, final, b_queue_start, b_queue_index, t_queue_start, t_queue_index, customer_counter
    global event_heap, business_queue, tourist_queue, business_server_stack, tourist_server_stack
    global b_queue_time, b_service_time, n_business_customers, t_queue_time, t_service_time, n_tourist_customers
    global b_cumulative_length, t_cumulative_length, b_queue_change_time, t_queue_change_time
    global queues_cumulative_length, queue_change_time, max_business, max_tourist, max_total
    global business_busy_start_time, business_busy_cumulative_time
    global tourist_busy_start_time, tourist_busy_cumulative_time

    # Resetting all the counters
    time = 0
    final = False
    b_queue_start = 0
    t_queue_start = 0
    b_queue_index = 0
    t_queue_index = 0
    customer_counter = 0
    b_queue_time = 0
    b_service_time = 0
    n_business_customers = 0
    t_queue_time = 0
    t_service_time = 0
    n_tourist_customers = 0
    b_cumulative_length = 0
    t_cumulative_length = 0
    b_queue_change_time = 0
    t_queue_change_time = 0
    queues_cumulative_length = 0
    queue_change_time = 0
    max_business = 0
    max_tourist = 0
    max_total = 0

    # Resetting the arrays
    event_heap = numpy.empty(41, dtype=object)
    business_queue = numpy.empty(500, dtype=object)
    tourist_queue = numpy.empty(500, dtype=object)
    business_server_stack = numpy.empty(20, dtype=int)
    tourist_server_stack = numpy.empty(20, dtype=int)
    business_busy_start_time = numpy.zeros(21, dtype=float)
    tourist_busy_start_time = numpy.zeros(21, dtype=float)
    business_busy_cumulative_time = numpy.zeros(21, dtype=float)
    tourist_busy_cumulative_time = numpy.zeros(21, dtype=float)


def display_stats():  # Our function to display all our gathered statistics from the simulations

    # Calculate our business statistics
    try:
        b_average_time = (b_queue_time + b_service_time) / n_business_customers
        b_average_queue_time = (b_queue_time / n_business_customers)
        b_ave_length_queue = (b_cumulative_length / time)
    except ZeroDivisionError:  # Just in case any of our simulations are only one kind of passenger
        b_average_time = 0
        b_average_queue_time = 0
        b_ave_length_queue = 0

    # Calculate our tourist statistics
    try:
        t_average_time = (t_queue_time + t_service_time) / n_tourist_customers
        t_average_queue_time = (t_queue_time / n_tourist_customers)
        t_ave_length_queue = (t_cumulative_length / time)
    except ZeroDivisionError:
        t_average_time = 0
        t_average_queue_time = 0
        t_ave_length_queue = 0

    # Calculate our combined statistics
    try:
        average_time = (b_queue_time + b_service_time + t_queue_time + t_service_time) / customer_counter
        average_queue_time = (b_queue_time + t_queue_time) / customer_counter
        ave_length_queue = (queues_cumulative_length / time)
    except ZeroDivisionError:
        average_time = 0
        average_queue_time = 0
        ave_length_queue = 0

    # Display all the results
    if sim == 1:
        print("\nPass 1: Business servers exclusively serve business class\n")
    elif sim == 2:
        print("\n\nPass 2: Idle business servers may serve tourist class\n")

    print("{0:<40} {1:>15}".format("Number of people served:", customer_counter))
    print("{0:<40} {1:>15.2f}".format("Time last service is completed: ", time))
    print("\nBusiness class customers:")
    print("{0:<40} {1:>15.2f}".format("Average total service time:", b_average_time))
    print("{0:<40} {1:>15.2f}".format("Average total time in queue:", b_average_queue_time))
    print("{0:<40} {1:>15.2f}".format("Ave length of queue:", b_ave_length_queue))
    print("{0:<40} {1:>15}".format("Maximum number queued:", max_business))
    print("\nTourist class customers:")
    print("{0:<40} {1:>15.2f}".format("Average total service time:", t_average_time))
    print("{0:<40} {1:>15.2f}".format("Average total time in queue:", t_average_queue_time))
    print("{0:<40} {1:>15.2f}".format("Ave length of queue:", t_ave_length_queue))
    print("{0:<40} {1:>15}".format("Maximum number queued:", max_tourist))
    print("\nAll customers:")
    print("{0:<40} {1:>15.2f}".format("Average total service time:", average_time))
    print("{0:<40} {1:>15.2f}".format("Average total time in queue:", average_queue_time))
    print("{0:<40} {1:>15.2f}".format("Ave length of queue:", ave_length_queue))
    print("{0:<40} {1:>15}".format("Maximum number queued:", max_total))

    print("\nBusiness class servers:")
    for b in range(1, n_business_servers + 1):
        print("Total idle time for business class server {0:>2}: {1:>10.2f}"
              .format(b, time - business_busy_cumulative_time[b]))

    print("\nTourist class servers:")
    for t in range(1, n_tourist_servers + 1):
        print("Total idle time for tourist class server {0:>2}: {1:>11.2f}"
              .format(t, time - tourist_busy_cumulative_time[t]))


def get_file():  # Our function to get the name of the user's file
    input_file = input("Please enter the input filename: ")  # We request the user's file name
    return input_file  # We put this outside our main function as we will need to run our sim twice


def main(file):  # Our main function to continuously read in customers and process their services
    global heap_size, temp_event, customer_counter, sim
    global n_business_servers, n_tourist_servers, b_stack_top, t_stack_top, b_stack_size, t_stack_size
    global n_business_customers, n_tourist_customers

    # We first read in how many servers of each type we have
    n_business_servers, n_tourist_servers = file.readline().split()
    n_business_servers, n_tourist_servers = int(n_business_servers), int(n_tourist_servers)

    # We populate our business server stacks backwards (so Server 1 is popped first) and set the appropriate counters
    for i in range(0, n_business_servers):
        business_server_stack[i] = n_business_servers - i
    b_stack_top = n_business_servers
    b_stack_size = n_business_servers

    # We do the same thing for the tourist server stack
    for j in range(0, n_tourist_servers):
        tourist_server_stack[j] = n_tourist_servers - j
    t_stack_top = n_tourist_servers
    t_stack_size = n_tourist_servers

    arrival_time, customer_type, service_time = file.readline().split()  # We read in the first arrival

    next_arrival, priority, next_service = float(arrival_time), int(customer_type), float(service_time)

    customer = create_customer(next_arrival, priority, next_service)  # And create an event struct out of them

    event_heap[0] = customer  # We stick them at the start of the heap

    heap_size += 1  # And increment the heap size by 1

    while heap_size > 0:  # While there are still events to process

        if event_heap[0][3] == 0:  # If the next event is an arrival
            customer_counter += 1  # Increment the customer counters appropriate to their class
            if event_heap[0][1] == 1:
                n_business_customers += 1
            elif event_heap[0][1] == 0:
                n_tourist_customers += 1
            temp_event = event_heap[0]  # Stick their information in a temporary event struct
            arrival_time, customer_type, service_time = file.readline().split()  # Read in the next arrival
            next_arrival, priority, next_service = float(arrival_time), int(customer_type), float(service_time)
            if next_arrival == 0 and next_service == 0:  # If we reach our EOF condition
                process_final(event_heap[0])  # We call the final function
            else:  # Else we process the current arrival at the top of the heap
                process_arrival(event_heap[0], next_arrival, priority, next_service)

        else:  # If this is a service completion, we call the appropriate function for the simulation we are in
            if sim == 1:
                process_service_end()
            elif sim == 2:
                process_service_end_2()
    display_stats()  # We call our function to display the stats for that simulation
    reset_counters()  # And reset our counters for the next simulation


user_file = get_file()  # First we read in the user file name

while sim < 3:  # We use a while loop to run the simulation twice
    try:  # Try to open the file
        f = open(user_file)
    except FileNotFoundError:  # If we can't open the file, close the program
        print("Error opening file. Program will exit.")
        sys.exit(0)
    main(f)  # Call our main function
    sim += 1  # Increment the simulation counter
