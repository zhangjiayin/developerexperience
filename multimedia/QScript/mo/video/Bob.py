#!/usr/bin/env python

import sys, time
from daemon import Daemon
import config
import random
import threading
import Queue
from BobUtil import *

from Processor import *
from log import log, ring
class bob(Daemon):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        Daemon.__init__(self,pidfile, stdin, stdout, stderr)
        self.jobs = Queue.Queue(0)
        self.result = Queue.Queue(0)
        self.workers = []

    def run(self):

        job_getor = threading.Thread(target=self.genJob)
        job_getor.start()

        result_processor = threading.Thread(target=self.processResult)
        result_processor.start()

        for n in xrange(config.THREAD_LIMIT):
            worker_t = threading.Thread(target=self.worker)
            worker_t.setDaemon(True)
            worker_t.start()
            self.workers.append(worker_t)

        for w in self.workers:
            w.join()

        result_processor.join()
        job_getor.join()

    def worker(self):
        """
        worker
        """
        while True:
            try:
                r = self.jobs.get(True, 5);
                result = r.callable(*r.args, **r.kwds)
                self.result.put((r, result))
            except Exception, e:
                pass
            time.sleep(1)

    def processResult(self):
        while True:
            try:
                req,res = self.result.get(True, 5)
                Processor.processResult(res,req)
            except Exception, e:
                pass
            time.sleep(.1)

    def genJob(self):
        while True:
            try:
                requests = Processor.getJob()
                if requests == []:
	 	    ring()
                    sys.stdout.flush()
                else:
	 	    ring()
                    for r in requests:
                        self.jobs.put(r,True, 5)
                        self.jobs.task_done()
            except Exception, e:
                print e
            time.sleep(1)


