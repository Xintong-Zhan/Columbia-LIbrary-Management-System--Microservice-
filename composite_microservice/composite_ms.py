from flask import Flask, render_template, session, redirect, url_for, flash, request, jsonify
import os
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from forms import Login, SearchBookForm, ChangePasswordForm, EditInfoForm, SearchStudentForm, NewStoreForm, StoreForm, BorrowForm
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
import time, datetime
import boto3

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://admin:11201120@e6156.cmvbbsiua9mw.us-east-1.rds.amazonaws.com/cu_library'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

'''
def make_shell_context():
    return dict(app=app, db=db, Admin=Admin, Book=Book)


manager.add_command("shell", Shell(make_context=make_shell_context))
'''
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'basic'
login_manager.login_view = 'login'
login_manager.login_message = u"Please login first!"

#admin_server_url=
readbook_server_url="http://18.216.35.187:5000"
student_server_url="http://3.141.15.137:5000"

class Admin(UserMixin, db.Model):
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




class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(13), primary_key=True)
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    press = db.Column(db.String(32))
    class_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % self.book_name


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


class Inventory(db.Model):
    __tablename__ = 'inventory'
    barcode = db.Column(db.String(6), primary_key=True)
    isbn = db.Column(db.ForeignKey('book.isbn'))
    storage_date = db.Column(db.String(13))
    location = db.Column(db.String(32))
    withdraw = db.Column(db.Boolean, default=False)  # 是否注销
    status = db.Column(db.Boolean, default=True)  # 是否在馆
    admin = db.Column(db.ForeignKey('admin.admin_id'))  # 入库操作员

    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class ReadBook(db.Model):
    __tablename__ = 'readbook'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    card_id = db.Column(db.ForeignKey('student.card_id'), index=True)
    start_date = db.Column(db.String(13))
    borrow_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 借书操作员
    end_date = db.Column(db.String(13), nullable=True)
    return_admin = db.Column(db.ForeignKey('admin.admin_id'))  # 还书操作员
    due_date = db.Column(db.String(13))  # 应还日期

    def __repr__(self):
        return '<ReadBook %r>' % self.id


@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(admin_id)


def get_db(db_server_url,function_name,query):

    url=db_server_url+'/'+str(function_name)+'?'+query
    print(url)
    x = (requests.get(url)).json()
    if type(x)==dict:
        x=[x]

    print(x)
    return x

def make_query(query_list):
    query=''
    for i in range(0,int(len(query_list)/2)):
        if i==0:
            query = query+ str(query_list[2 * i]) + '=' + str(query_list[2 * i + 1])
        else:
            query=query+'&'+str(query_list[2*i])+'='+str(query_list[2*i+1])
    return query

'''
def get_db(db_server_url,db_query):

    x = requests.post(db_server_url,json=db_query)
    return x.json()

'''
@app.route('/', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():

        user_db = Admin.query.filter_by(admin_id=form.account.data, password=form.password.data).first()
        '''
        admin_query=['admin_id',str(form.account.data),'password',str(form.password.data)]
        function_name="admin_query"
        admin_query=make_query(admin_query)
        user=get_db(admin_server_url,function_name,admin_query)[0]
        print(user)
        print(user['admin_id'])
        '''
        #temp_admin = Admin(admin_id=user['admin_id'], admin_name=user['admin_name'], password=user['password'],right=user['right'])
        if user_db is None:
            flash('username or password error！')
            return redirect(url_for('login'))
        else:
            login_user(user_db)
            session['admin_id'] = user_db.admin_id
            session['name'] = user_db.admin_name
            return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Successfully!')
    return redirect(url_for('login'))


@app.route('/index') #/student/<id> return id
@login_required
def index():
    return render_template('index.html', name=session.get('name'))


@app.route('/echarts')
@login_required
def echarts():
    days = []
    num = []
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    ten_ago = int(today_stamp) - 9 * 86400
    for i in range(0, 10):
        #borr = ReadBook.query.filter_by(start_date=str((ten_ago+i*86400)*1000)).count()
        book_query1 = ['start_date', str((ten_ago + i * 86400) * 1000)]
        function_name = 'book_query1'
        book_query1 = make_query(book_query1)
        borr = get_db(readbook_server_url, function_name, book_query1)[0]['count']

        #retu = ReadBook.query.filter_by(end_date=str((ten_ago+i*86400)*1000)).count()
        book_query2 = ['end_date', str((ten_ago+i*86400)*1000)]
        function_name = 'book_query2'
        book_query2 = make_query(book_query2)
        retu = get_db(readbook_server_url, function_name, book_query2)[0]['count']

        num.append(borr + retu)
        days.append(timeStamp((ten_ago+i*86400)*1000))
    data = []
    for i in range(0, 10):
        item = {'name': days[i], 'num': num[i]}
        data.append(item)
    return jsonify(data)


@app.route('/user/<id>')
@login_required
def user_info(id):
    user = Admin.query.filter_by(admin_id=id).first()
    '''
    admin_query1 = ['admin_id', str(id)]
    function_name = "admin_query1"
    admin_query1 = make_query(admin_query1)
    user = get_db(admin_server_url, function_name, admin_query1)[0]
    '''
    return render_template('user-info.html', user=user, name=session.get('name'))


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.password2.data != form.password.data:
        flash(u'Inconsistent with the password above!')
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'Change password successfully!')
            return redirect(url_for('index'))
        else:
            flash(u'Wrong original password. Change Failed!')
    return render_template("change-password.html", form=form)


@app.route('/change_info', methods=['GET', 'POST'])
@login_required
def change_info():
    form = EditInfoForm()
    if form.validate_on_submit():
        current_user.admin_name = form.name.data
        db.session.add(current_user)
        flash(u'Change personal information successfully!')
        return redirect(url_for('user_info', id=current_user.admin_id))
    form.name.data = current_user.admin_name
    id = current_user.admin_id
    right = current_user.right
    return render_template('change-info.html', form=form, id=id, right=right)


@app.route('/search_book', methods=['GET', 'POST'])
@login_required
def search_book():  # 这个函数里不再处理提交按钮，使用Ajax局部刷新
    form = SearchBookForm()
    return render_template('search-book.html', name=session.get('name'), form=form)



@app.route('/books', methods=['POST'])
def find_book():

    def find_name():
        book_query3 = ['book_name',request.form.get('content')]
        function_name = 'book_query3'
        book_query3 = make_query(book_query3)
        get_db1 = get_db(readbook_server_url, function_name, book_query3)
        return get_db1
        #return Book.query.filter(Book.book_name.like('%'+request.form.get('content')+'%')).all()

    def find_author():
        book_query4 = ['author', request.form.get('content')]
        function_name = 'book_query4'
        book_query4 = make_query(book_query4)
        get_db2 = get_db(readbook_server_url, function_name, book_query4)
        return get_db2
        #return Book.query.filter(Book.author.contains(request.form.get('content'))).all()

    def find_class():
        book_query5 = ['class_name', request.form.get('content')]
        function_name = 'Book'
        book_query5 = make_query(book_query5)
        get_db3 = get_db(readbook_server_url, function_name, book_query5)
        return get_db3
        #return Book.query.filter(Book.class_name.contains(request.form.get('content'))).all()

    def find_isbn():
        book_query6 = ['isbn', request.form.get('content')]
        function_name = 'book_query6'
        book_query6 = make_query(book_query6)
        get_db4 = get_db(readbook_server_url, function_name, book_query6)
        return get_db4
        #return Book.query.filter(Book.isbn.contains(request.form.get('content'))).all()

    methods = {
        'book_name': find_name,
        'author': find_author,
        'class_name': find_class,
        'isbn': find_isbn
    }
    books = methods[request.form.get('method')]()
    data = []

    for book in books:

        inventory_query1 = ['isbn', book['isbn']]
        function_name = 'inventory_query1'
        inventory_query1 = make_query(inventory_query1)
        count = get_db(readbook_server_url, function_name, inventory_query1)[0]['count']
        #count = Inventory.query.filter_by(isbn=book.isbn).count()

        inventory_query2 = ['isbn', book['isbn'], 'status',True]
        function_name = 'inventory_query2'
        inventory_query2 = make_query(inventory_query2)
        available = get_db(readbook_server_url, function_name, inventory_query2)[0]['count']
        #available = Inventory.query.filter_by(isbn=book.isbn, status=True).count()

        item = {'isbn': book['isbn'], 'book_name': book['book_name'], 'press': book['press'], 'author': book['author'],
                'class_name': book['class_name'], 'count':count, 'available': available}
        data.append(item)
    return jsonify(data)


@app.route('/user/book', methods=['GET', 'POST'])
def user_book():
    form = SearchBookForm()
    return render_template('user-book.html', form=form)


@app.route('/search_student', methods=['GET', 'POST'])
@login_required
def search_student():
    form = SearchStudentForm()
    return render_template('search-student.html', name=session.get('name'), form=form)


def timeStamp(timeNum):
    if timeNum is None:
        return timeNum
    else:
        timeStamp = float(float(timeNum)/1000)
        timeArray = time.localtime(timeStamp)
        print(time.strftime("%Y-%m-%d", timeArray))
        return time.strftime("%Y-%m-%d", timeArray)


@app.route('/student', methods=['POST'])
def find_student():

    student_query1 = ['card_id', request.form.get('card')]
    function_name = 'student_query1'
    student_query1 = make_query(student_query1)
    stu = get_db(student_server_url, function_name, student_query1)[0]

    #stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    if stu is None:
        return jsonify([])
    else:
       # valid_date = timeStamp(stu.valid_date)
       # return jsonify([{'name': stu.student_name, 'gender': stu.sex, 'valid_date': valid_date, 'debt': stu.debt}])
        valid_date = timeStamp(stu['valid_date'])
        return jsonify([{'name': stu['student_name'], 'gender': stu['sex'], 'valid_date': valid_date, 'debt': stu['debt']}])


@app.route('/record', methods=['POST'])
def find_record():
    find_record_func = ['card_id', request.form.get('card')]
    function_name = 'find_record_func'
    find_record_func = make_query(find_record_func)
    stu = get_db(readbook_server_url, function_name, find_record_func)
    return stu

'''
def find_record():
    records = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == request.form.get('card'))\
        .with_entities(ReadBook.barcode, Inventory.isbn, Book.book_name, Book.author, ReadBook.start_date,
                       ReadBook.end_date, ReadBook.due_date).all()  # with_entities啊啊啊啊卡了好久啊
    data = []
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
'''

@app.route('/user/student', methods=['GET', 'POST'])
def user_student():
    form = SearchStudentForm()
    return render_template('user-student.html', form=form)


@app.route('/storage', methods=['GET', 'POST'])
@login_required
def storage():
    form = StoreForm()
    if form.validate_on_submit():

        book_query7 = ['isbn', request.form.get('isbn')]
        function_name = 'book_query7'
        book_query7 = make_query(book_query7)
        stu = get_db(readbook_server_url, function_name, book_query7)
        #book = Book.query.filter_by(isbn=request.form.get('isbn')).first()

        book_query8 = ['barcode', request.form.get('barcode')]
        function_name = 'book_query8'
        book_query8 = make_query(book_query8)
        stu = get_db(readbook_server_url, function_name, book_query8)
        #exist = Inventory.query.filter_by(barcode=request.form.get('barcode')).first()
        if book is None:
            flash(u'Failed to add. Please note whether the book information has been entered. If not, please enter the information in the "Store" window.')
        else:
            if len(request.form.get('barcode')) != 6:
                flash(u'Book number length error')
            else:
                if exist is not None:
                    flash(u'This number already exists!')
                else:
                    book_add1 = ['barcode', request.form.get('barcode'),'isbn',request.form.get('isbn'),'admin',current_user.admin_id,\
                                 'location',request.form.get('location'),'status',True,'withdraw',False]
                    function_name = 'book_add1'
                    book_add1 = make_query(book_add1)
                    stu = get_db(readbook_server_url, function_name, book_add1)
                    if stu['test']==True:
                        flash(u'Store successfully！')
                    '''
                    item = Inventory()
                    item.barcode = request.form.get('barcode')
                    item.isbn = request.form.get('isbn')
                    item.admin = current_user.admin_id
                    item.location = request.form.get('location')
                    item.status = True
                    item.withdraw = False
                    today_date = datetime.date.today()
                    today_str = today_date.strftime("%Y-%m-%d")
                    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
                    item.storage_date = int(today_stamp)*1000
                    db.session.add(item)
                    db.session.commit()
                    flash(u'Store successfully！')
                    '''
        return redirect(url_for('storage'))
    return render_template('storage.html', name=session.get('name'), form=form)


@app.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = NewStoreForm()
    if form.validate_on_submit():
        if len(request.form.get('isbn')) != 13:
            flash(u'ISBN length error!')
        else:
            book_query9 = ['isbn', request.form.get('isbn')]
            function_name = 'book_query9'
            book_query9 = make_query(book_query9)
            exist = get_db(readbook_server_url, function_name, book_query9)[0]
            #exist = Book.query.filter_by(isbn=request.form.get('isbn')).first()
            if exist['word']=='yes':
                flash(u'The book information already exists, please check it before entering; Or fill in the store form.')
            else:
                '''
                book = Book()
                book.isbn = request.form.get('isbn')
                book.book_name = request.form.get('book_name')
                book.press = request.form.get('press')
                book.author = request.form.get('author')
                book.class_name = request.form.get('class_name')
                db.session.add(book)
                db.session.commit()
                '''
                book_add2 = ['isbn', request.form.get('isbn'),'book_name',request.form.get('book_name'),\
                             'press',request.form.get('press'),'author',request.form.get('author'),\
                             'class_name',request.form.get('class_name')]
                function_name = 'book_add2'
                book_add2 = make_query(book_add2)
                exist = get_db(readbook_server_url, function_name, book_add2)[0]
                if exist['test']==True:
                    flash(u'Add book information successfully！')
        return redirect(url_for('new_store'))
    return render_template('new-store.html', name=session.get('name'), form=form)


@app.route('/borrow', methods=['GET', 'POST'])
@login_required
def borrow():
    form = BorrowForm()
    return render_template('borrow.html', name=session.get('name'), form=form)


@app.route('/find_stu_book', methods=['GET', 'POST'])
def find_stu_book():
    book_query9 = ['card_id', request.form.get('card')]
    function_name = 'book_query9'
    book_query9 = make_query(book_query9)
    stu = get_db(student_server_url, function_name, book_query9)[0]
    #stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu['student_name']=='Not found':
        return jsonify([{'stu': 0}])  # 没找到
    if stu['debt'] is True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu['valid_date']) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu['loss'] is True:
        return jsonify([{'stu': 3}])  # 已经挂失

    booksquery = ['book_name', request.form.get('book_name')]
    function_name = 'booksquery'
    booksquery = make_query(booksquery)
    books = get_db(readbook_server_url, function_name, booksquery)
    '''
    books = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(request.form.get('book_name')),
        Inventory.status == 1).with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).\
        all()
    '''
    return books










def out():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    book_name = request.args.get('book_name')
    readbook = ReadBook()
    #readbook.id=0
    readbook.barcode = barcode
    readbook.card_id = card
    readbook.start_date = int(today_stamp)*1000
    readbook.due_date = (int(today_stamp)+40*86400)*1000
    readbook.borrow_admin = current_user.admin_id
    db.session.add(readbook)
    db.session.commit()
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = False
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(book_name), Inventory.status == 1).\
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'author': bk.author, 'press': bk.press}
        data.append(item)

    book_out = db.session.query(Book).join(Inventory).filter(Inventory.barcode.contains(barcode), Inventory.status == 0). \
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).first()

    sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAUSNPTE4A2EFMSJRO', aws_secret_access_key='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')
    response = sns_client.publish(
        TargetArn='arn:aws:sns:us-east-1:314437740289:Borrow',
        Message=('A user just borrowed the book "' + book_out.book_name + '"!'),
        Subject='Book Borrowed',
    )['MessageId']
    return jsonify(data), response



@app.route('/out', methods=['GET', 'POST'])
@login_required
def out():
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    barcode = request.args.get('barcode')
    card = request.args.get('card')
    book_name = request.args.get('book_name')


    book_out = ['barcode', barcode,'card_id',card,'start_date',int(today_stamp)*1000,'due_date',(int(today_stamp)+40*86400)*1000,\
                'borrow_admin',current_user.admin_id]
    function_name = 'book_out'
    book_out = make_query(book_out)
    the_out = get_db(readbook_server_url, function_name, book_out)

    '''
    readbook = ReadBook()
    #readbook.id=0
    readbook.barcode = barcode
    readbook.card_id = card
    readbook.start_date = int(today_stamp)*1000
    readbook.due_date = (int(today_stamp)+40*86400)*1000
    readbook.borrow_admin = current_user.admin_id
    db.session.add(readbook)
    db.session.commit()
    '''

    book_query10 = ['barcode',barcode,'book_name',book_name]
    function_name = 'book_query10'
    book_query10 = make_query(book_query10)
    book = get_db(readbook_server_url, function_name, book_query10)

    '''
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = False
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(Book).join(Inventory).filter(Book.book_name.contains(book_name), Inventory.status == 1).\
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).all()
    data = []
    for bk in bks:
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'author': bk.author, 'press': bk.press}
        data.append(item)
    return jsonify(data)
    '''

    sns_query = ['barcode', barcode]
    function_name = 'sns_query'
    sns_query = make_query(sns_query)
    book_out = get_db(readbook_server_url, function_name, sns_query)[0]
    sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAUSNPTE4A2EFMSJRO',
                              aws_secret_access_key='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')
    response = sns_client.publish(
        TargetArn='arn:aws:sns:us-east-1:314437740289:Borrow',
        Message=('A user just borrowed the book "' + book_out['book_name'] + '"!'),
        Subject='Book Borrowed',
    )['MessageId']
    return book, response

@app.route('/return', methods=['GET', 'POST'])
@login_required
def return_book():
    form = SearchStudentForm()
    return render_template('return.html', name=session.get('name'), form=form)


@app.route('/find_not_return_book', methods=['GET', 'POST'])
def find_not_return_book():

    book_query11 = ['card_id', request.form.get('card')]
    print(book_query11)
    function_name = 'book_query11'
    book_query11 = make_query(book_query11)
    print(book_query11)
    stu = get_db(student_server_url, function_name, book_query11)[0]

    #stu = Student.query.filter_by(card_id=request.form.get('card')).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    if stu['student_name']=='Not found':
        return jsonify([{'stu': 0}])  # 没找到
    if stu['debt'] == True:
        return jsonify([{'stu': 1}])  # 欠费
    if int(stu['valid_date']) < int(today_stamp)*1000:
        return jsonify([{'stu': 2}])  # 到期
    if stu['loss'] is True:
        return jsonify([{'stu': 3}])  # 已经挂失

    book_not = ['card_id', request.form.get('card')]
    function_name = 'book_not'
    book_not = make_query(book_not)
    stu = get_db(readbook_server_url, function_name, book_not)
    return stu


    '''
    books = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == request.form.get('card'),
        ReadBook.end_date.is_(None)).with_entities(ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
                                                 ReadBook.due_date).all()
    data = []
    for book in books:
        start_date = timeStamp(book.start_date)
        due_date = timeStamp(book.due_date)
        item = {'barcode': book.barcode, 'isbn': book.isbn, 'book_name': book.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)
    '''


@app.route('/in', methods=['GET', 'POST'])
@login_required
def bookin():
    barcode = request.args.get('barcode')
    card = request.args.get('card')

    book_in = ['barcode', barcode, 'card_id',card,'admin_id',current_user.admin_id]
    function_name = 'book_in'
    book_in = make_query(book_in)
    book_in_out = get_db(readbook_server_url, function_name, book_in)


    sns_query2 = ['barcode', barcode]
    function_name = 'sns_query2'
    sns_query2 = make_query(sns_query2)
    sns_in = get_db(readbook_server_url, function_name, sns_query2)[0]

    sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAUSNPTE4A2EFMSJRO',
                              aws_secret_access_key='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')
    response = sns_client.publish(
        TargetArn='arn:aws:sns:us-east-1:314437740289:Return',
        Message='A user just returned the book "' + sns_in['book_name'] + '"!',
        Subject='Book Returned',
    )['MessageId']


    return book_in_out,response

    bks = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == card,
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

    book_in = db.session.query(Book).join(Inventory).filter(Inventory.barcode.contains(barcode),
                                                            Inventory.status == 1). \
        with_entities(Inventory.barcode, Book.isbn, Book.book_name, Book.author, Book.press).first()

    sns_client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAUSNPTE4A2EFMSJRO',
                              aws_secret_access_key='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')
    response = sns_client.publish(
        TargetArn='arn:aws:sns:us-east-1:314437740289:Return',
        Message='A user just returned the book "' + book_in.book_name + '"!',
        Subject='Book Returned',
    )['MessageId']
    return jsonify(data), response






    '''
    record = ReadBook.query.filter(ReadBook.barcode == barcode, ReadBook.card_id == card, ReadBook.end_date.is_(None)).first()
    today_date = datetime.date.today()
    today_str = today_date.strftime("%Y-%m-%d")
    today_stamp = time.mktime(time.strptime(today_str + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
    record.end_date = int(today_stamp)*1000
    record.return_admin = current_user.admin_id

    
    
    
    db.session.add(record)
    db.session.commit()
    
    book = Inventory.query.filter_by(barcode=barcode).first()
    book.status = True
    db.session.add(book)
    db.session.commit()
    bks = db.session.query(ReadBook).join(Inventory).join(Book).filter(ReadBook.card_id == card,
        ReadBook.end_date.is_(None)).with_entities(ReadBook.barcode, Book.isbn, Book.book_name, ReadBook.start_date,
                                                 ReadBook.due_date).all()
    data = []
    for bk in bks:
        start_date = timeStamp(bk.start_date)
        due_date = timeStamp(bk.due_date)
        item = {'barcode': bk.barcode, 'isbn': bk.isbn, 'book_name': bk.book_name,
                'start_date': start_date, 'due_date': due_date}
        data.append(item)
    return jsonify(data)
    '''

@app.route('/library_map')
#@login_required
def library_map():

    return render_template('library_map.html')
    #return render_template('quickstart.html')



if __name__ == '__main__':
    manager.run()
