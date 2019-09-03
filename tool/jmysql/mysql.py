# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/8.
# 功能:
#  数据库
import pymysql


# star 数据库对象
class Mysql:
    """
    对pymysql的简单封装,实现基本的连接
    """

    def __init__(self, config={}):
        try:
            self.host = config["host"]
            self.user = config["user"]
            self.pwd = config["pwd"]
            self.db = config["db"]
        except:
            raise
        self.cur = self.__GetConnect()

    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        if not self.db:
            raise (NameError, "没有设置数据库信息")
        self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, db=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise (NameError, "连接数据库失败")
        else:
            return cur

    def ExecQuery(self, sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        调用示例：
                ms = MYSQL(host="localhost",user="sa",pwd="123456",db="PythonWeiboStatistics")
                resList = ms.ExecQuery("SELECT id,NickName FROM WeiBoUser")
                for (id,NickName) in resList:
                    print str(id),NickName
        """
        self.cur.execute(sql)
        resList = self.cur.fetchall()
        return resList

    def ExecNonQuery(self, sql):
        """
        执行非查询语句
        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception:  # 出现异常回滚
            self.conn.rollback()
            raise

    def __del__(self):
        self.cur.close()