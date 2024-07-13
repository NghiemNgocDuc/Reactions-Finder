from flask_security import UserMixin, RoleMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))) 

class Users(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    active = db.Column(db.Boolean())
    
    roles = db.relationship('Role', secondary=roles_users, backref='roled')

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            
            if hasattr(value, '__iter__') and not isinstance(value, str):
                
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None


        