#!/usr/bin/env python
import threading, time, random,cmemcached
import getopt,sys 
import redis

class testObj():
    def __init__(self,id):
	self.id = id

class BenchMarker(threading.Thread):

    def __init__ (self, id, write_time=0, read_time=0):
        super(BenchMarker,self).__init__()
	self.write_time = write_time
	self.read_time = read_time
	self.id = id
	self.client = redis.Redis(host="192.168.3.155")
	self.client.connect()
	
    def run (self):
	start = time.time()
	out =  "thread :" + str(self.id) + " write : " + str(self.write_time)  + " times " \
		" get : " + str(self.read_time)  + " times "
	self.test()
	end   = time.time()
	print out + "cost: " + str(end - start) + "seconds"

    def test (self):
	if (self.write_time == 0):
		for x in xrange(self.read_time):
			self.readTest()
		return True

	if (self.read_time == 0):
		for x in xrange(self.write_time):
			self.writeTest()
		return True
	
	for x in xrange(self.write_time + self.read_time):

		if(self.read_time <= 0):
			self.writeTest()
			self.write_time-=1
			continue

		if(self.write_time <= 0):
			self.readTest()
			self.read_time-=1
			continue

		if(random.randint(0,1) == 1 ):
			self.writeTest()
			self.write_time-=1
		else:
			self.readTest()
			self.read_time-=1

    def writeTest(self):
	key   = "prefix1_" + str(random.randint(1,random_key_range))
	value = random.randint(1,random_val_range)
	if is_obj:
	    value = testObj(value)
	self.client.set(key, value)
	
    def readTest(self):
	key   = "prefix1_" + str(random.randint(1,random_key_range))
	self.client.get(key)

if __name__ == '__main__':

	
    def	Usage():
	print 
        print "python reids benchmark"
	print "   -k --key       int type key random range default 10000000"
	print "   -v --val       int type value random range default 10000000"
	print "   -p --poolsize  thread workers num default 10 "
	print "   -w --writetime write times per thread default 1000"
	print "   -r --readtime  read  times per thread default 1000"
	print "   -o --testobj   test get or set obj"
	print "   -h --help      print this usage"
	print "   TODO big object set and get , multi set and get"

    random_key_range = 10000000
    random_val_range = 10000000

    write_time  = 1000
    read_time   = 1000
    pool_size   = 10
    is_obj 	= False
    opts,args=getopt.getopt(sys.argv[1:],'k::v::p::w::r::oh', "key=,value=, poolsize=, help")
	
    for a, o in opts:
	if a in("-k", "--key"):
	    random_key_range = int(o)
	if a in("-v", "--value"):
	    random_val_range = int(o)
	if a in("-p", "--poolsize"):
	    pool_size = int(o)
	if a in("-w", "--writetime"):
	    write_time = int(o)
	if a in("-r", "--readtime"):
	    read_time = int(o)
	if a in("-h", "--help"):
	    Usage()
	    sys.exit()

    pool = []	

    for i in xrange(pool_size):
	pool.append(BenchMarker(i, write_time=write_time, read_time=read_time))
    start = time.time()

    for t in pool:
	t.start()
    for t in pool:
	t.join()

    end = time.time()
	
    cost = end - start
    print str(pool_size) + " threads "  + "cost:" + str(cost) + " seconds"
    print "finish"
