#!/usr/bin/python

from hashlib import md5

class Singleton(object):

    _singleton = {}

    def __new__(cls, *args, **kwargs):
        hash = md5(cls.__name__ + str(args) + str(kwargs)).hexdigest()

        if hash not in cls._singleton:
            cls._singleton[hash] = super(Singleton, cls).__new__(cls)
        return cls._singleton[hash]
