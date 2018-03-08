# -*- coding: utf-8 -*-
import textwrap

from config.settings import *
from config.errors import *
import requests
import json


class LivyAPI:
    livy_url = LIVY_URL
    hdfs_url = HDFS_URL
    pivot_dir = "product/pivot/"

    from_size = 0
    to_size = 100

    pivot_tables = ['income_situtn', 'trnstn_situtn']
    livy_statements = []

    url_salsh = None
    session_id = None
    headers = {'Content-Type': 'application/json'}

    def __init__(self):
        print('LivyAPI')
        print(self.livy_url)

    @classmethod
    def test_static_method(cls):
        # cls.refine_livy_url()
        return 'OK'

    @staticmethod
    def refine_url(url):
        url_length = len(url)

        if url[url_length - 1] is '/':
            return url[:-1]
        else:
            return url

    @classmethod
    def get_sessions(cls, from_size, to_size):
        if from_size is None:
            from_size = cls.from_size
        if to_size is None:
            to_size = cls.to_size

        target_url = cls.refine_url(cls.livy_url) + "/sessions"
        params = {'from': from_size, 'size': to_size}
        res = requests.get(target_url, params=params)

        if res.text is None:
            return {
                'isSuccess': False,
                'msg': ERR_LIVY_SESSION_EMPTY['msg'],
                'code': ERR_LIVY_SESSION_EMPTY['code'],
            }
        else:
            return {
                'isSuccess': True,
                'msg': 'get sessions',
                'data': res.json()
            }

    @classmethod
    def get_sessions_with_create(cls, from_size, to_size):
        if from_size is None:
            from_size = cls.from_size
        if to_size is None:
            to_size = cls.to_size

        sessions = cls.get_sessions(from_size, to_size)

        if sessions['isSuccess']:
            return sessions
        else:
            cls.create_session()

            return cls.get_sessions(from_size, to_size)

    @classmethod
    def get_sessions_by_name(cls, from_size, to_size, name):
        if from_size is None:
            from_size = cls.from_size
        if to_size is None:
            to_size = cls.to_size

        sessions = cls.get_sessions(from_size, to_size)

        ret = []
        if sessions['isSuccess']:
            for session in sessions['data']:
                if session['name'] == name:
                    ret.append(session)

            if len(ret) <= 0:
                return {
                    'isSuccess': False,
                    'msg': ERR_LIVY_SESSION_EMPTY['msg'],
                    'code': ERR_LIVY_SESSION_EMPTY['code'],
                }
            else:
                return {
                    'isSuccess': True,
                    'msg': 'get sessions',
                    'data': ret
                }
        else:
            return sessions

    @classmethod
    def get_session(cls, session_id):
        if session_id is None:
            session_id = cls.session_id

        if session_id is None:
            return {
                'isSuccess': False,
                'errorCode': ERR_LIV_SESSION_ID_UNMATCHED['code'],
                'msg': ERR_LIV_SESSION_ID_UNMATCHED['msg']
            }

        target_url = cls.refine_url(cls.livy_url) + "/sessions/" + str(session_id)

        res = requests.get(target_url)
        print(res.url)

        if 'id' in res.json():
            return {
                'isSuccess': True,
                'msg': 'get session',
                'data': res.json()
            }
        else:
            return {
                'isSuccess': False,
                'errorCode': ERR_LIV_SESSION_ID_UNMATCHED['code'],
                'msg': res.json()
            }

    @classmethod
    def create_session(cls):
        target_url = cls.refine_url(cls.livy_url) + "/sessions"
        print(target_url)
        headers = {'Content-Type': 'application/json'}
        data = {
            'kind': 'pyspark',
            'proxyUser': str(SERVER_NAME)
        }
        res = requests.post(target_url, data=json.dumps(data), headers=headers)

        print("*****************Livy API SSS*****************")
        print(res.text)
        print("*****************Livy API SSS*****************")

        cls.session_id = res.json()['id']

        if 'id' in res.json():
            return {
                'isSuccess': True,
                'msg': 'created',
                'data': res.text
            }
        else:
            return {
                'isSuccess': False,
                'errorCode': ERR_LIVY_SESSION_EMPTY['code'],
                'msg': ERR_LIVY_SESSION_EMPTY['msg']
            }

    @classmethod
    def delete_session(cls, session_id):
        print("hihihihihihihihihihihihihihihihihihihihihihihihi")
        target_url = cls.refine_url(cls.livy_url) + "/sessions/" + str(session_id)
        headers = {'Content-Type': 'application/json'}

        res = requests.delete(target_url, headers=headers)

        if 'msg' in res.json():
            print(res.json())
            if res.json()['msg'] == 'deleted':
                return {
                    'isSuccess': True,
                    'msg': 'deleted',
                    'data': None
                }
            else:
                return {
                    'isSuccess': False,
                    'errorCode': ERR_LIVY_SESSION_EMPTY['code'],
                    'msg': ERR_LIVY_SESSION_EMPTY['msg']
                }
        else:
            print(res.json())
            return {
                'isSuccess': False,
                'errorCode': ERR_LIVY_DELETED_FAIL['code'],
                'msg': res.json()
            }

    @classmethod
    def get_statements(cls, table_name):
        cls.session_id = 53

        cls.get_sessions_with_create(0, 10)
        livy_url = cls.refine_url(cls.livy_url)
        session_url = livy_url + "/sessions/" + str(cls.session_id)
        statements_url = session_url + "/statements"

        data = {'code': "df = sqlContext.read.format('csv').option('header', 'true')." +
                        "load('" + cls.refine_url(cls.hdfs_url) + '/' + cls.pivot_dir + 'popltn_mvmt/pivot_popltn_mvmt' + "').cache();" +
                        "df.createOrReplaceTempView('" + 'pivot_poplnt_mvmt' + "');"}

        print(data)

        res = requests.post(statements_url, data=json.dumps(data), headers=cls.headers)
        print(res)

        # df = {
        #     'trnstn_situtn_1': 'trnstn_count_df',
        #     'trnstn_situtn': 'trnstn_junse_df',
        #     'trnstn_situtn_2': 'trnstn_sale_df''',
        #     'supply_present_1': 'supply_count_df',
        #     'supply_present_2': 'supply_price_df'
        # }
        #
        # tableCode = {'code': "spark.sql('SELECT * FROM {data} limit 2').toJSON().collect()".format(data=table_name)}
        # # tableCode = {
        # #     'code': textwrap.dedent("""
        # #     val d = spark.sql("SELECT * FROM {data} limit 2")
        # #     val e = d.collect
        # #     %json e""").format(data=table_name)}
        # setTableCode = requests.post(statements_url, data=json.dumps(tableCode), headers=cls.headers)
        #
        # waitingFlag = True
        # getTableInfo = None
        # while waitingFlag:
        #     getTableInfo = requests.get(livy_url + setTableCode.headers['Location'], headers=cls.headers)
        #
        #     print("getTableInfo")
        #     if getTableInfo.json()['state'] == 'available':
        #         waitingFlag = False
        #
        # print(getTableInfo)
        # getTableStatements = getTableInfo.json()
        #
        # print(getTableStatements)
        #
        # if getTableStatements['output']['status'] != 'error':
        #     resultArr = getTableStatements['output']['data']
        #
        #     print(resultArr)
        #     # resultArr = json.dumps(resultArr).replace("'", "")
        #
        #     # print(json.loads(resultArr))
        #     # print(resultArr['text'])
        # else:
        #     return 'error'
        #
        #
        # # for result in resultArr:
        # #     print(result)
        #
        # cls.livy_statements.append(getTableInfo)
        # cls.delete_session(cls.session_id)

    @classmethod
    def get_datas(cls, table_name):

        cls.session_id = 53

        cls.get_sessions_with_create(0, 10)
        livy_url = cls.refine_url(cls.livy_url)
        session_url = livy_url + "/sessions/" + str(cls.session_id)
        statements_url = session_url + "/statements"

        tableCode = {'code': "spark.sql('SELECT * FROM {data} where in_sid_cd=11 and out_sid_cd=11').toJSON().collect()".format(data=table_name)}
        # tableCode = {
        #     'code': textwrap.dedent("""
        #     val d = spark.sql("SELECT * FROM {data} limit 2")
        #     val e = d.collect
        #     %json e""").format(data=table_name)}
        setTableCode = requests.post(statements_url, data=json.dumps(tableCode), headers=cls.headers)
        print(setTableCode.text)

        getTableInfo = requests.get(livy_url + setTableCode.headers['Location'], headers=cls.headers)
        print(getTableInfo.text)

        return getTableInfo.json()['output']
