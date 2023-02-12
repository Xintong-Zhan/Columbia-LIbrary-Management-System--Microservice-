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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:11201120@e6156.cmvbbsiua9mw.us-east-1.rds.amazonaws.com/cu_library'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(13), primary_key=True)
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    press = db.Column(db.String(100))
    class_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % self.book_name

class Inventory(db.Model):
    __tablename__ = 'inventory'
    barcode = db.Column(db.String(6), primary_key=True)
    isbn = db.Column(db.ForeignKey('book.isbn'))
    storage_date = db.Column(db.String(13))
    location = db.Column(db.String(32))
    withdraw = db.Column(db.Boolean, default=False)  # 是否注销
    status = db.Column(db.Boolean, default=True)  # 是否在馆
    #admin = db.Column(db.ForeignKey('admin.admin_id'))  # 入库操作员
    admin = db.Column(db.String(13))  # 入库操作员
    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class ReadBook(db.Model):
    __tablename__ = 'readbook'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    #card_id = db.Column(db.ForeignKey('student.card_id'), index=True)
    card_id = db.Column(db.String(13), index=True)
    start_date = db.Column(db.String(13))
    #borrow_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 借书操作员
    borrow_admin = db.Column(db.String(13))  # 借书操作员
    end_date = db.Column(db.String(13), nullable=True)
    #return_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 还书操作员
    return_admin = db.Column(db.String(13))  # 还书操作员
    due_date = db.Column(db.String(13))  # 应还日期

    def __repr__(self):
        return '<ReadBook %r>' % self.id


'''
@app.get("/book_query1")
def admin_query():
    temp=copy.copy(request.args)
    user = ReadBook.query.filter_by(start_date=temp['start_date']).count()
    print(temp['admin_id'])
    msg={'id':user.id,'barcode':user.barcode,'card_id':user.card_id,'start_date':user.start_date,'borrow_admin':user.borrow_admin,\
         
         'end_date':user.end_date}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(result)
    return result
'''

def timeStamp(timeNum):
    if timeNum is None:
        return timeNum
    else:
        timeStamp = float(float(timeNum)/1000)
        timeArray = time.localtime(timeStamp)
        #print(time.strftime("%Y-%m-%d", timeArray))
        return time.strftime("%Y-%m-%d", timeArray)


@app.get("/book_query1")
def book_query1():
    temp = copy.copy(request.args)
    user = ReadBook.query.filter_by(start_date=temp['start_date']).count()
    msg={'count':user}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result


@app.get("/book_query2")
def book_query2():
    temp = copy.copy(request.args)
    user = ReadBook.query.filter_by(end_date=temp['end_date']).count()
    msg={'count':user}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result




@app.get("/book_query3")
def book_query3():
    temp = copy.copy(request.args)
    user = Book.query.filter(Book.book_name.like('%'+temp['book_name']+'%')).all()
    msg=[]
    for i in range(0,len(user)):
        tmp1={'isbn':user[i].isbn,'book_name':user[i].book_name,'author':user[i].author,'press':user[i].press,'class_name':user[i].class_name}
        msg.append(tmp1)
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result




@app.get("/book_query4")
def book_query4():
    temp = copy.copy(request.args)
    user =  Book.query.filter(Book.author.contains(temp['author'])).all()
    msg=[]
    for i in range(0,len(user)):
        tmp1={'isbn':user[i].isbn,'book_name':user[i].book_name,'author':user[i].author,'press':user[i].press,'class_name':user[i].class_name}
        msg.append(tmp1)
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/book_query5")
def book_query5():
    temp = copy.copy(request.args)
    user =  Book.query.filter(Book.class_name.contains(temp['class_name'])).all()
    msg=[]
    for i in range(0,len(user)):
        tmp1={'isbn':user[i].isbn,'book_name':user[i].book_name,'author':user[i].author,'press':user[i].press,'class_name':user[i].class_name}
        msg.append(tmp1)
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/book_query6")
def book_query6():
    temp = copy.copy(request.args)
    user =  Book.query.filter(Book.isbn.contains(temp['isbn'])).all()
    msg=[]
    for i in range(0,len(user)):
        tmp1={'isbn':user[i].isbn,'book_name':user[i].book_name,'author':user[i].author,'press':user[i].press,'class_name':user[i].class_name}
        msg.append(tmp1)
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/inventory_query1")
def inventory_query1():
    temp = copy.copy(request.args)
    user = Inventory.query.filter_by(isbn=temp['isbn']).count()
    msg = {'count': user}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result


@app.get("/inventory_query2")
def inventory_query2():
    temp = copy.copy(request.args)
    user = Inventory.query.filter_by(isbn=temp['isbn'], status=True).count()
    msg = {'count': user}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result



@app.get("/find_record_func")
def find_record_func():
    temp = copy.copy(request.args)
    records = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == temp['card_id']) \
        .with_entities(ReadBook.barcode, Inventory.isbn, Book.book_name, Book.author, ReadBook.start_date,
                       ReadBook.end_date, ReadBook.due_date).all()
    data=[]
    for record in records:
        start_date = timeStamp(record.start_date)
        due_date = timeStamp(record.due_date)
        end_date = timeStamp(record.end_date)
        if end_date is None:
            end_date = 'Not returned'
        item = {'barcode': record.barcode, 'book_name': record.book_name, 'author': record.author,
                'start_date': start_date, 'due_date': due_date, 'end_date': end_date}
        data.append(item)
    return jsonify(data)


@app.get("/book_query7")
def book_query7():
    temp = copy.copy(request.args)
    user = Book.query.filter_by(isbn=temp['isbn']).first()
    msg = {'isbn': user[i].isbn, 'book_name': user[i].book_name, 'author': user[i].author, 'press': user[i].press,
            'class_name': user[i].class_name}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result


@app.get("/book_query8")
def book_query8():
    temp = copy.copy(request.args)
    user = Inventory.query.filter_by(barcode=temp['barcode']).first()
    msg={'barcode':user.barcode,'isbn':user.isbn,'storage_date':user.storage_date,'location':user.location,'withdraw':user.withdraw,'status':user.status,'admin':user.admin}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/book_add1")
def book_add1():
    temp = copy.copy(request.args)

    item = Inventory()
    item.barcode = temp['barcode']
    item.isbn = temp['isbn']
    item.admin = temp['admin']
    item.location = temp['location']
    item.status = True
    item.withdraw = False
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    item.storage_date = int(today_stamp) * 1000
    db.session.add(item)
    db.session.commit()
    msg={'test':True}
    return Response(json.dumps(msg), status=200, content_type="application/json")



@app.get("/book_query9")
def book_query9():
    temp = copy.copy(request.args)
    print(temp['isbn'])
    user = Book.query.filter_by(isbn=temp['isbn']).first()
    print(user)
    if user is not None:
        msg={'word':'yes'}
    else:
        msg={'word':'no'}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result



@app.get("/book_add2")
def book_add2():
    temp = copy.copy(request.args)
    book = Book()
    book.isbn = temp['isbn']
    book.book_name = temp['book_name']
    book.press = temp['press']
    book.author = temp['author']
    book.class_name = temp['class_name']
    db.session.add(book)
    db.session.commit()
    msg={'test':True}
    return Response(json.dumps(msg), status=200, content_type="application/json")



@app.get("/booksquery")
def booksquery():
    temp = copy.copy(request.args)
    books = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(temp['book_name']),
                                                          Inventory.status == 1).with_entities(Inventory.barcode,
                                                                                               Book.isbn,
                                                                                               Book.book_name,
                                                                                               Book.author, Book.press).all()
    data = []
    for book in books:
        item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
                'author': book.author, 'press': book.press}
        data.append(item)
    return jsonify(data)



@app.get("/book_out")
def book_out():
    temp = copy.copy(request.args)
    readbook = ReadBook()
    readbook.barcode = temp['barcode']
    readbook.card_id = temp['card_id']
    readbook.start_date = temp['start_date']
    readbook.due_date = temp['due_date']
    readbook.borrow_admin = temp['borrow_admin']
    db.session.add(readbook)
    db.session.commit()
    msg={'test':True}
    return Response(json.dumps(msg), status=200, content_type="application/json")

@app.get("/book_query10")
def book_query10():
    temp = copy.copy(request.args)
    book = Inventory.query.filter_by(barcode=temp['barcode']).first()
    book.status = False
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(temp['book_name']), Inventory.status == 1). \
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'author': bk.author, 'press': bk.press}
        data.append(item)
    return jsonify(data)


@app.get("/book_not")
def book_not():
    temp = copy.copy(request.args)
    
    books = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == temp['card_id'],
                                                                         ReadBook.end_date.is_(None)).with_entities(
        ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
        ReadBook.due_date).all()
    data = []
    for book in books:
        start_date = timeStamp(book.start_date)
        due_date = timeStamp(book.due_date)
        item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    print(data[0])
    return jsonify(data)



@app.get("/book_in")
def book_in():
    temp = copy.copy(request.args)
    record = ReadBook.query.filter(ReadBook.barcode == temp['barcode'], ReadBook.card_id == temp['card_id'],
                                   ReadBook.end_date.is_(None)).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    record.end_date = int(today_stamp) * 1000
    record.return_admin = temp['admin_id']

    db.session.add(record)
    db.session.commit()

    book = Inventory.query.filter_by(barcode=temp['barcode']).first()
    book.status = True
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == temp['card_id'],
                                                                       ReadBook.end_date.is_(None)).with_entities(
        ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
        ReadBook.due_date).all()
    data = []
    for bk in bks:
        start_date = timeStamp(bk.start_date)
        due_date = timeStamp(bk.due_date)
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)



    



@app.get("/sns_query")
def sns_query():
    temp = copy.copy(request.args)
    book_out = db.session.query(Book).join(Inventory).filter(Inventory.barcode.contains(temp['barcode']),
                                                             Inventory.status == 0). \
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).first()
    msg={'book_name':book_out.book_name}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

@app.get("/sns_query2")
def sns_query2():
    temp = copy.copy(request.args)
    book_in = db.session.query(Book).join(Inventory).filter(Inventory.barcode.contains(temp['barcode']),
                                                            Inventory.status == 1). \
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).first()
    msg={'book_name':book_in.book_name}
    result = Response(json.dumps(msg), status=200, content_type="application/json")
    print(msg)
    return result

if __name__ == '__main__':
    manager.run()
