from flask import render_template, url_for, request, flash, redirect, current_app
from flask_login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm, \
    ChangeEmailForm
from . import auth
from app.models import User, Role
from flask_babel import gettext as _
from app import db
from app.utils.email import send_email
from app.inote.utils.iNoteCategoryUtils import iNoteCategoryUtil


@auth.route('/', methods=['get', 'post'])
@auth.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            # login successful
            logout_user()
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            return redirect(next or url_for('main.index'))
        flash(_('Invalid username or password.'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout', methods=['get', 'post'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, role_id=1)
        print(user)
        print(user.verify_password(form.password.data))
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, _('Confirm Your Account'),
                   'auth/email/confirm', user=user, token=token)
        flash(_('Registration Successful.'))
        flash(_('A confirmation email has been sent to you by email.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    print('confirm 0')
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        iNoteCategoryUtil.init()
        flash(_('You have confirmed your account. Thanks!'))
    else:
        flash(_('The confirmation link is invalid or has expired.'))
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[
                                                                        :5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed', methods=['POST', 'GET'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, _('Confirm Your Account'),
               'auth/email/confirm', user=current_user, token=token)
    print('resend ', token)
    flash(_('A new confirmation email has been sent to you by email.'))
    return redirect(url_for('main.index'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(_('Your password has been updated.'))
            return redirect(url_for('main.index'))
        else:
            flash(_('Invalid password.'))
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, _('Reset Your Password'),
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash(_('An email with instructions to reset your password has been sent to you.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash(_('Your password has been updated.'))
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, _('Confirm your email address'),
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash(_('An email with instructions to confirm your new email address has been sent to you.'))
            return redirect(url_for('main.index'))
        else:
            flash(_('Invalid email or password.'))
    return render_template("auth/change_email.html", form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(_('Your email address has been updated.'))
    else:
        flash(_('Invalid request.'))
    return redirect(url_for('main.index'))
