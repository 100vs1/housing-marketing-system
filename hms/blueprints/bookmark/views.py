# -*- coding: utf-8 -*-
from flask import Blueprint, request, jsonify, json
from flask_login import current_user, login_required
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

from lib.util_json import render_json
from hms.blueprints.bookmark.models import Bookmark

bookmark = Blueprint('bookmark', __name__, url_prefix='/bookmarks')


@bookmark.before_request
@login_required
def before_request():
    pass


@bookmark.route('', methods=['GET', 'POST'])
def select_bookmark():
    page = int(request.form.get('bookmark_page'))
    if page is None:
        page = 1

    per_page = 10

    recent_bookmarks = Bookmark.query.filter(Bookmark.user_id == current_user.id) \
        .order_by(Bookmark.created_on.desc()).limit(per_page).offset((page - 1) * per_page)

    # print(recent_bookmarks.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))

    items = [{
        'id': bookmark.id,
        'user_id': bookmark.user_id,
        'name': bookmark.name,
        'target': bookmark.target,
        'parameter': bookmark.parameter
    } for bookmark in recent_bookmarks.all()]

    return render_json(200, items=items)


@bookmark.route('/add', methods=['POST'])
def insert_bookmark():
    name = request.form.get('name')
    target = request.form.get('target')
    parameter = request.form.get('parameter')

    if name and target and parameter:
        obj = Bookmark()
        obj.user_id = current_user.id
        obj.name = name
        obj.target = target
        obj.parameter = parameter

        obj.save()

        return render_json(200, {'msg': '저장되었습니다.'})

    return render_json(400, {'msg': '저장되지 않았습니다.'})


@bookmark.route('/edit', methods=['POST'])
def update_bookmark():
    id = request.form.get('id')
    name = request.form.get('name')

    obj = Bookmark.query.get(id)

    if obj and name and obj.user_id == current_user.id:
        obj.name = name
        obj.save()

        return render_json(200, {'msg': '수정되었습니다.'})

    return render_json(400, {'msg': '수정되지 않았습니다.'})


@bookmark.route('/delete', methods=['POST'])
def delete_bookmark():
    id = request.form.get('id')

    obj = Bookmark.query.get(id)

    if obj and obj.user_id == current_user.id:
        obj.delete()

        return render_json(200, {'msg': '삭제되었습니다.'})

    return render_json(400, {'msg': '삭제되지 않았습니다.'})
