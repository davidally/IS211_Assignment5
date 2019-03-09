#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import csv
import random
import argparse
import decimal


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

    response = urllib2.urlopen(file)
    parsed_data = csv.reader(response)

    init_list = []

    for row in parsed_data:
        init_list.append(row)

    return init_list


def simulateOneServer(url):

    # URL = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'

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

    # Grab requests and load into queue
    requests = processRequests(url)
    for row in requests:
        new_request = Request(row[0], row[2])
        server_queue.enqueue(new_request)

    # Check queue has items
    queue_has_tasks = True if server_queue.items else False

    # Server will process the queue
    while server_running:
        if queue_has_tasks and not single_server.busy():
            process_item = server_queue.dequeue()
            single_server.start_next(process_item)

        # single_server.tick()

    return


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('--file', action='store', type=str,
                       help='Enter valid link to CSV file.')
    args = parse.parse_args()

    simulateOneServer(args.file)


if __name__ == '__main__':
    main()
