from BobDB import *
from BobUtil import *
import config
import sys
import os

from convert import Convert
from log import log

class Processor:

    @staticmethod
    def getJob():
        r = BobDB.getJob()
        params = []
        for p in r:
            BobDB.updateStatus(1, p["id"])
            params.append(p)

        requests = makeRequests(Processor.doJob, params, None, Processor.handle_exception)
        return requests

    @staticmethod
    def doJob(data):

        source_file = os.path.join(config.BASE_DIR, data["node"], config.IMAGE_DIR, data["key"][0:2] + "/" + data["key"][2:4] + "/" + data["key"][4:6] + "/" + data["key"])

        dest_path   = os.path.join(config.BASE_DIR, data["node"], config.THUMBNAIL_DIR, data["key"][0:2] + "/" + data["key"][2:4] + "/" + data["key"][4:6] + "/")

        result = False

        if not os.path.exists(dest_path):
            os.makedirs(dest_path, 0777)
        try:
            result = Convert.do(source_file,dest_path)
        except Exception ,e:
            print e
        return (data, result)

    @staticmethod
    def handle_exception ():
        """docstring for handle_exception """
        traceback.print_exception(*exc_info)

    @staticmethod
    def processResult(result,request):
        """docstring for processResult"""
        log(result)

        if result[1] == True:
            BobDB.delete(result[0]['id'])
        else:
            BobDB.updateStatus(2, result[0]['id'])
	try:
            if result[0].has_key("call_back") and result[1]:
                import json
                params = json.loads(result[0]["call_back"])
                params["status"] = result[1]
                print httprequest(config.CALL_BACK_URL,data=params, method="post")
        except Exception, e:
            print  "---"
            print e


if __name__ == "__main__":
    print Processor.getJob()
