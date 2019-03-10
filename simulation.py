#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import csv
import random
import argparse
from decimal import Decimal


class Queue(object):
    """
    Defining Queue abstract data type.
    """

    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server(object):
    """
    Creates a simulation of a printing server.
    """

    def __init__(self):
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None

    def busy(self):
        if self.current_task != None:
            return True
        else:
            return False

    def start_next(self, new_task):
        self.current_task = new_task
        self.time_remaining = new_task.get_request_time()


class Request(object):
    """
    Creates a simulated printer task.
    """

    def __init__(self, time, process_time):
        self.timestamp = time
        self.request_time = process_time

    def get_stamp(self):
        return self.timestamp

    def get_request_time(self):
        return self.request_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


def processRequests(file):
    """Pulls data from a CSV file and makes it more usable.

    Args:
        file (str): Link to a valid CSV file.

    Returns:
        list: A list of arrays.
    """

    response = urllib2.Request(file)
    raw_data = urllib2.urlopen(response)
    parsed_data = csv.reader(raw_data)

    init_list = []

    for row in parsed_data:
        init_list.append(row)

    return init_list


def simulateOneServer(url):
    """This will process a CSV file and transform each line
    into a Request object. This request will then be loaded
    into a queue for a simulated server to process. 

    Args:
        url (str): A link to a valid CSV file. 
    """

    # Initialize Server and Queue
    single_server = Server()
    server_queue = Queue()

    # Check if server is up
    try:
        server_running = True if single_server else False
    except Exception:
        print 'Server is not functioning correctly.'
        return

    # Grab requests
    requests = processRequests(url)
    time_now = 8

    # Load into Queue
    for row in requests:
        new_request = Request(int(row[0]), int(row[2]))
        server_queue.enqueue(new_request)

    waiting_times = []
    while server_running:
        if (not server_queue.is_empty()) and (not single_server.busy()):
            process_item = server_queue.dequeue()
            waiting_times.append(process_item.wait_time(time_now))
            single_server.start_next(process_item)

        single_server.tick()
        time_now += 1

        if server_queue.is_empty():
            break

    avg_wait = time_now / (Decimal(sum(waiting_times)) /
                           Decimal(len(waiting_times)))
    print 'The average wait time is {} seconds'.format(avg_wait)
    return avg_wait


def simulateManyServers(url, servers_num):

    # Generate and package servers and queues
    total_servers = [Server() for _ in range(servers_num)]
    total_queues = [Queue() for _ in range(servers_num)]
    servers_config = zip(total_servers, total_queues)
    test = True

    # Grab requests
    requests = processRequests(url)

    # Load requests into queue
    server_counter = 0
    for request in requests:
        new_request = Request(int(request[0]), int(request[2]))
        servers_config[server_counter][1].enqueue(new_request)
        if server_counter < (servers_num - 1):
            server_counter += 1
        else:
            server_counter = 0

    # Processing server queues
    server_averages = []
    for server in servers_config:
        time_now = 0
        waiting_times = []
        while test:
            if (not server[1].is_empty()) and (not server[0].busy()):
                process_item = server[1].dequeue()
                waiting_times.append(process_item.wait_time(time_now))
                server[0].start_next(process_item)

            server[0].tick()
            time_now += 1

            if server[1].is_empty():
                break

        avg_wait = time_now / \
            (Decimal(sum(waiting_times)) / Decimal(len(waiting_times)))
        server_averages.append(avg_wait)

    total_averages = Decimal(sum(server_averages)) / \
        Decimal(len(server_averages))

    # Just testing argparse
    print 'There are {} servers! The average processing time of these servers is {}'.format(
        servers_num, total_averages)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--file', action='store', type=str,
                       help='Enter valid link to CSV file.')
    parse.add_argument('-s', '--servers', action='store',
                       type=int, required=False, help='Enter number of servers to simulate')
    args = parse.parse_args()

    if args.servers is not None:
        simulateManyServers(args.file, args.servers)
    else:
        simulateOneServer(args.file)


if __name__ == '__main__':
    main()
