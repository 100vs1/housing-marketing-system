# -*- coding: utf-8 -*-
from geoalchemy2.types import Geometry
from sqlalchemy import or_, and_, asc, func, desc, collate
from hms.extensions import db
from hms.blueprints.common.models.code import Code
from hms.blueprints.common.models.area import AdmSidArea, AdmSggArea, AdmEmdArea, LawEmdArea


class IncomeSitutnCompany(db.Model):
    """
    소득현황_기업 모델 정의 클래스
    지역현황 > 소득현황 메뉴에서 사용함
    """

    __bind_key__ = 'gisdb'
    __tablename__ = 'income_situtn_company'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    sid_cd = db.Column(db.String(2), nullable=False)
    sgg_cd = db.Column(db.String(5), nullable=False)
    emd_cd = db.Column(db.String(10), nullable=False)
    geom = db.Column(Geometry(geometry_type='POINT', srid=4326))
    estimate_year_income = db.Column(db.Integer())
    company_name = db.Column(db.String())
    address = db.Column(db.String())
    cl = db.Column(db.String())
    income_average = db.Column(db.Integer())
    persons = db.Column(db.Integer())
    person_income = db.Column(db.Integer())
    accident_insurance = db.Column(db.Integer())
    labor_count = db.Column(db.Integer())
    hier_insurance = db.Column(db.Integer())
    fee = db.Column(db.Integer())

    def __init__(self, **kwargs):
        super(IncomeSitutnCompany, self).__init__(**kwargs)

    @classmethod
    def find_by_filter_for_check(cls, sid_cd, sgg_cd, emd_cd):
        result = db.session.query(
                cls.emd_cd
            ).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).limit(1).first()

        return result is not None

    @classmethod
    def find_by_filter_for_list(cls, sid_cd, sgg_cd, emd_cd):
        geojson = func.ST_AsGeoJSON(cls.geom).label('geojson')

        result = db.session.query(
                geojson,
                cls.company_name,
                cls.address,
                func.count(cls.id).label('group_count')
            ).\
            filter(or_(cls.sid_cd == sid_cd,
                     cls.sgg_cd == sgg_cd,
                     cls.emd_cd == emd_cd)).\
            group_by(geojson, cls.company_name, cls.address).\
            order_by(asc(collate(cls.company_name, '"C"')))

        return result

    @classmethod
    def find_by_filter_for_bubble(cls, is_type, sid_cd, sgg_cd, emd_cd):
        geojson = db.session.query(func.ST_AsGeoJSON(func.ST_Centroid(LawEmdArea.geom)).label('geojson')). \
            filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('geojson')

        bubble_col = None
        if is_type == '1':
            bubble_col = func.round(func.avg(cls.estimate_year_income / 10000), 0)
        else:
            bubble_col = func.sum(cls.labor_count)

        result = db.session.query(db.session.query(LawEmdArea.emd_ko_nm).
                                  filter(LawEmdArea.emd_cd == cls.emd_cd).limit(1).label('area_ko_nm'),
                                  geojson,
                                  # 만 원 단위로 결과 값 변경해서 10000원 나눔
                                  bubble_col.label('total_sum')).\
            filter(or_(cls.sid_cd == sid_cd,
                       cls.sgg_cd == sgg_cd,
                       cls.emd_cd == emd_cd)).\
            group_by(cls.emd_cd, 'geojson')

        return result

    @classmethod
    def find_by_summary_by_geom(cls, geom):
        labor_sum = db.session.query(
            func.sum(cls.labor_count).label('labor_sum')
        ).filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        income_avg = db.session.query(
            func.avg(cls.estimate_year_income).label('income_avg')
        ).filter(func.ST_Intersects(cls.geom, func.ST_SetSRID(func.ST_GeomFromGeoJSON(geom), 4326)))

        return {
            'is_yyyymm': '201706',
            'labor_sum': labor_sum,
            'income_avg': income_avg
        }
