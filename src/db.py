# -*- coding: utf-8 -*-
import os
import pymysql.cursors
conn = pymysql.connect(
    user=os.environ["MYSQL_USER"],
    passwd=os.environ["MYSQL_ROOT_PASSWORD"],
    host=os.environ["MYSQL_HOST"],
    db=os.environ["MYSQL_DATABASE"],
    charset="utf8"
)