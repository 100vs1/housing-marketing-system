# -*- coding: utf-8 -*-
from flask_wtf import Form
from lib.util_wtforms import ModelForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import (
    Length,
    Optional
)


class SearchForm(Form):
    q = StringField('검색어', [Optional(), Length(1, 256)])


class PostForm(ModelForm):
    title = StringField('제목',
                        [DataRequired('필수 항목입니다.'), Length(1, 280)])
    body = TextAreaField('본문',
                         [DataRequired('필수 항목입니다.'), Length(1, 2000)])


class TagForm(ModelForm):
    name = StringField('태그',
                       [DataRequired('필수 항목입니다.'), Length(1, 40)])


class CommentForm(ModelForm):
    body = TextAreaField('댓글',
                         [DataRequired('필수 항목입니다.'), Length(1, 1000)])
