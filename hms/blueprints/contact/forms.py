# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextAreaField
from wtforms_components import EmailField
from wtforms.validators import DataRequired, Length


class ContactForm(Form):
    email = EmailField("이메일 주소",
                       [DataRequired('필수 항목입니다.'), Length(3, 254)])
    message = TextAreaField("문의 내용",
                            [DataRequired('필수 항목입니다.'), Length(1, 8192)])
