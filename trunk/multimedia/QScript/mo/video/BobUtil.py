import urllib2
import urllib
import sys
if sys.version_info[1] < 6:	
    import simplejson as json
else:
    import json


def _handle_thread_exception(request, exc_info):
    traceback.print_exception(*exc_info)

def makeRequests(callable_, args_list, callback=None,
        exc_callback=_handle_thread_exception):
    requests = []
    for item in args_list:
        if isinstance(item, tuple):
            requests.append(
                WorkRequest(callable_, item[0], item[1], callback=callback,
                    exc_callback=exc_callback)
            )
        else:
            requests.append(
                WorkRequest(callable_, [item], None, callback=callback,
                    exc_callback=exc_callback)
            )
    return requests

class WorkRequest:
    def __init__(self, callable_, args=None, kwds=None, requestID=None,
            callback=None, exc_callback=_handle_thread_exception):
        if requestID is None:
            self.requestID = id(self)
        else:
            try:
                self.requestID = hash(requestID)
            except TypeError:
                raise TypeError("requestID must be hashable.")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "<WorkRequest id=%s args=%r kwargs=%r exception=%s>" % \
            (self.requestID, self.args, self.kwds, self.exception)


def httprequest(url, data={},headers={}, method="get"):
    """return a dict if json decode succeed
    otherwise return response string"""

    if url.find("http://") != 0:
        url  = "http://" + url
        pass

    if method.lower() == "get" and data != None :
        if url.find('?') == -1:
            url = url + "?" + urllib.urlencode(data)
            pass
        else:
            url = url + "&" + urllib.urlencode(data)
            pass
        data = None

    if data != None:
        data = urllib.urlencode(data)

    req = urllib2.Request(url,data,headers)
    r = urllib2.urlopen(req)
    ret = r.read()
    try:

        return json.loads(ret)
    except Exception, e:
        return ret


if __name__ == "__main__":
    from BobDB import *
    def doJob(data):
        print data
        pass
    r = BobDB.getJob()

    params = []
    for p in r:
        params.append(list(p))
    requests = makeRequests(doJob, params, None, None)

    for x in requests:
        print x.args
        result = x.callable(*x.args, **x.kwds)

