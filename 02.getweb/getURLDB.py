#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pymysql

class GetPath:
    """docstring for GetPathh"""
    def __init__(self, netloc, startID):
        self.cur = ''
        self.netloc = netloc
        self.startID = startID
        self.connect()

    def connect(self):
        conn = pymysql.connect(
            host='127.0.0.1',
            unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
            port=3306,
            user='web',
            passwd='web',
            db='crawler',
            use_unicode=True,
            charset='utf8')

        self.cur = conn.cursor()

        # get netloc tid
        self.cur.execute("SELECT tid \
                          FROM crawler_taxonomy_term_data \
                          WHERE name=%s", self.netloc)
        tid = self.cur.fetchone()

        self.cur.execute("SELECT b.field_url_id_value, a.field_url_path_value \
                          FROM crawler_field_data_field_url_path AS a \
                          INNER JOIN crawler_field_data_field_url_id AS b \
                          INNER JOIN crawler_field_data_field_netloc AS c \
                          ON a.entity_id=b.entity_id AND a.entity_id=c.entity_id \
                          WHERE c.field_netloc_tid=%s AND b.field_url_id_value > %s \
                          ORDER BY b.field_url_id_value", (tid[0], self.startID))

        self.cur.close()
        conn.close()

    def getResult(self):
        return self.cur


if __name__ == '__main__':
    getPath = GetPath('health.sanook.com')
    rows = getPath.getResult()
    for row in rows:
        print row[0]," : ",row[1].encode('utf-8', 'replace')
