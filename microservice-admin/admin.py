from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify,Response
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from forms import Login, SearchBookForm, ChangePasswordForm, EditInfoForm, SearchStudentForm, NewStoreForm, StoreForm, BorrowForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import time, datetime
import json

import copy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)

app.config['SECRET_KEY'] = 'hard to guess string'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:zxt13131036@localhost/cu_library_6156'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:11201120@e6156.cmvbbsiua9mw.us-east-1.rds.amazonaws.com/cu_library'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

#class Admin(UserMixin, db.Model):
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.String(6), primary_key=True)
    admin_name = db.Column(db.String(32))
    password = db.Column(db.String(24))
    right = db.Column(db.String(32))

    def __init__(self, admin_id, admin_name, password, right):
        self.admin_id = admin_id
        self.admin_name = admin_name
        self.password = password
        self.right = right

    def get_id(self):
        return self.admin_id

    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def __repr__(self):
        return '<Admin %r>' % self.admin_name




@app.get("/admin_query")
def admin_query():
    temp=copy.copy(request.args)
    user = Admin.query.filter_by(admin_id=temp['admin_id'], password=temp['password']).first()
    print(temp['admin_id'])
    msg={'admin_id':user.admin_id,'admin_name':user.admin_name,'password':user.password,'right':user.right}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(result)
    return result


if __name__ == '__main__':
    manager.run()
