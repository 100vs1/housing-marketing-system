# -*- coding: utf-8 -*-
from flask import send_file

from config.settings import *
import requests


class VWorldAPI:
    searchUrl = 'http://api.vworld.kr/req/search?'
    wmsUrl = 'http://api.vworld.kr/req/wms?'
    wfsUrl = 'http://api.vworld.kr/req/wfs?'

    apiKey = VWORLD_API_KEY
    domain = 'http://' + SERVER_NAME
    requestUrl = ''

    def __init__(self):
        print('vWorldAPI')

    # 주소 검색
    @classmethod
    def search(cls, query, search_type, category):
        data = {
            'service': 'search',
            'version': '2.0',
            'request': 'search',
            'key': cls.apiKey,
            'format': 'json',
            'errorFormat': 'json',
            'size': 1000,
            'page': 1,
            'query': query,
            'type': search_type,
            'category': category,
            'crs': 'EPSG:4326',
        }
        req = requests.post(cls.searchUrl, data)

        return req.json()['response']

    # 지적도_WMS
    @classmethod
    def land_seq_map_for_wms(cls, req_oper, transparent, bgcolor):
        # req_oper: GetMap,GetCapabilities
        # data = {
        #     'service': 'WMS',
        #     'version': '1.3.0',
        #     'request': req_oper,
        #     'key': cls.apiKey,
        #     'format': 'image/png',
        #     # 'format': 'json',
        #     'exceptions': 'text/xml',
        #     'layers': 'LP_PA_CBND_BUBUN,LP_PA_CBND_BONBUN',
        #     'styles': 'LP_PA_CBND_BUBUN,LP_PA_CBND_BONBUN',
        #     'bbox': '14133818.022824,4520485.8511757,14134123.770937,4520791.5992888',
        #     'width': 250,
        #     'height': 250,
        #     'transparent': transparent,
        #     'bgcolor': bgcolor,         # 0xFFFFFF
        #     'crs': 'EPSG:4326',
        #     'domain': cls.domain
        # }

        data = {
            'service': 'WMS',
            # 'version': '1.3.0',
            'request': 'GetMap',
            'key': 'A2D7B074-4BE3-3253-BA1B-04619AC46675',
            'format': 'image/png',
            # 'exceptions': 'text/xml',
            'layers': 'LP_PA_CBND_BUBUN',
            'styles': 'LP_PA_CBND_BUBUN',
            'bbox': '13987670,3912271,14359383,4642932',
            'width': '1000',
            'height': '256',
            # 'transparent': 'true',
            # # 'bgcolor': '0xFFFFFF',
            'crs': 'EPSG:900913',
            'domain': 'http://www.local_alphanets.ai'
        }

        req = requests.post(cls.wmsUrl, data)

        return req

    # 지적도_WFS
    @classmethod
    def land_seq_map_for_wfs(cls, req_oper, feature_id):
        # req_oper: GetMap,GetCapabilities
        data = {
            'service': 'WFS',
            'version': '1.3.0',
            'request': req_oper,
            'key': cls.apiKey,
            'output': 'text/xml;subType=gml/3.1.1/profiles/gmlsf/1.0.0/0',
            'exceptions': 'text/xml',
            'typename': 'LP_PA_CBND_BUBUN',
            'format': 'image/png',
            # 'featureid': feature_id,
            'propertyname': '',
            'maxfeatures': '1000',
            'sortby': '',
            'srsname': 'EPSG:4326',
            'domain': cls.domain,
            'width': '1000',
            'height': '256',
        }

        req = requests.post(cls.wfsUrl, data)

        return req

    # 토지이용계획도_WMS
    @classmethod
    def land_plan_map_for_wms(cls, req_oper, transparent, bgcolor):
        # req_oper: GetMap,GetCapabilities
        data = {
            'service': 'WMS',
            'version': '1.3.0',
            'request': req_oper,
            'key': cls.apiKey,
            'format': 'image/png',
            'exceptions': 'text/xml',
            'layers': 'LT_C_LHBLPN',
            'styles': 'LT_C_LHBLPN',
            'bbox': '33.1137120731772, 124.609708785584, 38.6137093106933, 131.872783431502',
            'width': 250,
            'height': 250,
            'transparent': transparent,
            'bgcolor': bgcolor,         # 0xFFFFFF
            'crs': 'EPSG:4326',
            'domain': cls.domain
        }

        req = requests.get(cls.wmsUrl, data)
        print(req.text)
        return req

    # 토지이용계획도_WFS
    @classmethod
    def land_plan_map_for_wfs(cls, req_oper, feature_id):
        # req_oper: GetMap,GetCapabilities
        data = {
            'service': 'WFS',
            'version': '1.1.0',
            'request': req_oper,
            'key': cls.apiKey,
            'output': 'text/xml;subType=gml/3.1.1/profiles/gmlsf/1.0.0/0',
            'exceptions': 'text/xml',
            'typename': 'LT_C_LHBLPN',
            'featureid': feature_id,
            'propertyname': '',
            'maxfeatures': '1000',
            'sortby': '',
            'srsname': 'EPSG:4326',
            'domain': cls.domain,
            'filter': ''
        }
        req = requests.post(cls.wmsUrl, data)

        return req.json()
