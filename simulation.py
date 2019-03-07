#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import csv
import random
import argparse


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

    def __init__(self, time, prnttime):
        self.timestamp = time
        self.request_time = prnttime

    def get_stamp(self):
        return self.timestamp

    def get_request_time(self):
        return self.request_time

    def wait_time(self, current_time):
        return current_time - self.timestamp
