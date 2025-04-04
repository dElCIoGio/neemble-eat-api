import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('app'), '..')))


ONE_SECOND = 1
ONE_MINUTE = 60
ONE_HOUR = 3600
ONE_DAY = 86400
ONE_WEEK = 604800

class CacheTime:
    GET_PARSED_MENU=5*ONE_MINUTE
    GET_MENU_PAGE=1*ONE_HOUR
    GET_RESTAURANT=12*ONE_HOUR
    GET_ALL_TABLES=10*ONE_MINUTE
    GET_ALL_ORDERS=0
    GET_RESTAURANTS_TOP_ORDERS=ONE_DAY
    GET_ALL_SESSION_ORDERS=0
    GET_OPEN_SESSION=0
    GET_TABLE_SESSION=0
    GET_USER=ONE_HOUR
    GET_USER_BY_UUID=ONE_HOUR


