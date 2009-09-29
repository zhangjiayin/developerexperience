import Dao

dao = Dao.Dao();
class BobDB:
    @staticmethod
    def getJob():
        result = dao.query("select * from `video_tmp` where status = 0;")
        ret = []
        for x in result:
            ret.append({"id": x[0], "key": x[1], "node": x[2], "time": x[3], "call_back": x[5]})
        return ret
    @staticmethod
    def updateStatus(status, id):

        sql = "UPDATE  `storage`.`video_tmp` SET  `status` =  '" + str(status) + "' WHERE  `video_tmp`.`fileid` =  '" + str(id) + "' LIMIT 1 ;"
        return dao.query(sql)

    @staticmethod
    def delete(key) :
        sql = "delete from `storage`.`video_tmp`  WHERE  `video_tmp`.`fileid` =  '" +  str(key)+ "' LIMIT 1 ;"
        return dao.query(sql)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "restore":
        BobDB.restore()
    result = BobDB.getJob()
    print result
