from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify, Response
import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from forms import Login, SearchBookForm, ChangePasswordForm, EditInfoForm, SearchStudentForm, NewStoreForm, StoreForm, \
    BorrowForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import time, datetime
import json

import copy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:11201120@e6156.cmvbbsiua9mw.us-east-1.rds.amazonaws.com/cu_library'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = 'student'
    card_id = db.Column(db.String(8), primary_key=True)
    student_id = db.Column(db.String(9))
    student_name = db.Column(db.String(32))
    sex = db.Column(db.String(2))
    telephone = db.Column(db.String(11), nullable=True)
    enroll_date = db.Column(db.String(13))
    valid_date = db.Column(db.String(13))
    loss = db.Column(db.Boolean, default=False)  # 是否挂失
    debt = db.Column(db.Boolean, default=False)  # 是否欠费

    def __repr__(self):
        return '<Student %r>' % self.student_name

def timeStamp(timeNum):
    if timeNum is None:
        return timeNum
    else:
        timeStamp = float(float(timeNum)/1000)
        timeArray = time.localtime(timeStamp)
        print(time.strftime("%Y-%m-%d", timeArray))
        return time.strftime("%Y-%m-%d", timeArray)

@app.get("/student_query1")
def student_query1():
    temp = copy.copy(request.args)
    user = Student.query.filter_by(card_id=temp['card_id']).first()
    msg = {'card_id':user.card_id ,'student_id':user.student_id,'student_name':user.student_name,'sex':user.sex,'telephone':user.telephone,'enroll_date':user.enroll_date,'valid_date':user.valid_date,'loss':user.loss,'debt':user.debt}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/book_query9")
def book_query9():
    temp = copy.copy(request.args)
    user = Student.query.filter_by(card_id=temp['card_id']).first()
    if user is None:
        msg={'student_name':'Not found'}
    else:
        msg = {'card_id':user.card_id ,'student_id':user.student_id,'student_name':user.student_name,'sex':user.sex,'telephone':user.telephone,'enroll_date':user.enroll_date,'valid_date':user.valid_date,'loss':user.loss,'debt':user.debt}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/book_query11")
def book_query11():

    temp = copy.copy(request.args)
    user = Student.query.filter_by(card_id=temp['card_id']).first()
    if user is None:
        msg={'student_name':'Not found'}
    else:
        msg = {'card_id':user.card_id ,'student_id':user.student_id,'student_name':user.student_name,'sex':user.sex,'telephone':user.telephone,'enroll_date':user.enroll_date,'valid_date':user.valid_date,'loss':user.loss,'debt':user.debt}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result





if __name__ == '__main__':
    manager.run()
