#!/usr/bin/env python
import commands
import os
import math
from log import log
import config
import re

class Convert:

    @staticmethod
    def do(fullfilename, targetDir="./"):

        str = fullfilename
        basename = os.path.basename(fullfilename)

        source = fullfilename

        fileinfo = os.path.splitext(basename)

        target = os.path.join(targetDir,fileinfo[0] + '.flv')
        target_thumb = os.path.join(targetDir,fileinfo[0] + '.jpg')

        if not os.path.exists(fullfilename):
            log(fullfilename  + " " + "not Exists")
            return 0, False

        """ convert to flv"""

        showtime=0

        if os.path.exists(target):
            showtime = Convert.get_show_time(target)
            log(target  + " " + "skip")
            return (showtime, True)

        if fileinfo[1] == ".flv":
            status, output = Convert.cmd("cp " + fullfilename + " " + target)
            if status != 0:
                log(output)
                return (1, False)
        else:
            """ generate thumbnail """
            status, output = Convert.convert(fullfilename, target)
            if status != 0:
                log(output)
                return  (2, False)

        showtime = Convert.get_show_time(target)

#        if showtime == 0:
#            return (3, False)

        status, output = Convert.generate_thumbnail(target, target_thumb, showtime)

        if status == 0:
            return (showtime, True)

        return (4, False)

    @staticmethod
    def cmd(cmd):
        return commands.getstatusoutput(cmd)

    @staticmethod
    def convert(source, target):
        """ convert file to flv """
        log("processing " + source + " to " + target )
        cmd = config.MENCODER_CMD % (source, target)
        return Convert.cmd(cmd)

    @staticmethod
    def get_show_time(target):
        status, output = Convert.cmd(config.FLVTOOL2_CMD % target)
        sec = 0
        try:
            if status == 0:
                m = re.compile('duration: ([\d|\.]+)').search(output)
                if m:
                    sec = int(float(m.group(1)))
        except Exception, e:
            print e
            sec = 0
        return sec

    @staticmethod
    def generate_thumbnail(target, target_thumb, showtime):

        start_position = max(math.floor(showtime / 10), 1)

        if not os.path.exists(os.path.dirname(target_thumb)):
            try:
                os.makedirs(os.path.dirname(target_thumb))
            except OSError:
                return (1024, "cannnot make thumbnail path")

        status, output = commands.getstatusoutput(config.SMALL_THUMBNAIL_CMD%(target , start_position, target_thumb))

        if status != 0:
            log(output)

        return (status, output)


if __name__ == "__main__":
    a = Convert.do("/Data/upload/st001/tmpvideo/f8/4f/1f/f84f1fcec8c809f12165d977b31eaeca.flv", './a/');
    print a
