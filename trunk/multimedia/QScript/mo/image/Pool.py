#!/usr/bin/python
# -*- coding: utf-8 -*-

from Queue import Queue, Full, Empty

class Pool(Queue):
    """ Manage a fixed-size pool of reusable, identical objects """

    def __init__(self, constructor, poolsize=5):
        self.queue = Queue(poolsize)
        self.constructor = constructor
        for x in range(poolsize):
            self.queue.put(self.constructor())

    def get(self, block=0):
        """ Get an object from the pool or create a new one if pool is empty """

        try:
            return self.queue.get(block)
        except Empty:
            self.queue.put(self.constructor())

            return self.constructor()

    def put(self, obj, block=0):
        """ Put an object into the pool if it is not full.The caller must not use the object after this. """
        try:
            self.queue.put(obj, block)
        except Full:
            return True

    def restore(self, obj, block=0):
        """ Restore an object into the pool """
        return self.put(obj, block)

    def check(self):
        return self.queue.qsize()

class Constructor:

    """ Return a constructor that returns apply(function, args, kwargs) when called. """

    def __init__(self, function, *args, **kwargs):
        self.f = function
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return apply(self.f, self.args, self.kwargs)
