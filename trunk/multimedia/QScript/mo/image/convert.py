#!/usr/bin/env python
import commands
import os
import math
from log import log

class Convert:

    tmp_dir = "/tmp/"

    thumb_config  = {
            "tiny" : {"type": "inside" ,"size": [20,  20]},
            "small": {"type": "inside" ,"size": [50,  50]},
            "thumb": {"type": "inside"  ,"size": [75,  75]},
            "list" : {"type": "album"  ,"size": [140, 200]},
            "show" : {"type": "album"  ,"size": [250, 400]},
            "big"  : {"type": "album"  ,"size": [500, 650]},
    }

    commands = {
            "inside"    : 'convert %s +profile "*" -crop %dx%d+%d+%d -resize %dx%d! %s',
            "album"     : 'convert %s  +profile "*" -resize "%dx%d>" %s',
    }

    gencommands = {
            "identify": "identify -format '%%w %%h ' -quiet  %s",
            "coalesce": "convert %s +profile \"*\" -coalesce  %s"
    }

    material = {
            'text' :'text.gif',
            'url'  :'url.gif',
            'nopic':  'noc.gif',
            }

    MARKWIDTH  = 200;
    MARKHEIGHT = 15;

    @staticmethod
    def do(fullfilename, targetDir="./"):
        """docstring for do"""
        status, output = Convert.cmd(Convert.gencommands['identify'] % fullfilename)

        if status != 0:
            log(output)
            return False

        size = Convert.getSize(output)

        a = output.split(" ")

        bname   = os.path.basename(fullfilename)

        pathinfo = os.path.splitext(bname)

        tmpCoalesceName = False
        isAnimated = False
        tmpName =  os.path.join(Convert.tmp_dir, pathinfo[0] +  '.tmp' +  pathinfo[1])

        if len(a) > 3:
            """coalesce"""
            status, output = Convert.cmd(Convert.gencommands['coalesce'] % (fullfilename , tmpName))
            if status != 0:
                log(output)
                return False
            isAnimated = True

        result = 0
        for c in Convert.thumb_config:

            t = Convert.thumb_config[c]
            targetFile  = pathinfo[0] + '_' +  str(t["size"][0]) + 'x' + str(t["size"][1]) +  pathinfo[1]
            target = os.path.join(targetDir, targetFile)

            if isAnimated:
                status, output = Convert.doThumbNail(tmpName, target, t["type"], size, t["size"])

                result &= status
                if status !=0:
                    log(output)
            else:
                status, output = Convert.doThumbNail(fullfilename, tmpName,t["type"], size,t["size"])
                r = Convert.waterMark(tmpName, target)

                if result == 0:
                    status = r
                    result &= status
                else:
                    print "error water mark"

        if os.path.exists(tmpName):
            os.unlink(tmpName)

        if result != 0:
            return False

        return True

    @staticmethod
    def getSize(string):
        index  = 0
        height = 0
        width  = 0
        for x in string.split(" "):
            index+=1
            if x == "":
                continue

            i = int(x)
            if index % 2 == 0:
                if i > height:
                    height = i
            else:
                if i > width:
                    width = i
        return [width, height]

    @staticmethod
    def cmd(cmd):
        return commands.getstatusoutput(cmd)

    @staticmethod
    def doThumbNail(file,target, type,orgsize, size):
        command = Convert.getCommandString(file,target, type, orgsize, size)
        print command
        return Convert.cmd(command)

    @staticmethod
    def getCommandString(file,target, type,orgsize, size):
        if type == "album":
            return Convert.commands[type] % ( file, size[0], size[1], target)
        elif type == "inside":

            orgWidth = orgsize[0]
            orgHeight = orgsize[1]
            orgRate = orgsize[0] *1.0 / orgsize[1];
            rate = size[0]  * 1.0 / size[1];

            if orgRate > rate :
                cropHeight = orgHeight;
                cropWidth  = cropHeight * rate;
            else:
                cropWidth  = orgWidth;
                cropHeight = cropWidth / rate;

            cropLeft = math.floor((orgWidth - cropWidth) / 2);
            cropTop  = math.floor((orgHeight - cropHeight) / 2);

            cropWidth = math.floor(cropWidth);
            cropHeight = math.floor(cropHeight);

            return Convert.commands[type] % (file, cropWidth, cropHeight, cropLeft, cropTop, size[0], size[1], target)


    @staticmethod
    def waterMark(filename, target):
        """docstring for waterMark"""
        status, output = Convert.cmd(Convert.gencommands['identify'] % filename)
        if status != 0:
            log(output)
            return False

        size = Convert.getSize(output)
        if size[0] > Convert.MARKWIDTH :
            base_dir = os.path.split(os.path.abspath(__file__))[0]
            text = os.path.join(base_dir,  'water', Convert.material['text']);
            url  = os.path.join(base_dir,  'water', Convert.material['url']);

            command = "convert -quality 85 -sharpen 1 -size " + str(size[0]) + "x" + str(size[1] + Convert.MARKHEIGHT) + " xc:black "\
                + "-draw \"image over 0,0 " + str(size[0])  + "x" + str(size[1]) + " '" + filename  + "'\" " \
                + "-draw \"line 0," + str(size[1]) + " " +  str(size[0]) + "," + str(size[1]) + "\" "\
                + "-gravity SouthWest -draw \"image over 0,0 0,0 '" + url + "'\" "\
                + "-gravity SouthEast -draw \"image over 0,0 0,0 '" + text + "'\" "\
                +  target;
            status, output = Convert.cmd(command)
            if status != 0:
                log(output)
            return status
        else:
            status, output = Convert.cmd("convert " +  filename  + " -quiet -quality 85 " + target);
            if status != 0:
                log(output)
            return status
        return 0


if __name__ == "__main__":
    a = Convert.do("/Data/upload/st001/image/ff/ff/11/ffff116c51a7ca4e63be868bae2ff076.jpg");
    Convert.do("ffff830aa88ba3db5d3de34ff3ad4201.jpg");
    Convert.do("test.php");
    #import os
    #str=os.path.split(os.path.abspath(__file__))[0]
    #print str
    #str = "fffff831f79e5557008b8b1e55b39c01.jpg"
    #str=os.path.abspath(str)
    #print os.path.split(str)
    #print os.path.splitext(str)
    #print os.path.basename(str)
