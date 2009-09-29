RUNLOG= '/logs/bob.video.run.log'
ERRORLOG = '/logs/bob.video.error.log'

RINGLOG= '/logs/bob.video.ring.log'

LOGNAME = "BOBVIDEOLOG"
LOGSIZE = 524288000

PIDFILE = '/var/run/bob.video.pid'

DB_HOST = "10.10.208.52"
DB_USER = "mo.video"
DB_PASSWD = "mo.video.8.15"
DB_NAME = "storage"
DB_PORT = 3306

THREAD_LIMIT = 8

TEMP_DIR        = "tmpvideo"
VIDEO_DIR       = "video"
BASE_DIR        = "/Data/upload/"

CALL_BACK_URL 	= "http://10.10.208.52/update.php"

MENCODER_CMD = '/opt/newmplayer/bin/mencoder  %s -o %s -of lavf -oac mp3lame -lameopts abr:br=56 -ovc lavc -lavcopts vcodec=flv:vbitrate=500:mbd=2:mv0:trell:v4mv:cbp:last_pred=3 -vf scale=480:360,harddup -srate 22050 -sws 3 -ofps 30000/1001'
FLVTOOL2_CMD = '/usr/bin/flvtool2 -UP %s'

SMALL_THUMBNAIL_CMD = '/opt/ffmpeg/bin/ffmpeg -i %s -y -f image2 -ss %d -t 0.001 -s 120*90 %s >/dev/null 2>&1'

