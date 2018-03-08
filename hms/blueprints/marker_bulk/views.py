# -*- coding: utf-8 -*-
import csv
import sys
import uuid

from flask import Blueprint, request, jsonify, render_template, json
from flask_login import current_user, login_required

from hms.blueprints.marker_bulk.models import bulk_marker
from hms.blueprints.marker_bulk.models.bulk_history import BulkHistory
from hms.blueprints.marker_bulk.models.bulk_marker import BulkMarker
from hms.blueprints.rest_api.models.vWordlAPI import VWorldAPI
from lib.util_json import render_json

bulk_upload = Blueprint('bulk_upload', __name__, url_prefix='/bulk_upload')

@bulk_upload.route('/data_setting')
@login_required
def data_setting():
    return render_template('user/data_setting.html')


@bulk_upload.route('/response_test', methods=['GET', 'POST'])
@login_required
def response_test():
    return 'OK'


@bulk_upload.route('/srch_bulk_history', methods=['POST'])
@login_required
def srch_bulk_history():
    items = BulkHistory.find_by_user_id(current_user.id)

    return render_json(200, rows=[{
        'file_name': item.file_name,
        'total_cnt': item.total_cnt,
        'success_cnt': item.success_cnt,
        'fail_cnt': item.fail_cnt,
        'summary_info': item.summary_info,
        'created_on': item.created_on,
    } for item in items])


@bulk_upload.route('/get_bulk_categorys', methods=['POST'])
@login_required
def get_bulk_categorys():
    items = BulkMarker.find_not_replication_categorys(current_user.id)

    return render_json(200, rows=[{
        'category': item.category
    } for item in items])


@bulk_upload.route('/get_bulks', methods=['POST'])
@login_required
def get_bulks():
    category = request.form.getlist('category')

    items = BulkMarker.find_by_categorys(current_user.id, category)

    return render_json(200, rows=[{
        'idx': item.idx,
        'user_id': item.user_id,
        'category': item.category,
        'title': item.title,
        'content': item.content,
        'address': item.address,
        'geom': json.loads(item.geom)['coordinates'],
        'number1': item.number1,
        'number2': item.number2,
        'number3': item.number3,
        'number4': item.number4,
        'number5': item.number5,
        'string1': item.string1,
        'string2': item.string2,
        'string3': item.string3,
        'string4': item.string4,
        'string5': item.string5,
        'created_on': item.created_on,
        'updated_on': item.updated_on,
        'img_name': item.img_name
    } for item in items])


@bulk_upload.route('/get_cols', methods=['POST'])
@login_required
def get_cols():
    csv_file = request.files['file']
    csv_input = csv.reader(csv_file)
    cols = csv_input.next()
    first_rows = csv_input.next()

    row_count = sum(1 for row in csv_input)

    if row_count > 5000:
        return jsonify({
            'status': '500',
            'msg': '데이터 row 수가 너무 많습니다. (' + str(row_count) + ')'
        })

    print (sys.stdin.encoding)
    print (sys.stdout.encoding)

    # TODO : 컬럼수로 정합하게 할 것.
    ret = []
    for i in range(len(cols)):
        temp_ret_row = {
            'col': cols[i],
            'first_row': first_rows[i]
        }
        ret.append(temp_ret_row)

    return jsonify(results=ret)


@bulk_upload.route('/save_data', methods=['POST'])
@login_required
def save_data():
    target_file = request.files['file']
    match_info = request.form.getlist('match_info')

    print(match_info)

    match_data = {}
    for info in match_info:
        print(json.loads(info)['row'])
        print(json.loads(info)['field'])

        if json.loads(info)['field'] is not 'null' and json.loads(info)['field'] is not u'':
            match_data[json.loads(info)['field']] = json.loads(info)['row']

    csv_input = csv.reader(target_file)

    total_cnt = 0
    success_cnt = 0
    fail_cnt = 0
    fail_reason = []

    history_idx = uuid.uuid4();
    for row in csv_input:
        if u'category' in match_data:
            category = row[match_data[u'category']]
        else:
            category = None

        if u'title' in match_data:
            title = row[match_data[u'title']]
        else:
            title = None

        if u'content' in match_data:
            content = row[match_data[u'content']]
        else:
            content = None
                
        if u'address' in match_data:
            address = row[match_data[u'address']]
        else:
            address = None
            
        if u'number1' in match_data:
            number1 = row[match_data[u'number1']]
        else:
            number1 = None
            
        if u'number2' in match_data:
            number2 = row[match_data[u'number2']]
        else:
            number2 = None
            
        if u'number3' in match_data:
            number3 = row[match_data[u'number3']]
        else:
            number3 = None
            
        if u'number4' in match_data:
            number4 = row[match_data[u'number4']]
        else:
            number4 = None
            
        if u'number5' in match_data:
            number5 = row[match_data[u'number5']]
        else:
            number5 = None
            
        if u'string1' in match_data:
            string1 = row[match_data[u'string1']]
        else:
            string1 = None
            
        if u'string2' in match_data:
            string2 = row[match_data[u'string2']]
        else:
            string2 = None

        if u'string3' in match_data:
            string3 = row[match_data[u'string3']]
        else:
            string3 = None

        if u'string4' in match_data:
            string4 = row[match_data[u'string4']]
        else:
            string4 = None

        if u'string5' in match_data:
            string5 = row[match_data[u'string5']]
        else:
            string5 = None

        if total_cnt is not 0:
            addr_result = VWorldAPI.search(address, 'ADDRESS', 'ROAD')
            if addr_result['status'] == 'OK':
                # coordinates = addr_result['result']['items']['item']['point']
                coordinates = addr_result['result']['items'][0]['point']

                lat = coordinates['x']
                lon = coordinates['y']

                BulkMarker.insert_data(current_user.id, history_idx,
                                       category, title, content, address,
                                       lon, lat,
                                       number1, number2, number3, number4, number5,
                                       string1, string2, string3, string4, string5,
                                       'text')

                total_cnt += 1
                success_cnt += 1
            else:
                fail_reason.append(addr_result['status'])
                fail_cnt += 1
                total_cnt += 1
        else:
            # 헤더 처리
            total_cnt += 1
    BulkHistory.insert_data(history_idx, current_user.id, target_file.filename, success_cnt + fail_cnt,
                            success_cnt, fail_cnt)

    return jsonify({'successCnt': success_cnt, 'failCnt': fail_cnt, 'failReason': fail_reason})