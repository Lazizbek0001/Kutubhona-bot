import sqlite3
from config import admin, API_TOKEN
import requests

conn = sqlite3.connect("data_base.db")

cur = conn.cursor()



class kutubhona:
    def __init__(self):
        self.conn = conn
        self.cur = cur
    
    
    def create_category_table(self):
        cur.execute("""create table if not exists category(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar(50)
        )""")
        conn.commit()
        
        
        
    def create_users_table(self):
        cur.execute("""create table if not exists users(
        id INTEGER PRIMARY KEY,
        username text
        )""")
        conn.commit()
        
        
        
    def create_books_table(self):
        self.cur.execute("""create table if not exists books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id int,
        name varchar(150),
        author varchar(150),
        photo_id text,
        file_id text,
        comment text
        )""")
        conn.commit()
        
    def select_user(self,telegram_id):
        self.cur.execute("""select * from users where id = {}""".format(telegram_id))
        user = self.cur.fetchone()
        return user
        
        
        
    def insert_category1(self,name):
        self.cur.execute("""insert into category(name) values('{}')""".format(name))
        self.conn.commit()
    
    def add_user(self,user_id, username):
        self.user = self.select_user(user_id)
        if self.user is None:
            self.cur.execute("insert into users values('{}', '{}')".format(user_id, username))
            self.conn.commit()
            text = f"""Bazaga qoshildi
ID : {user_id}
Username: @{username}"""
            self.response = requests.post(
            url='https://api.telegram.org/bot{}/sendMessage'.format(API_TOKEN),
            data={'chat_id': admin, 'text': text}
            ).json()
        else:
            return False
   
   
    def insert_books(self,category_id,name,author ,photo_id,file_id,comment):
        self.cur.execute("""insert into books(category_id,name,author,photo_id,file_id,comment) values(
            {},
            '{}',
            '{}',
            '{}',
            '{}',
            '{}'
            )""".format(category_id,name,author ,photo_id,file_id,comment))
        self.conn.commit()     
        
    def select_category(self):
        self.cur.execute("select * from category")
        return self.cur.fetchall()
    def select_category_name(self, name):
        self.cur.execute("select id from category where name = '{}' ".format(name))
        return self.cur.fetchone()   
    

    
    def select_category_id(self,id):
        self.cur.execute("select * from books where category_id = {}".format(id))
        book= self.cur.fetchall()
        return book
    def select_book_by_id(self, id):
        self.cur.execute("select * from books where id = {}".format(id))
        return self.cur.fetchone()
    
    
    def insert_category(self, category, name, auther, photo_id, file_id, comment):
        self.cur.execute("""insert into books(category_id, name, auther, photo_id, file_id, comment) values(
            {},
            '{}',
            '{}',
            '{}',
            '{}',
            '{}'
            )""".format(category, name, auther, photo_id, file_id, comment))
        self.conn.commit()
    
    
    def delete_book(self,name):
        self.cur.execute("delete from books where name = '{}' ".format(name))
        self.conn.commit()
    
    
    
    def search_book(self, text):
        self.cur.execute("""select * from books where name like "%{}%" """.format(text))
        books = self.cur.fetchall()
        return books
    
    
    
    def delete_category(self, name):
        
        self.cur.execute("select id from category where name = '{}' ".format(name))
        del_id = self.cur.fetchone()
    
        self.cur.execute("""delete from category where name = "{}" """.format(name))
        self.cur.execute("""delete from books where category_id = {}""".format(del_id[0]))
        self.conn.commit()
        
    def update_books(self, name, update,old):
        self.cur.execute("""update books set {} = '{}' where name = '{}' """.format(old,update,name))
        self.conn.commit()
        
    def select_book(self, name):
        self.cur.execute("select * from books where name = '{}' ".format(name))
        return self.cur.fetchone()
    
    def select_all_user(self):
        self.cur.execute("""select * from users""")
        user = self.cur.fetchall()
        return user