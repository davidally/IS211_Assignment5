#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import csv
import random
import argparse
from decimal import Decimal


class Queue(object):
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

    response = urllib2.Request(file)
    raw_data = urllib2.urlopen(response)
    parsed_data = csv.reader(raw_data)

    init_list = []

    for row in parsed_data:
        init_list.append(row)

    return init_list


def simulateOneServer(url):

    # Initialize Server and Queue
    single_server = Server()
    server_queue = Queue()

    # Check if server is up
    try:
        if single_server:
            server_running = True
    except Exception:
        print 'Server is not functioning correctly.'
        return

    # Grab requests
    requests = processRequests(url)

    time_now = 0
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

    avg_wait = Decimal(sum(waiting_times)) / Decimal(len(waiting_times))
    print 'The average wait time is {} seconds'.format(avg_wait)


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--file', action='store', type=str,
                       help='Enter valid link to CSV file.')
    args = parse.parse_args()

    simulateOneServer(args.file)


if __name__ == '__main__':
    main()
