

from flask import render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_user,
    logout_user
)

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Role, Users

from apps.authentication.util import verify_pass
from apps.pu_hh.forms import TimkiemPuHhForm



@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)     
            if user.roles[0].name == 'Admin':      
                #return admin
                return render_template('pu_hh/tim_kiem_admin.html', msg='', form=TimkiemPuHhForm(request.form))
            else:
                #return normal user
                return redirect('/tim_kiem_pu_hh')
            
            #return redirect(url_for('authentication_blueprint.route_default'))           
        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Sai thông tin đăng nhập',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Tên đăng nhập đã tồn tại',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email đã đăng ký',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        role = Role.query.filter_by(name='Normal').first()
        user.roles.append(role)
        user.active = True

        try:
            db.session.add(user)
            db.session.commit()        
        except Exception as expt:
            print (expt)
            return render_template('home/page-500.html'), 500

        return render_template('accounts/register.html',
                               
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500

@blueprint.route('/change_password', methods=['GET', 'POST'])
def change_password():
    create_account_form = CreateAccountForm(request.form)
    if 'change_password' in request.form:

        userIdStr = current_user.get_id()

        userUpdate = Users(**request.form)
        
        # Check usename exists
        user = Users.query.filter_by(id=userIdStr).first()
        if user:
            user.password = userUpdate.password
            try:            
                db.session.commit()        
            except Exception as expt:
                print (expt)
                return render_template('home/page-500.html'), 500

        return render_template('accounts/change_password.html',
                               
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/change_password.html', form=create_account_form)
