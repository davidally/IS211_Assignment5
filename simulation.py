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


def simulateOneServer():

    URL = 'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'

    single_server = Server()
    server_queue = Queue()
    # Check if server is up
    try:
        if single_server:
            server_running = True
    except Exception:
        print 'Server is not running.'
        return

    # Grab requests
    requests = processRequests(URL)

    # Load requests into server queue
    for row in requests:
        new_request = Request(row[0], row[2])
        server_queue.enqueue(new_request)

    queue_has_tasks = True if server_queue.items else False
    # Server will process the queue
    while server_running:
        if queue_has_tasks == True and not single_server.busy():
            process_item = server_queue.dequeue()
            single_server.start_next(process_item)

    return


simulateOneServer()


# def main():

#     req_file = 'test'


# if __name__ == '__main__':
#     main()
