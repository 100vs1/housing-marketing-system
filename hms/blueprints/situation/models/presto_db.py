# -*- coding: utf-8 -*-

import prestodb

from sqlalchemy import func, and_, or_, desc
from sqlalchemy.dialects import postgresql

from hms.extensions import db

import datetime

class PrestoTest(db.Model):

    __bind__ = 'hms'
    __tablename__ = '$/$/$/$/$/$'

    conn = None
    sid_cd = db.Column(db.String(2), primary_key=True, nullable=False)
    sgg_cd = db.Column(db.String(5), primary_key=True, nullable=False)
    emd_cd = db.Column(db.String(10), primary_key=True, nullable=False)
    age_grp_cd = db.Column(db.String(10))
    rsdnc_clsftn_cd = db.Column(db.String(10))
    fmly_num_cd = db.Column(db.String(10))
    room_num_cd = db.Column(db.String(10))
    exclsv_areacl_id = db.Column(db.String(10))
    house_clsftn_code = db.Column(db.String(10))
    hshold_num_cd = db.Column(db.String(10))
    exclsv_area = db.Column(db.Float(10))
    trnstn_clsftn_code = db.Column(db.String(10))
    out_sid_cd = db.Column(db.String(10))
    out_sgg_cd = db.Column(db.String(10))
    out_emd_cd = db.Column(db.String(10))
    in_sid_cd = db.Column(db.String(10))
    in_sgg_cd = db.Column(db.String(10))
    in_emd_cd = db.Column(db.String(10))
    mv_reasn_cd = db.Column(db.String(10))
    aplcnt_age_cd = db.Column(db.String(10))
    fmly_nums = db.Column(db.String(10))

    def __init__(self, **kwargs):
        # Call Flask-SQLAlchemy's constructor.
        super(PrestoTest, self).__init__(**kwargs)

    @classmethod
    def get_cursor(self):
        conn = prestodb.dbapi.connect(
            host='183.111.230.252',
            port=7788,
            user='hadoop',
            catalog='hive',
            schema='hms',
        )

        cur = conn.cursor()
        # cur.execute('SELECT * FROM hms.pivot_test')
        # rows = cur.fetchall()

        return cur
        # return 'OK'

    @classmethod
    def select_popltn_stats_pivot_for_area(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm):
        table_name = 'popltn_stats_pivot_new'

        age_grps = []
        for cds in age_grp_cds:
            age_grps.append(str(cds))

        base_query = db.sesssion.query(
            cls.sid_cd
        ).filter(cls.age_grp_cd.in_(age_grps))

        if sid_cd:
            col_arr = ['sid_ko_nm', 'sgg_ko_nm']
            base_query = base_query.filter(cls.sid_cd == sid_cd)
        elif sgg_cd:
            col_arr = ['sgg_ko_nm', 'emd_ko_nm']
            base_query = base_query.filter(cls.sgg_cd == sgg_cd)
        elif emd_cd:
            col_arr = ['emd_cd']
            base_query = base_query.filter(cls.emd_cd == emd_cd)

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        date_arr = cls.get_term_arr_for_pivot(st_yyyymm, ed_yyyymm, 1, except_quotes=False)

        date_arr_for_sum = []
        # for date in date_arr:

    # 인구통계 테이블
    @classmethod
    def find_for_popltn_stats_pivot(cls, sid_cd, sgg_cd, emd_cd, age_grp_cds, st_yyyymm, ed_yyyymm):
        # 테이블 명
        table_name = 'popltn_stats_pivot_new'

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.age_grp_cd.in_(age_grp_cds))

        # 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        # where 절 만들기
        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(st_yyyymm, ed_yyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('sum ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_hshold_stats_pivot(cls, sid_cd, sgg_cd,
                                    rsdnc_clsftn_cds, fmly_num_cds, room_num_cds,
                                    hs_syear, hs_eyear):

        table_name = 'hshold_stats_pivot'

        results = db.session.query(
            cls.sid_cd
        ).filter(or_(cls.sid_cd == sid_cd,
                     cls.sgg_cd == sgg_cd)).\
            filter(cls.rsdnc_clsftn_cd.in_(rsdnc_clsftn_cds)).\
            filter(cls.fmly_num_cd.in_(fmly_num_cds)).\
            filter(cls.room_num_cd.in_(room_num_cds))

        dummy_sql = str(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        col_arr = ['sid_ko_nm', 'sgg_ko_nm', 'rsdnc_clsftn_cd', 'fmly_num_cd', 'room_num_cd']
        date_arr = cls.get_term_arr_for_pivot(hs_syear, hs_eyear, 5)

        cols = ", ".join(col_arr + date_arr)

        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where
        print(sql)
        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': cols
        }

    @classmethod
    def find_for_popltn_mvmt(cls, out_sid_cds, out_sgg_cds, out_emd_cds, in_sid_cd, in_sgg_cd,
                             in_emd_cd, mv_reasn_cds, aplcnt_age_cds, fmly_nums,
                             pm_syyyymm, pm_eyyyymm):
        # 테이블 명
        table_name = 'popltn_mvmt_pivot_new'

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.mv_reasn_cd.in_(mv_reasn_cds)).\
            filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds))

        # 필터 추가 적용
        if out_sid_cds:
            base_query = base_query.filter(cls.out_sid_cd == out_sid_cds)
        elif out_sgg_cds:
            base_query = base_query.filter(cls.out_sgg_cd == out_sgg_cds)
        elif out_emd_cds:
            base_query = base_query.filter(cls.out_emd_cd == out_emd_cds)
        else:
            print('asdf')
        if in_sid_cd:
            base_query = base_query.filter(cls.in_sid_cd == in_sid_cd)
        elif in_sgg_cd:
            base_query = base_query.filter(cls.in_sgg_cd == in_sgg_cd)
        elif in_emd_cd:
            base_query = base_query.filter(cls.in_emd_cd == in_emd_cd)
        else:
            print('asdf')

        # where 절 만들기
        dummy_sql = str(
            base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만드릭
        out_col_arr = cls.get_area_col(out_sid_cds, out_sgg_cds, out_emd_cds, 'out_')
        in_col_arr = cls.get_area_col(in_sid_cd, in_sgg_cd, in_emd_cd, 'in_')
        date_arr = cls.get_term_arr_for_pivot(pm_syyyymm, pm_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('sum ("' + date + '") as "' + date + '"')
        cols = ", ".join(out_col_arr + in_col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            out_col_arr + in_col_arr) + ' ORDER BY ' + ", ".join(out_col_arr + in_col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(out_col_arr + in_col_arr + date_arr)
        }

        # if out_sid_cds:
        #     out_sid_cds = int(out_sid_cds)
        # if out_sgg_cds:
        #     out_sgg_cds = int(out_sgg_cds)
        # if out_emd_cds:
        #     out_emd_cds = int(out_emd_cds)
        # if in_sid_cd:
        #     table_name = table_name + '_' + in_sid_cd
        #     in_sid_cd = int(in_sid_cd)
        # if in_sgg_cd:
        #     table_name = table_name + '_' + str(int(in_sid_cd) / 1000)
        #     in_sgg_cd = int(in_sgg_cd)
        # if in_emd_cd:
        #     table_name = table_name + '_' + str(int(in_sid_cd) / 100000)
        #     in_emd_cd = int(in_emd_cd)

        # results = db.session.query(
        #     cls.sid_cd
        # ).filter(or_(cls.out_sid_cd == out_sid_cds,
        #              cls.out_sgg_cd == out_sgg_cds,
        #              cls.out_emd_cd == out_emd_cds)). \
        #     filter(or_(cls.in_sid_cd == in_sid_cd,
        #                cls.in_sgg_cd == in_sgg_cd,
        #                cls.in_emd_cd == in_emd_cd)).\
        #     filter(cls.mv_reasn_cd.in_(mv_reasn_cds)).\
        #     filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds))

        # results = db.session.query(
        #     cls.sid_cd
        # ).filter(or_(cls.out_sid_cd == out_sid_cds,
        #              cls.out_sgg_cd == out_sgg_cds,
        #              cls.out_emd_cd == out_emd_cds)).\
        #     filter(or_(cls.in_sid_cd == in_sid_cd,
        #                cls.in_sgg_cd == in_sgg_cd,
        #                cls.in_emd_cd == in_emd_cd)).\
        #     filter(cls.mv_reasn_cd.in_(mv_reasn_cds)).\
        #     filter(cls.aplcnt_age_cd.in_(aplcnt_age_cds))
        #
        # dummy_sql = str(results.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        #
        # where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")
        #
        # col_arr = ['in_sid_ko_nm', 'in_sgg_ko_nm', 'in_emd_ko_nm', 'out_sid_ko_nm', 'out_sgg_ko_nm', 'out_emd_ko_nm', 'mv_reasn_cd', 'aplcnt_age_cd']
        # date_arr = cls.get_term_arr_for_pivot(pm_syyyymm, pm_eyyyymm, 1)
        #
        # # date_arr_for_sum = []
        # # for date in date_arr:
        # #     date_arr_for_sum.append('sum(' + date + ') as ' + date)
        #
        # cols = ", ".join(col_arr + date_arr)
        #
        # sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where
        #
        # print(sql)
        # #
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # # print("print sql Start")
        # # print(sql)
        # # print("print sql End")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # #
        # # print("print Connection Start")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # # cur = cls.get_cursor()
        # # # cur = cls.get_cursor()
        # # print("print Connection End")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # #
        # # print("print execute Start")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # # cur.execute(sql)
        # # print("print execute End")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # #
        # # print("print fetchall Start")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        # # rows = cur.fetchmany(100000)
        # # print("print fetchall End")
        # # dt = datetime.datetime.now()
        # # print(str(dt.minute) + ':' + str(dt.second) + ':' + str(dt.microsecond))
        #
        # cur = cls.get_cursor()
        # cur.execute(sql)
        # rows = cur.fetchall()
        #
        # return {
        #     'rows': rows,
        #     'cols': cols
        # }

    @classmethod
    def parse_exclusive_cd(cls, cd):
        if cd == 1:
            return u"20(㎡) 이하"
        elif cd == 2:
            return u'20(㎡) ~ 30(㎡)'
        elif cd == 3:
            return u'30(㎡) ~ 40(㎡)'
        elif cd == 4:
            return u'40(㎡) ~ 50(㎡)'
        elif cd == 5:
            return u'50(㎡) ~ 60(㎡)'
        elif cd == 6:
            return u'60(㎡) ~ 70(㎡)'
        elif cd == 7:
            return u'70(㎡) ~ 80(㎡)'
        elif cd == 8:
            return u'80(㎡) ~ 90(㎡)'
        elif cd == 9:
            return u'90(㎡) ~ 100(㎡)'
        elif cd == 10:
            return u'100(㎡) ~ 110(㎡)'
        elif cd == 11:
            return u'110(㎡) ~ 120(㎡)'
        elif cd == 12:
            return u'120(㎡) ~ 130(㎡)'
        elif cd == 13:
            return u'130(㎡) ~ 140(㎡)'
        elif cd == 14:
            return u'140(㎡) ~ 150(㎡)'
        elif cd == 15:
            return u'150(㎡) ~ 160(㎡)'
        elif cd == 16:
            return u'160(㎡) ~ 170(㎡)'
        elif cd == 17:
            return u'170(㎡) ~ 180(㎡)'
        elif cd == 18:
            return u'180(㎡) ~ 190(㎡)'
        elif cd == 19:
            return u'190(㎡) ~ 200(㎡)'
        elif cd == 20:
            return u'200(㎡) 이상'


    @classmethod
    def find_for_trnstn_situtn_count(cls, sid_cd, sgg_cd, emd_cd,
                                     tst_ssale, tst_esale,
                                     tst_trans_type, tst_house_kind,
                                     tst_sexarea, tst_eexarea,
                                     tst_syyyymm, tst_eyyyymm):
        # 테이블 명
        table_name = 'trnstn_count_pivot_new'

        tst_sexarea = int(tst_sexarea) / 10
        tst_eexarea = int(tst_eexarea) / 10
        exclsv_areacl = []
        for i in range(tst_sexarea, tst_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.trnstn_clsftn_code == tst_trans_type).\
            filter(cls.house_clsftn_code == tst_house_kind).\
            filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        # where 절 만들기
        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tst_syyyymm, tst_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_supply_count_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                     tst_ssale, tst_esale,
                                     tst_trans_type, tst_house_kind,
                                     tst_sexarea, tst_eexarea,
                                     tst_syyyymm, tst_eyyyymm):
        # 테이블 명
        table_name = 'trnstn_supply_count_pivot_new'

        tst_sexarea = int(tst_sexarea) / 10
        tst_eexarea = int(tst_eexarea) / 10
        exclsv_areacl = []
        for i in range(tst_sexarea, tst_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        # where 절 만들기
        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tst_syyyymm, tst_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_trnstn_sale_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                   tsp_ssale, tsp_esale,
                                   tsp_trans_type, tsp_house_kind,
                                   tsp_sexarea, tsp_eexarea,
                                   tsp_syyyymm, tsp_eyyyymm):

        # 테이블 명
        table_name = 'trnstn_sale_pivot_new'

        # 면적 코드 처리
        tsp_sexarea = int(tsp_sexarea) / 10
        tsp_eexarea = int(tsp_eexarea) / 10

        if tsp_eexarea > 20:
            tsp_eexarea = 20
        exclsv_areacl = []
        for i in range(tsp_sexarea, tsp_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.house_clsftn_code == tsp_house_kind).\
            filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tsp_syyyymm, tsp_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_trnstn_junse_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                    tsp_ssale, tsp_esale,
                                    tsp_trans_type, tsp_house_kind,
                                    tsp_sexarea, tsp_eexarea,
                                    tsp_syyyymm, tsp_eyyyymm):

        # 테이블 명
        table_name = 'trnstn_junse_pivot_new'

        # 면적 코드 처리
        tsp_sexarea = int(tsp_sexarea) / 10
        tsp_eexarea = int(tsp_eexarea) / 10

        if tsp_eexarea > 20:
            tsp_eexarea = 20

        exclsv_areacl = []
        for i in range(tsp_sexarea, tsp_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.house_clsftn_code == tsp_house_kind).\
            filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tsp_syyyymm, tsp_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_trnstn_mnthly_rent_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                    tsp_ssale, tsp_esale,
                                    tsp_trans_type, tsp_house_kind,
                                    tsp_sexarea, tsp_eexarea,
                                    tsp_syyyymm, tsp_eyyyymm):
        # 테이블 명
        table_name = 'trnstn_mnthly_rent_pivot_new'

        # 면적 코드 처리
        tsp_sexarea = int(tsp_sexarea) / 10
        tsp_eexarea = int(tsp_eexarea) / 10

        if tsp_eexarea > 20:
            tsp_eexarea = 20
        exclsv_areacl = []
        for i in range(tsp_sexarea, tsp_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.house_clsftn_code == tsp_house_kind). \
            filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        dummy_sql = str(
            base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tsp_syyyymm, tsp_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_trnstn_supply_price_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                           tsp_ssale, tsp_esale,
                                           tsp_trans_type, tsp_house_kind,
                                           tsp_sexarea, tsp_eexarea,
                                           tsp_syyyymm, tsp_eyyyymm):
        # 테이블 명
        table_name = 'trnstn_supply_price_pivot_new'

        # 면적 코드 처리
        tsp_sexarea = int(tsp_sexarea) / 10
        tsp_eexarea = int(tsp_eexarea) / 10

        if tsp_eexarea > 20:
            tsp_eexarea = 20

        exclsv_areacl = []
        for i in range(tsp_sexarea, tsp_eexarea + 1):
            exclsv_areacl.append(str(i))

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(tsp_syyyymm, tsp_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_idnftn_bldng_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                    ib_house_kind, ib_sexarea, ib_eexarea,
                                    ib_syyyymm, ib_eyyyymm):
        # 테이블 명
        table_name = 'idntfn_bldng_pivot_new'

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.house_clsftn_code == ib_house_kind). \
            filter(and_(cls.exclsv_areacl_id >= ib_sexarea,
                        cls.exclsv_areacl_id <= ib_eexarea))

        # 지역 코드 필터 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        # where 절 추가
        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(ib_syyyymm, ib_eyyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('avg ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_busins_situtn_pivot(cls):
        return 'OK'

    @classmethod
    def find_for_hshold_imgrat_pivot(cls, sid_cd, sgg_cd, emd_cd, hi_fmly_num_cd, st_yyyymm, ed_yyyymm):
        # 테이블 명
        table_name = 'hshold_imgrat_pivot_new'

        # 베이스 쿼리 만들기
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.hshold_num_cd.in_(hi_fmly_num_cd))

        # 필처 추가 적용
        base_query = cls.get_area_filter(sid_cd, sgg_cd, emd_cd, base_query)

        # where 절 만들기
        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")
        date_arr = cls.get_term_arr_for_pivot(st_yyyymm, ed_yyyymm, 1, False)
        date_arr_for_sum = []
        for date in date_arr:
            date_arr_for_sum.append('sum ("' + date + '") as "' + date + '"')
        cols = ", ".join(col_arr + date_arr_for_sum)

        # SQL Summary
        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_supply_present_pivot(cls, sid_cd, sgg_cd, emd_cd,
                                      sp_type,
                                      sp_sexarea, sp_eexarea,
                                      st_yyyymm, ed_yyyymm):

        sp_sexarea = int(sp_sexarea) / 10
        sp_eexarea = int(sp_eexarea) / 10

        if sp_eexarea > 20:
            sp_eexarea = 20

        exclsv_areacl = []
        for i in range(sp_sexarea, sp_eexarea + 1):
            exclsv_areacl.append(str(i))

        # base_query의 column 목록은 재정의 될 것이므로 sid_cd를 더미로 넣어둔다.
        base_query = db.session.query(
            cls.sid_cd
        ).filter(cls.exclsv_areacl_id.in_(exclsv_areacl))

        if sid_cd:
            col_arr = ['sid_ko_nm', 'sgg_ko_nm']
            base_query = base_query.filter(cls.sid_cd == sid_cd)
        elif sgg_cd:
            col_arr = ['sgg_ko_nm', 'emd_ko_nm']
            base_query = base_query.filter(cls.sgg_cd == sgg_cd)
        else:
            col_arr = ['emd_ko_nm']
            base_query = base_query.filter(cls.emd_cd == emd_cd)

        if sp_type == '1':
            table_name = 'supply_present_count_pivot_new'
            grouping_type = 'sum'
        else:
            table_name = 'supply_present_price_pivot_new'
            grouping_type = 'avg'

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        date_arr = cls.get_term_arr_for_pivot(st_yyyymm, ed_yyyymm, 1, except_quotes=False)

        date_arr_for_sum = []
        for date in date_arr:
            if grouping_type is 'avg':
                date_arr_for_sum.append(grouping_type + '("' + date + '") as ' + '"' + date + '"')
            else:
                date_arr_for_sum.append(grouping_type + '("' + date + '") as ' + '"' + date + '"')

        cols = ", ".join(col_arr + date_arr_for_sum)

        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " group by " + ", ".join(col_arr) + ' order by sgg_ko_nm'

        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + date_arr)
        }

    @classmethod
    def find_for_income_situtn_pivot(cls, sid_cd, sgg_cd, emd_cd, is_type):
        # 테이블 명
        table_name = 'income_situtn_company_pivot'

        # if sid_cd:
        #     sid_cd = int(sid_cd)
        # if sgg_cd:
        #     sgg_cd = int(sgg_cd)
        # if emd_cd:
        #     emd_cd = int(emd_cd)

        # 베이 쿼리 만들기
        base_query = db.session.query(cls.sid_cd)

        # 지역 코드 필터 추가 적용
        # todo: Pivot Varchar colmun으로 치환 되면 바꿔야함
        if sid_cd:
            base_query = base_query.filter(cls.sid_cd == int(sid_cd))
        elif sgg_cd:
            base_query = base_query.filter(cls.sgg_cd == int(sgg_cd))
        elif emd_cd:
            base_query = base_query.filter(cls.emd_cd == int(emd_cd))
        else:
            print('asdf')

        dummy_sql = str(base_query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
        where = ' ' + dummy_sql[dummy_sql.find("WHERE "):].replace('"' + cls.__tablename__ + '".', "")

        # column 만들기
        col_arr = cls.get_area_col(sid_cd, sgg_cd, emd_cd, "")

        target_col = []
        target_col_for_group = []
        if is_type == '1':
            target_col = ['estimate_year_income']
            target_col_for_group = ['avg(estimate_year_income) as estimate_year_income']
        else:
            target_col = ['labor_count']
            target_col_for_group = ['sum(labor_count) as labor_count']

        cols = ", ".join(col_arr + target_col_for_group)

        sql = "SELECT " + cols + " FROM " + cls.__bind__ + '.' + table_name + where + " GROUP BY " + ", ".join(
            col_arr) + ' ORDER BY ' + ", ".join(col_arr)
        print(sql)

        cur = cls.get_cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        return {
            'rows': rows,
            'cols': ", ".join(col_arr + target_col)
        }

    @classmethod
    def get_area_filter(cls, sid_cd, sgg_cd, emd_cd, base_query):
        if sid_cd:
            base_query = base_query.filter(cls.sid_cd == sid_cd)
        elif sgg_cd:
            base_query = base_query.filter(cls.sgg_cd == sgg_cd)
        elif emd_cd:
            base_query = base_query.filter(cls.emd_cd == emd_cd)
        else:
            print('Something wrong')

        return base_query

    @classmethod
    def get_area_col(cls, sid_cd, sgg_cd, emd_cd, prefix=None):
        col_arr = []
        if sid_cd:
            col_arr = [prefix + 'sid_ko_nm', prefix + 'sgg_ko_nm']
        elif sgg_cd:
            col_arr = [prefix + 'sgg_ko_nm', prefix + 'emd_ko_nm']
        elif emd_cd:
            col_arr = [prefix + 'emd_ko_nm']
        else:
            print('Something wrong');

        return col_arr

    @classmethod
    def get_term_arr_for_pivot(cls, start_date, end_date, step, except_quotes=True):

        start_length = len(str(start_date))
        end_length = len(str(end_date))

        start_date = int(start_date)
        end_date = int(end_date)

        ret = []
        # date
        if start_length == 4 and end_length == 4:
            target = start_date
            while target <= end_date:
                if except_quotes:
                    print("True~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    ret.append('"' + str(target) + '"')
                else:
                    ret.append(str(target))
                    print("flase~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                target += step

            return ret
        # year
        elif start_length == 6 and end_length == 6:
            target = start_date
            while target <= end_date:
                if except_quotes:
                    ret.append('"' + str(target) + '"')
                else:
                    ret.append(str(target))

                if target % 100 == 12:
                    target += 89
                else:
                    target += step
            return ret
        else:
            return False
