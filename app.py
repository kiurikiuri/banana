import os
from flask import Flask, make_response, jsonify
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import json
import pytz
import werkzeug



# ----------------------------------------
# DB CONFIG
# ----------------------------------------
# DB_USER = 'sqlsys'
# DB_PASS = 'syssql'
# HOST = 'localhost'
# DB_NAME = 'wordwork'

DB_USER = 'yztiv86wjd2ywejs'
DB_PASS = 'kigf4i6rxo4ijapl'
HOST = 'qz8si2yulh3i7gl3.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306'
DB_NAME = 'gf291wo421za8xew'
 
# ----------------------------------------
# CONST DEFINE
# ----------------------------------------
SUCCESS=1
FAILER=0
UPLOAD_DIR = "./data/loadcsv/"

# ----------------------------------------
# Application Define
# ----------------------------------------
STUDY_KIND_FORGET=1
# ----------------------------------------
# Flask settings
# ----------------------------------------
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
      'user': DB_USER,
      'password': DB_PASS,
      'host': HOST,
      'db_name': DB_NAME
  })
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
db = SQLAlchemy(app)
 
login_manager = LoginManager()
login_manager.init_app(app)

# ----------------------------------------
# SQL Define
# ----------------------------------------
SQL_STUDY_FORGET_INFO = ' \
    select \
        a.id as study_id,  \
        a.study_kind_id as study_kind_id,  \
        a.deck_id as deck_id,   \
        b.user_id as user_id,  \
        b.deck as deck, \
        c.study_kind as study_kind, \
        d.id as dwsts_id,  \
        d.last_date as last_date,   \
        d.c_num as c_num,   \
        d.ic_num as ic_num,   \
        d.check_list as check_list, \
        e.id as word_id,   \
        e.word as word,   \
        e.discription as discription, \
        g.id as study_forget_id,       \
        g.ans_num as ans_num,   \
        g.next_date as next_date,   \
        h.id as kind_id,  \
        h.kind as kind   \
    from  \
        study as a  \
    inner join  \
        decks as b  \
            on a.deck_id = b.id \
    inner join \
        studyKind as c \
            on a.study_kind_id = c.id \
    inner join  \
        dwsts as d  \
            on a.deck_id = d.deck_id \
            and b.user_id = d.user_id \
    inner join  \
        words as e  \
            on d.word_id = e.id \
            and b.user_id = e.user_id \
    inner join  \
        wdindk as f  \
            on e.id = f.word_id \
            and b.user_id = f.user_id \
            and d.deck_id = f.deck_id \
    inner join  \
        studyforget as g  \
            on f.id = g.wdindk_id \
            and g.deck_id = b.id \
    inner join  \
        kind as h  \
            on e.kind_id = h.id \
'
# ----------------------------------------
# create table class
# ----------------------------------------
#class BlogArticle(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(50), nullable=False)
#    body = db.Column(db.String(500), nullable=False)
#    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
class Words(db.Model):
    __tablename__ = 'words'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    kind_id = db.Column(db.Integer, db.ForeignKey('kind.id', onupdate='CASCADE', ondelete='CASCADE'))
    word = db.Column(db.String(500), nullable=False)
    discription = db.Column(db.String(1024), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    dwsts=db.relationship('Dwsts')
    wdindk=db.relationship('Wdindk')
class Decks(db.Model):
    __tablename__ = 'decks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    deck_kind_id = db.Column(db.Integer, db.ForeignKey('dkkind.id', onupdate='CASCADE', ondelete='CASCADE')) 
    deck = db.Column(db.String(255), nullable=False)
    shared_flg = db.Column(db.SmallInteger, default=0)
    appear_flg = db.Column(db.SmallInteger, default=1)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    dwsts=db.relationship('Dwsts')
    wdindk=db.relationship('Wdindk')
    study=db.relationship('Study')
    studyForget=db.relationship('StudyForget')
class Kind(db.Model):
    __tablename__ = 'kind'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'))
    kind = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    words=db.relationship('Words')
class Dwsts(db.Model):
    __tablename__ = 'dwsts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE')) 
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', onupdate='CASCADE', ondelete='CASCADE')) 
    word_id = db.Column(db.Integer, db.ForeignKey('words.id', onupdate='CASCADE', ondelete='CASCADE')) 
    last_date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    check_list = db.Column(db.SmallInteger, default=0)
    c_num = db.Column(db.Integer, default=0)
    ic_num = db.Column(db.Integer, default=0)
    ans_num = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
class Wdindk(db.Model):
    __tablename__ = 'wdindk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE')) 
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', onupdate='CASCADE', ondelete='CASCADE')) 
    word_id = db.Column(db.Integer, db.ForeignKey('words.id', onupdate='CASCADE', ondelete='CASCADE')) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    studyForget=db.relationship('StudyForget')
class Dkkind(db.Model):
    __tablename__ = 'dkkind'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE')) 
    deck_kind = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    decks=db.relationship('Decks')
class Study(db.Model):
    __tablename__ = 'study'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_kind_id = db.Column(db.Integer, nullable=False)
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', onupdate='CASCADE', ondelete='CASCADE')) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
class StudyKind(db.Model):
    __tablename__ = 'studyKind'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    study_kind = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
class StudyForget(db.Model):
    __tablename__ = 'studyForget'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wdindk_id = db.Column(db.Integer, db.ForeignKey('wdindk.id', onupdate='CASCADE', ondelete='CASCADE')) 
    deck_id = db.Column(db.Integer, db.ForeignKey('decks.id', onupdate='CASCADE', ondelete='CASCADE')) 
    ans_num = db.Column(db.Integer, default=0)
    next_date = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))
#----------------------------------------
# difine sql
# ----------------------------------------


#----------------------------------------
# create user table class
# ----------------------------------------
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256))
    words=db.relationship('Words')
    decks=db.relationship('Decks')
    kind=db.relationship('Kind')
    dwsts=db.relationship('Dwsts')
    wdindk=db.relationship('Wdindk')
    dkkind=db.relationship('Dkkind')

# ----------------------------------------
# login manager settings
# ----------------------------------------
@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ----------------------------------------
# signup user
# ----------------------------------------
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == "POST":
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # Userのインスタンスを作成
#         user = User(username=username, password=generate_password_hash(password, method='sha256'))
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/login')
#     else:
#         return render_template('signup.html')

# ----------------------------------------
# login
# ----------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        # Userテーブルからusernameに一致するユーザを取得
        user = User.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        return redirect('/login')
    else:
        return render_template('login.html')

# ----------------------------------------
# logout 
# ----------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# ----------------------------------------
# utility
# ----------------------------------------
# ----------------------------------------
# check
# ----------------------------------------
# check word exists
def isWordExists(user_id, kind_id, word):
    isWord = db.session.query(Words).filter(Words.user_id == user_id).filter(Words.kind_id == kind_id).filter(Words.word == word).first()
    return isWord
# check word kind exists
def isKindExists(user_id, kind):
    isKind = db.session.query(Kind).filter(Kind.user_id == user_id).filter(Kind.kind == kind).first()
    return isKind
# check deck kind exists
def isDeckKindExists(user_id, deck_kind):
    isDkkind = db.session.query(Dkkind).filter(Dkkind.user_id == user_id).filter(Dkkind.deck_kind == deck_kind).first()
    return isDkkind
# check deck exists
def isDecksExists(user_id, deck_kind_id, deck):
    isDeck = db.session.query(Decks).filter(Decks.user_id == user_id).filter(Decks.deck_kind_id == deck_kind_id).filter(Decks.deck == deck).first()
    return isDeck

# ----------------------------------------
# select all at user
# ----------------------------------------
def selectAtUserKind(user_id):
    rec = db.session.query(Kind).filter(Kind.user_id == user_id).all()
    return rec
def selectAtUserWords(user_id):
    rec = db.session.query(Words).filter(Words.user_id == user_id).all()
    return rec
def selectAtUserDeckKind(user_id):
    rec = db.session.query(Dkkind).filter(Dkkind.user_id == user_id).all()
    return rec
def selectAtUserDecks(user_id):
    rec = db.session.query(Decks).filter(Decks.user_id == user_id).all()
    return rec

   
# ----------------------------------------
# select partial search at user
# ----------------------------------------
def selectPtAtUserWords(user_id, s):
    rec = db.session.query(Words).filter(Words.user_id == user_id).filter(Words.word.like("%{}%".format(s))).all()
    return rec

# ----------------------------------------
# dynamic sql struction
# ----------------------------------------
def dynamicSqlStcWordAtUser(user_id):
    sql = db.session.query(Words).filter(Words.user_id == user_id)
    return sql
def dynamicSqlStcDeckAtUser(user_id):
    sql = db.session.query(Decks).filter(Decks.user_id == user_id)
    return sql


# ----------------------------------------
# get at key ,user
# ----------------------------------------
def getKind(id, user_id):
    rec = db.session.query(Kind).filter(Kind.id == id).filter(Kind.user_id == user_id).first()
    return rec
def getWords(id, user_id, kind_id):
    rec = db.session.query(Words).filter(Words.id == id).filter(Words.user_id == user_id).filter(Words.kind_id == kind_id).first()
    return rec
def getDeckKind(id, user_id):
    rec = db.session.query(Dkkind).filter(Dkkind.id == id).filter(Dkkind.user_id == user_id).first()
    return rec

# ----------------------------------------
# get none key
# ----------------------------------------
def getWordKind(user_id, word, kind_id):
    rec = db.session.query(Words).filter(Words.user_id == user_id).filter(Words.kind_id == kind_id).filter(Words.word == word).all()
    return rec
# =========================================
# delete
# =========================================
# ----------------------------------------
# delete keys
# ----------------------------------------
def deleteWordsAtKeys(user_id, word_id, kind_id):
    print(user_id)
    print(word_id)
    print(kind_id)
    words = db.session.query(Words).filter(Words.user_id == user_id).filter(Words.kind_id == kind_id).filter(Words.id == word_id).first()
    print(words)
    db.session.delete(words)
    db.session.commit()
    return 1

# ----------------------------------------
# delete keys object
# ----------------------------------------
def deleteWordsAtKeysObjct(keysObj):
    print(keysObj)
    ret = deleteWordsAtKeys(keysObj['user_id'], keysObj['id'], keysObj['kind_id'])
    return ret

# ----------------------------------------
# delete keys object list
# ----------------------------------------
def deleteWordsAtKeysObjctList(keysObjList):
    print(keysObjList)
    for o in keysObjList:
        deleteWordsAtKeysObjct(o)
    return 1

# ----------------------------------------
# delete keys object list
# ----------------------------------------
def deleteWordsAtIdList(idList):
    for i in idList:
        words = Words.query.get(i)
        db.session.delete(words)
        db.session.commit()
    return 1

def deleteDecksAtIdList(idList):
    for i in idList:
        decks = Decks.query.get(i)
        Study.query.filter(Study.deck_id==i).delete()
        StudyForget.query.filter(StudyForget.deck_id==i).delete()
        Dwsts.query.filter(Dwsts.deck_id==i).delete()
        Wdindk.query.filter(Wdindk.deck_id==i).delete()
        db.session.delete(decks)
        db.session.commit()
    return 1
def getNextDateForStudyForget(d, num):
    now = datetime.now()#.strftime('%Y/%m/%d 00:00:00')
    if num == 1:
        print(1)
        nextDate = now + timedelta(days=1)
    elif num == 2:
        print(2)
        nextDate = now + timedelta(days=7)
    elif num == 3:
        print(3)
        nextDate = now + timedelta(days=20)
    elif num == 4:
        print(4)
        nextDate = now + timedelta(days=35)
    else:
        print(6)
    return nextDate

# ----------------------------------------
# components
# ----------------------------------------
def addWord(word, discription, kind_id):
    isWord = isWordExists(current_user.id, kind_id, word)
    if isWord is None:
        # kindのインスタンスを作成
        newWord = Words(word=word, discription=discription, kind_id=kind_id, user_id=current_user.id)
        db.session.add(newWord)
        db.session.commit()
        msg="word is created.[word='{}']".format(word)
        print(msg)
        rslt = { 'msg': msg, 'result': SUCCESS, 'code': 1, 'rec': newWord }
    else:
        msg="The word is already exists.[word='{}']".format(word)
        print(msg)
        rslt = { 'msg': msg, 'result': FAILER, 'code': 0, 'rec': None}
    rtn = { 'addWord': rslt }
    return rtn
def addDeck(deck, deck_kind_id):
    try:
        isDeck = isDecksExists(current_user.id, deck_kind_id, deck)
        if isDeck is None:
            newDeck = Decks(user_id=current_user.id, deck_kind_id=deck_kind_id, deck=deck)
            db.session.add(newDeck)
            db.session.commit()
            msg="新しいデックの作成に成功しました。[deck={}]".format(deck)
            print(msg)
            rslt = { 'msg': msg, 'result': SUCCESS, 'code': 1}
        else:
            msg="すでに登録されているデック名とデック種別の組み合わせです。[deck={}]".format(deck)
            print(msg)
            rslt = { 'msg': msg, 'result': FAILER, 'code': 0}
        rtn = { 'addDeck': rslt }
        return rtn
    except:
        msg="DBアクセスエラー。[deck={}]".format(deck)
        print(msg)
        rslt = { 'msg': msg, 'result': FAILER, 'code': -1}
        rtn = { 'addDeck': rslt }
        return rtn
def addWordInDeck(deckRecord, wordIdList):
    try:
        print(wordIdList)
        for li in wordIdList:
            print(1)
            newWdindk = Wdindk(user_id=current_user.id, deck_id=deckRecord.id, word_id=int(li))
            db.session.add(newWdindk)
        for li in wordIdList:
            print(2)
            newDwsts = Dwsts(user_id=current_user.id, deck_id=deckRecord.id, word_id=int(li))
            db.session.add(newDwsts)
        db.session.commit()
        msg="デックにワードを追加しました。[deck={}]".format(deckRecord.deck)
        print(msg)
        rslt = { 'msg': msg, 'result': SUCCESS, 'code': 1}
        rtn = { 'addWordInDeck': rslt }

        return rtn
    except:
        msg="DBアクセスエラー。[deck={}]".format(deckRecord.deck)
        print(msg)
        rtn = { 'msg': msg, 'result': FAILER, 'code': -1}
        return rtn
def createStudy(deck_id):
    try:
        print(1)
        newStudy = Study(study_kind_id=STUDY_KIND_FORGET, deck_id=deck_id)
        db.session.add(newStudy)
        wdindkList = Wdindk.query.filter(Wdindk.deck_id==deck_id).all()
        for li in wdindkList:
            newStudyForget = StudyForget(wdindk_id=li.id, deck_id=deck_id)
            db.session.add(newStudyForget)
        db.session.commit()
        msg="STUDYの初期作成に成功しました。"
        rtn = { 'msg': msg, 'result': SUCCESS, 'code': 1}
    except:
        msg="DBアクセスエラー。"
        rtn = { 'msg': msg, 'result': FAILER, 'code': -1}
    return rtn
def addStudy(deck_id, word_id):
    try:
        print("addstudy")
        print(deck_id)
        print(word_id)
        es = Study.query.filter(Study.deck_id == deck_id).filter(Study.study_kind_id == STUDY_KIND_FORGET)
        if db.session.query(es.exists()).scalar():
            print("scalar")
            # newStudy = Study(study_kind_id=STUDY_KIND_FORGET, deck_id=deck_id)
            # db.session.add(newStudy)
            wdindk = Wdindk.query.filter(Wdindk.deck_id==deck_id).filter(Wdindk.word_id==word_id).first()
            newStudyForget = StudyForget(wdindk_id=wdindk.id, deck_id=deck_id)
            db.session.add(newStudyForget)
            db.session.commit()
            msg="STUDYの追加に成功しました。"
            rtn = { 'msg': msg, 'result': SUCCESS, 'code': 1, 'rec': newStudyForget}
        else:
            msg="STUDYが存在しません。"
            rtn = { 'msg': msg, 'result': FAILER, 'code': -2, 'rec': None}
        return rtn
    except:
        msg="DBアクセスエラー。"
        rtn = { 'msg': msg, 'result': FAILER, 'code': -1, 'rec': None}
        
    
# ----------------------------------------
# root page route
# ----------------------------------------
@app.route('/', methods=['GET'])
@login_required
def index():
    print(current_user.id)
    return render_template('index.html' )

@app.route('/load-csv')
@login_required
def load_csv():
   return render_template('load_csv.html' )

# ----------------------------------------
# select data template
# ----------------------------------------
# @app.route('/', methods=['GET'])
# @login_required
#def blog():
#    if request.method == 'GET':
#        # DBに登録されたデータをすべて取得する
#        blogarticles = BlogArticle.query.all()
#    return render_template('index.html', blogarticles=blogarticles)

@app.route('/kind-list', methods=['GET'])
@login_required
def kind_list():
   # DBに登録されたデータをすべて取得する
   kindList = selectAtUserKind(current_user.id)
   return render_template('kind_list.html', kindList=kindList)

@app.route('/deck-kind-list', methods=['GET'])
@login_required
def deck_kind_list():
   # DBに登録されたデータをすべて取得する
   deckKindList = selectAtUserDeckKind(current_user.id)
   return render_template('deck_kind_list.html', deckKindList=deckKindList)

@app.route('/word-list', methods=['GET', 'POST'])
@login_required
def word_list():
    wordList = selectAtUserWords(current_user.id)
    kindList = selectAtUserKind(current_user.id)
    if request.method == 'POST':
        if not request.form.get('deleteItems') == "":
            arr = request.form.get('deleteItems').split(',')
            ret = deleteWordsAtIdList(arr)
            wordList = selectAtUserWords(current_user.id)
        else:
            sql = dynamicSqlStcWordAtUser(current_user.id)
            if not request.form.get('searchword') is None:
                sql = sql.filter(Words.word.like("%{}%".format(request.form.get('searchword'))))
            if not request.form.get('kind_id') is None:
                sql = sql.filter(Words.kind_id == request.form.get('kind_id'))
            wordList = sql.all()
    return render_template('word_list.html', wordList=wordList, kindList=kindList)

@app.route('/deck-list', methods=['GET', 'POST'])
@login_required
def deck_list():
    deckList = selectAtUserDecks(current_user.id)
    deckKindList = selectAtUserDeckKind(current_user.id)
    if request.method == 'POST':
        if not request.form.get('deleteItems') == "":
            arr = request.form.get('deleteItems').split(',')
            ret = deleteDecksAtIdList(arr)
            deckKindList = selectAtUserDeckKind(current_user.id)
            deckList = selectAtUserDecks(current_user.id)
        else:
            sql = dynamicSqlStcDeckAtUser(current_user.id)
            if not request.form.get('searchdeck') is None:
                sql = sql.filter(Decks.deck.like("%{}%".format(request.form.get('searchdeck'))))
            if not request.form.get('deck_kind_id') is None:
                sql = sql.filter(Decks.deck_kind_id == request.form.get('deck_kind_id'))
            deckList = sql.all()
    return render_template('deck_list.html', deckList=deckList, deckKindList=deckKindList)

@app.route('/study-list/<int:id>', methods=['GET', 'POST'])
@login_required
def study_list(id):
    sql = SQL_STUDY_FORGET_INFO + ' \
            where  b.user_id = {} \
            and    a.deck_id = {} \
            order by g.next_date asc \
            ;'.format(current_user.id, id)
    t = db.text(sql)
    deckInfoList = db.session.execute(t).all()
    if request.method == 'POST':
        print(1)
    return render_template('study_word_list.html', deckInfoList = deckInfoList)

@app.route('/study-deck/<int:id>', methods=['GET', 'POST'])
@login_required
def study_deck(id):
    msg="initialize"
    studyKind=Study.query.filter(Study.deck_id == id).first()
    if request.method == "POST":
        print(1)
        # dwsts recode
        dwsts = Dwsts.query.get(request.form.get('dwsts_id'))
        if request.form.get('actionflg') == 'correct':
            print(2)
            dwsts.c_num = int(dwsts.c_num) + 1
        elif request.form.get('actionflg') == 'incorrect':
            print(3)
            dwsts.ic_num = int(dwsts.ic_num) + 1
        dwsts.ans_num = int(dwsts.ans_num) + 1
        print(4)
        dwsts.check_list = request.form.get('chkComprehension')
        # studyForget recode
        studyForget = StudyForget.query.get(request.form.get('study_forget_id'))
        studyForget.ans_num = int(studyForget.ans_num) + 1
        studyForget.next_date = getNextDateForStudyForget(studyForget.next_date, studyForget.ans_num)

        # commit update
        db.session.commit()
        
        # select new recode
        now = datetime.now()
        tommorow = now + timedelta(days=1)
        tommorowStr = tommorow.strftime('%Y/%m/%d 00:00:00')
        sql = SQL_STUDY_FORGET_INFO + ' \
                where  b.user_id = {} \
                and    a.deck_id = {} \
                and    g.next_date < "{}" \
                order by g.next_date asc \
                ;'.format(current_user.id, id, tommorowStr)
        t = db.text(sql)
        deckInfo = db.session.execute(t).first()
    else:
        if int(studyKind.study_kind_id) == STUDY_KIND_FORGET:
            now = datetime.now()
            tommorow = now + timedelta(days=1)
            tommorowStr = tommorow.strftime('%Y/%m/%d 00:00:00')
            sql = SQL_STUDY_FORGET_INFO + ' \
                    where  b.user_id = {} \
                    and    a.deck_id = {} \
                    and    g.next_date < "{}" \
                    order by g.next_date asc \
                    ;'.format(current_user.id, id, tommorowStr)
            t = db.text(sql)
            deckInfo = db.session.execute(t).first()
    return render_template('study_deck.html', msg=msg, deckInfo=deckInfo )
# ----------------------------------------
# update data template
# ----------------------------------------
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# @login_required
# def update(id):
#     # 引数idに一致するデータを取得する
#     blogarticle = BlogArticle.query.get(id)
#     if request.method == "GET":
#         return render_template('update.html', blogarticle=blogarticle)
#     else:
#         # 上でインスタンス化したblogarticleのプロパティを更新する
#         blogarticle.title = request.form.get('title')
#         blogarticle.body = request.form.get('body')
#         # 更新する場合は、add()は不要でcommit()だけでよい
#         db.session.commit()
#         return redirect('/') 
@app.route('/edit-kind/update/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_kind_update(id):
    # 引数id ログイン中ユーザIDに一致するデータを取得する
    msg="initialize"
    kind = Kind.query.get(id)
    if request.method == "POST":
        # 入力されたkindをチェック
        isKind = isKindExists(current_user.id, request.form.get('kind'))
        if isKind is None:
            # 上でインスタンス化したkindのプロパティを更新する
            kind.kind = request.form.get('kind')
            # 更新する場合は、add()は不要でcommit()だけでよい
            db.session.commit()
            kind = Kind.query.get(id)
            msg="更新に成功しました。[kind={}]".format(kind.kind)
        else:
            msg="更新に失敗しました。すでに登録されているワード種別です。[kind={}]".format(kind.kind)
    return render_template('edit_kind.html', kind=kind, msg=msg) 

@app.route('/edit-deck-kind/update/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_deck_kind_update(id):
    # 引数id ログイン中ユーザIDに一致するデータを取得する
    msg="initialize"
    deckKind = Dkkind.query.get(id)
    if request.method == "POST":
        # 入力されたdeckKindをチェック
        isDeckKind = isDeckKindExists(current_user.id, request.form.get('deckKind'))
        if isDeckKind is None:
            # 上でインスタンス化したkindのプロパティを更新する
            deckKind.deck_kind = request.form.get('deckKind')
            # 更新する場合は、add()は不要でcommit()だけでよい
            db.session.commit()
            deckKind = Dkkind.query.get(id)
            msg="更新に成功しました。[deckKind={}]".format(deckKind.deck_kind)
        else:
            msg="更新に失敗しました。すでに登録されているデック種別です。[deckKind={}]".format(deckKind.deck_kind)
    return render_template('edit_deck_kind.html', deckKind=deckKind, msg=msg) 

@app.route('/edit-word/update/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_word_update(id):
    # 引数idに一致するデータを取得する
    msg="initialize"
    word = Words.query.get(id)
    kindList = selectAtUserKind(current_user.id)
    if request.method == "POST":
        isWord = isWordExists(current_user.id, request.form.get('kind_id'), request.form.get('word'))
        if isWord is None:
            # 上でインスタンス化したwordのプロパティを更新する
            word.word = request.form.get('word')
            word.discription = request.form.get('discription')
            word.kind_id = request.form.get('kind_id')
            # 更新する場合は、add()は不要でcommit()だけでよい
            db.session.commit()
            msg="更新に成功しました。[word={}]".format(word.word)
            return redirect('/word-list')
        else:
            if word.word != request.form.get('word'):
                msg="更新に失敗しました。すでに登録されているワードです。[word={}]".format(word.word)
            elif word.kind_id != request.form.get('kind_id'):
                isWordKind = getWordKind(current_user.id, word.word, request.form.get('kind_id'))
                if not isWordKind is None:
                    msg="更新に失敗しました。すでに登録されているワードです。[word={}]".format(word.word)
    return render_template('edit_word.html', msg=msg, word=word, kindList=kindList)

# ----------------------------------------
# delete data template
# ----------------------------------------
# @app.route('/delete/<int:id>', methods=['GET'])
# @login_required
# def delete(id):
#     # 引数idに一致するデータを取得する
#     blogarticle = BlogArticle.query.get(id)
#     db.session.delete(blogarticle)
#     db.session.commit()
#     return redirect('/')

# ----------------------------------------
# create data template
# ----------------------------------------
# @app.route('/create', methods=['GET', 'POST'])
# @login_required
# def create():
#     if request.method == "POST":
#         title = request.form.get('title')
#         body = request.form.get('body')
#         # BlogArticleのインスタンスを作成
#         blogarticle = BlogArticle(title=title, body=body)
#         db.session.add(blogarticle)
#         db.session.commit()
#         return redirect('/')
#     else:
#         return render_template('create.html')
@app.route('/create-kind', methods=['GET', 'POST'])
@login_required
def create_kind():
    msg="initialize"
    if request.method == "POST":
        kind = request.form.get('kind')
        isKind = isKindExists(current_user.id, kind)
        # kindのインスタンスを作成
        if  isKind is None:
            newkind = Kind(kind=kind, user_id=current_user.id)
            db.session.add(newkind)
            db.session.commit()
            msg="登録に成功しました。[kind={}]".format(kind)
        else:
            msg="登録に失敗しました。次のワード種別はすでに登録されています。[kind={}]".format(kind)
    return render_template('create_kind.html', msg=msg)


@app.route('/create-word', methods=['GET', 'POST'])
@login_required
def create_word():
    msg="initialize"
    kindList = selectAtUserKind(current_user.id)
    if request.method == "POST":
        word = request.form.get('word')
        disc = request.form.get('discription')
        kind_id = request.form.get('kind_id')
        result = addWord(word, disc, kind_id)
        msg = result['addWord']['msg']
    return render_template('create_word.html', msg=msg, kindList=kindList)

@app.route('/create-deck-kind', methods=['GET', 'POST'])
@login_required
def create_deck_kind():
    msg="initialize"
    if request.method == "POST":
        deck_kind = request.form.get('deck_kind')
        isDeckKind = isDeckKindExists(current_user.id, deck_kind)
        if isDeckKind is None:
            # kindのインスタンスを作成
            newDeckKind = Dkkind(user_id=current_user.id, deck_kind=deck_kind)
            db.session.add(newDeckKind)
            db.session.commit()
            msg="deck kind is created."
        else:
            msg="The Deck kind is already exists.[deck_kind='{}']".format(deck_kind)
    return render_template('create_deck_kind.html', msg=msg)

@app.route('/create-deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    msg="initialize"
    kindList = selectAtUserKind(current_user.id)
    wordList = selectAtUserWords(current_user.id)
    deckKindList = selectAtUserDeckKind(current_user.id)
    # DBに登録されたデータをすべて取得する
    if request.method == "POST":
        if request.form.get('actionflg') == "add":
            wordIdList = request.form.get('addItems').split(',')
            deck_kind_id = request.form.get('deck_kind_id')
            deck = request.form.get('deckname')
            createDeckResult = addDeck(deck, deck_kind_id)
            if createDeckResult['addDeck']['result'] == 1:
                newDeck = db.session.query(Decks).filter(Decks.user_id==current_user.id, Decks.deck_kind_id==deck_kind_id, Decks.deck==deck).first()
                addWordInDeckResult = addWordInDeck(newDeck, wordIdList)
                createStudy(newDeck.id)
                msg=addWordInDeckResult['addWordInDeck']['msg']
            else:
                msg=createDeckResult['addDeck']['msg']
        else:
            sql = dynamicSqlStcWordAtUser(current_user.id)
            if not request.form.get('searchword') is None:
                sql = sql.filter(Words.word.like("%{}%".format(request.form.get('searchword'))))
            if not request.form.get('kind_id') is None:
                sql = sql.filter(Words.kind_id == request.form.get('kind_id'))
            wordList = sql.all()
    return render_template('create_deck.html', msg=msg, wordList=wordList, kindList=kindList, deckKindList=deckKindList)

def addWordToDeck(deck_id, word, discription, kind_id):
    try:
        print("addWordTodeck")
        print(deck_id)
        print(word)
        print(discription)
        print(kind_id)
        rtn = {}
        print(1111)
        addWordRslt = addWord(word, discription, kind_id)
        print(1113)
        deckRecord = Decks.query.get(deck_id)
        print(1111)
        print(addWordRslt['addWord'])
        print(addWordRslt['addWord']['result'])
        if addWordRslt['addWord']['result'] == FAILER:
            print('add exist word to deck')
            newWord = Words.query.filter(Words.user_id == current_user.id).filter(Words.word == word).filter(Words.kind_id == kind_id).first()
            addWordRslt['addWord']['rec'] = newWord
        else:
            print('add new word to deck')
            newWord = addWordRslt['addWord']['rec']
        print(newWord)
        rtn['calls'] = addWordRslt
        # デックに新規追加ワードが登録されているか確認する
        if Wdindk.query.filter(Wdindk.deck_id == deck_id).filter(Wdindk.word_id == newWord.id).first() == None:
            print("aaafdasfa")
            addWordInDeckRslt = addWordInDeck(deckRecord, [newWord.id])
            print("1aaafdasfa")
            rtn['addWordInDeck'] = addWordInDeckRslt
            print("2aaafdasfa")
            msg="デックに新しく単語を追加[word_id={}]".format(newWord.id)
            print(2)
            print(msg)
            rslt = { 'msg': msg, 'result': SUCCESS, 'code': 1}
        else:
            msg="デックにこの単語は登録されているので何も登録しない[word_id={}]".format(newWord.id)
            print(1)
            print(msg)
            rslt = { 'msg': msg, 'result': SUCCESS, 'code': 2}
        rtn['addWordToDeck'] = rslt
        for rs in rtn:
            print(rs)
        return rtn
    except Exception as e:
        print(e)
        msg="DBアクセスエラー。"
        rtn = { 'msg': msg, 'result': FAILER, 'code': -1}
        print(msg)
        return rtn
@app.route('/add-word-to-deck/<int:deck_id>/<int:word_id>', methods=['GET', 'POST'])
@login_required
def add_word_to_deck(deck_id, word_id):
   # DBに登録されたデータをすべて取得する
   deck = Decks.query.get(deck_id)
   deckKind = Dkkind.query.filter(Dkkind.id == deck.deck_kind_id).first()
   word = Words.query.get(word_id)
   kind = Kind.query.get(word.kind_id)
   msg='initialize'
   rtn = {}
   if request.method == 'POST':
       deck_id = deck_id
       word = request.form.get('word')
       discription = request.form.get('discription')
       kind_id = request.form.get('kind_id')
       addWordToDeckRslt = addWordToDeck(deck_id, word, discription, kind_id)
       rtn['addWordToDeckRslt'] = addWordToDeckRslt
       if addWordToDeckRslt['addWordToDeck']['code'] == 1:
           addStudy(deck_id, addWordToDeckRslt['calls']['addWord']['rec'].id)
        
   return render_template('add_word_to_deck.html', msg=msg, deck=deck, deckKind=deckKind, kind=kind)
@app.route('/study-config/<int:id>', methods=['GET', 'POST'])
@login_required
def study_config(id):
   # DBに登録されたデータをすべて取得する
   studyKindList = StudyKind.query.all()
   msg='initialize'
   if request.method == 'POST':
        study = Study.query.filter(Study.deck_id == id).first()
        study.study_kind_id = request.form.get('study_kind')
        db.session.commit()
        if int(request.form.get('study_kind')) == STUDY_KIND_FORGET:
            es = StudyForget.query.filter(StudyForget.deck_id == id)
            if db.session.query(es.exists()).scalar():
                studyForgetList = StudyForget.query.filter(StudyForget.deck_id == id).all()
                for li in studyForgetList:
                    db.session.delete(li)
                db.session.commit()
            wdindkList = Wdindk.query.filter(Wdindk.deck_id==id).all()
            for li in wdindkList:
                newStudyForget = StudyForget(wdindk_id=li.id, deck_id=id)
                db.session.add(newStudyForget)
            msg="STUDY方法の更新に成功しました。"
            db.session.commit()
   return render_template('study_config.html', msg=msg, studyKindList=studyKindList)

@app.route('/create-deck-at-csv-post', methods=['GET', 'POST'])
@login_required
def create_deck_at_csv_post():
    rtnjson = { "result": "failure", "code": "-1" }
    if request.method == 'POST':
        try:
            req = request.get_json()
            for rec in req:
                deck        = rec["deck"]
                deck_kind   = rec["deck_kind"]
                # study_kind  = rec["study_kind"]
                word        = rec["word"]
                kind        = rec["word_kind"]
                discription = rec["discription"]
                print(deck       )
                print(deck_kind  )
                # print(study_kind )
                print(word       )
                print(kind       )
                print(discription)

                #deck_kindが登録されているかを確認
                sql = Dkkind.query.filter(Dkkind.user_id == current_user.id).filter(Dkkind.deck_kind == deck_kind)
                if not db.session.query(sql.exists()).scalar():
                    print(1)
                    # 登録されていなかったので登録
                    newDkkind = Dkkind(user_id=current_user.id, deck_kind=deck_kind)
                    db.session.add(newDkkind)
                    db.session.flush()
                    deck_kind_id = newDkkind.id
                else:
                    print(2)
                    deck_kind_id = sql.first().id

                #kindが登録されているかを確認
                sql = Kind.query.filter(Kind.user_id == current_user.id).filter(Kind.kind == kind)
                print(3)
                if not db.session.query(sql.exists()).scalar():
                    print(4)
                    # 登録されていなかったので登録
                    newkind = Kind(user_id=current_user.id, kind=kind)
                    db.session.add(newkind)
                    db.session.flush()
                    kind_id = newkind.id
                else:
                    print(5)
                    kind_id = sql.first().id

                #wordとkindの組み合わせが登録されているかを確認
                sql = Words.query.filter(Words.user_id == current_user.id).filter(Words.word == word).filter(Words.kind_id == kind_id)
                print(33)
                if not db.session.query(sql.exists()).scalar():
                    print(1114)
                    # 登録されていなかったので登録
                    newWord = Words(user_id=current_user.id, word=word, discription=discription, kind_id=kind_id)
                    db.session.add(newWord)
                    db.session.flush()
                    word_id = newWord.id
                else:
                    print(5)
                    word_id = sql.first().id

                # deckとdeck_kindの組み合わせが登録されているか確認
                sql = Decks.query.filter(Decks.user_id == current_user.id).filter(Decks.deck == deck).filter(Decks.deck_kind_id == deck_kind_id)
                if not db.session.query(sql.exists()).scalar():
                    print(44)
                    # 登録されていなかったので登録
                    newDeck = Decks(user_id=current_user.id, deck_kind_id=deck_kind_id, deck=deck)
                    db.session.add(newDeck)
                    db.session.flush()
                    deck_id = newDeck.id
                else:
                    # 登録されているので登録済みのdeck_idを設定
                    print(55)
                    deck_id = sql.first().id

                # wdindkが登録されているか確認
                sql = Wdindk.query.filter(Wdindk.user_id == current_user.id).filter(Wdindk.deck_id == deck_id).filter(Wdindk.word_id == word_id)
                if not db.session.query(sql.exists()).scalar():
                    print(451)
                    # 登録されていなかったので登録
                    newWdindk = Wdindk(user_id=current_user.id, deck_id=deck_id, word_id=word_id)
                    db.session.add(newWdindk)
                    db.session.flush()
                    wdindk_id = newWdindk.id
                else:
                    # 登録されているので登録済みのdeck_idを設定
                    print(56)
                    wdindk_id = sql.first().id

                # dwstsが登録されているか確認
                sql = Dwsts.query.filter(Dwsts.user_id == current_user.id).filter(Dwsts.deck_id == deck_id).filter(Dwsts.word_id == word_id)
                if not db.session.query(sql.exists()).scalar():
                    print(452)
                    # 登録されていなかったので登録
                    newDwsts = Dwsts(user_id=current_user.id, deck_id=deck_id, word_id=word_id)
                    db.session.add(newDwsts)
                    db.session.flush()
                    dwsts_id = newDwsts.id
                else:
                    # 登録されているので登録済みのdeck_idを設定
                    print(5611)
                    dwsts_id = sql.first().id

                # studyとdeck_idの組み合わせが登録されているか確認
                sql = Study.query.filter(Study.deck_id == deck_id)
                if not db.session.query(sql.exists()).scalar():
                    print(45)
                    # 登録されていなかったので登録
                    newStudy = Study(study_kind_id=1, deck_id=deck_id)
                    db.session.add(newStudy)
                    db.session.flush()
                    study_id = newStudy.id
                else:
                    # 登録されているので登録済みのdeck_idを設定
                    print(56)
                    study_id = sql.first().id
                
                # studyForgetとdeck_idの組み合わせが登録されているか確認
                sql = StudyForget.query.filter(StudyForget.deck_id == deck_id).filter(StudyForget.wdindk_id == wdindk_id)
                if not db.session.query(sql.exists()).scalar():
                    print(4116)
                    # 登録されていなかったので登録
                    newStudyForget = StudyForget(wdindk_id=wdindk_id, deck_id=deck_id, ans_num=0)
                    db.session.add(newStudyForget)
                    db.session.flush()
                    study_id = newStudyForget.id
                else:
                    # 登録されているので登録済みのdeck_idを設定
                    print(57)
                    study_id = sql.first().id
                print(6)
            db.session.commit()
            rtnjson = { "result": "success", "code": "1" }
        except Exception as e:
            print(e)
            db.session.rollback()
            rtnjson = { "result": "failure", "code": "-1" }
        finally:
            return jsonify(rtnjson)

@app.route('/create-deck-at-csv', methods=['GET', 'POST'])
@login_required
def create_deck_at_csv():
    # DBに登録されたデータをすべて取得する
    msg='initialize'
    if request.method == 'POST':
        print(1)
        # req = request.get_json()
        # for li in request.json:
        #     li.get("deck")

    return render_template('create_deck_at_csv.html', msg=msg)
