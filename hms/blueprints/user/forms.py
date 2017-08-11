# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import HiddenField, StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from wtforms_components import EmailField, Email, Unique

from config.settings import LANGUAGES
from lib.util_wtforms import ModelForm, choices_from_dict
from hms.blueprints.user.models import User, db
from hms.blueprints.user.validations import ensure_identity_exists, \
    ensure_existing_password_matches


class LoginForm(Form):
    next = HiddenField()
    identity = StringField('이메일',
                           [DataRequired(), Length(3, 254)])
    password = PasswordField('비밀번호', [DataRequired(), Length(8, 128)])
    # remember = BooleanField('Stay signed in')


class BeginPasswordResetForm(Form):
    identity = StringField('이메일',
                           [DataRequired(),
                            Length(3, 254),
                            ensure_identity_exists])


class PasswordResetForm(Form):
    reset_token = HiddenField()
    password = PasswordField('비밀번호', [DataRequired(), Length(8, 128)])


class SignupForm(ModelForm):
    email = EmailField(validators=[
        DataRequired(),
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('비밀번호', [DataRequired(), Length(8, 128)])


class WelcomeForm(ModelForm):
    username_message = '문자와 숫자만 입력해주세요.'

    username = StringField(validators=[
        Unique(
            User.username,
            get_session=lambda: db.session
        ),
        DataRequired(),
        Length(1, 16),
        Regexp('^\w+$', message=username_message)
    ])


class UpdateCredentialsForm(ModelForm):
    current_password = PasswordField('현재 비밀번호',
                                     [DataRequired(),
                                      Length(8, 128),
                                      ensure_existing_password_matches])

    email = EmailField(validators=[
        Email(),
        Unique(
            User.email,
            get_session=lambda: db.session
        )
    ])
    password = PasswordField('새로운 비밀번호', [Optional(), Length(8, 128)])


class UpdateLocaleForm(Form):
    locale = SelectField('사용 언어', [DataRequired()],
                         choices=choices_from_dict(LANGUAGES,
                                                   prepend_blank=False))
