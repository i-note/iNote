from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_babel import gettext as _
from app.models import User


class LoginForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_('Keep me logged in'))
    submit = SubmitField(_('Login'))


class RegistrationForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(_('Username'), validators=[DataRequired(), Length(1, 64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, _(
                                                          'Usernames must have only letters, numbers, dots or underscores'))])
    password = PasswordField(_('Password'),
                             validators=[DataRequired(), Length(6, 20, message=_('Passwords must >=6 and <=20.')),
                                         EqualTo('confirm', message=_('Passwords must match.'))])
    confirm = PasswordField(_('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(_('Register'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(_('Username already in use.'))


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(_('Old password'), validators=[DataRequired()])
    password = PasswordField(_('New password'), validators=[
        DataRequired(), Length(6, 20, message=_('Passwords must >=6 and <=20.'))
        , EqualTo('confirm', message=_('Passwords must match'))])
    confirm = PasswordField(_('Confirm new password'), validators=[DataRequired()])
    submit = SubmitField(_('Update Password'))


class PasswordResetRequestForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 64),
                                                Email()])
    submit = SubmitField(_('Reset Password'))


class PasswordResetForm(FlaskForm):
    email = StringField(_('Email'), validators=[DataRequired(), Length(1, 64),
                                                Email()])
    password = PasswordField(_('New Password'), validators=[
        DataRequired(), EqualTo('confirm', message=_('Passwords must match'))])
    confirm = PasswordField(_('Confirm password'), validators=[DataRequired()])
    submit = SubmitField(_('Reset Password'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(_('Unknown email address.'))


class ChangeEmailForm(FlaskForm):
    email = StringField(_('New Email'), validators=[DataRequired(), Length(1, 64),
                                                    Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])
    submit = SubmitField(_('Update Email Address'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(_('Email already registered.'))
