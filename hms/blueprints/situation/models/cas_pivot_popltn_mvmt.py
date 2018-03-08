# -*- coding: utf-8 -*-
# from cassandra.cluster import Cluster

class CasPivotPoplntMvmt():
    # cluster = Cluster(['183.109.124.94'], port=9042)
    # session = cluster.connect('gisdb')

    def __init__(self, **kwargs):
        super(CasPivotPoplntMvmt, self).__init__(**kwargs)

    @classmethod
    def get_col_ym_list(cls, st_yyyymm, ed_yyyymm):
        return 'OK'

    @classmethod
    def test_func(cls):
        col = ['sid_cd', 'sgg_cd', 'emd_cd', 'age_grp_cd']
        query =  "select * from pivot_popltn_stats limit 1"
        query2 = """select    %s from pivot_popltn_stats limit %s"""

        print("*" * 50)
        print(query)
        print("*" * 50)

        # return cls.session.execute(query)
        # return cls.session.execute(query2, (col, 1))

        return 'OK'
