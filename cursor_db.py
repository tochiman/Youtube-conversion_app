import Youtube_conversion2
import os
import sqlite3
#changeworkdir
os.chdir('G:\マイドライブ\VS code\python(.py)\Youtube_conversion_app')


#背景色をHEXに変換する
def color(name):
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    #cur.execute("create table color(id integer primary key autoincrement, color string)")
    cur.execute("select color from color where name = ?", (name,))
    color_code=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    conn.close()
    return color_code


#現在の背景色を保存しているdbのテーブルにアクセス
def intial_color_update(opt_color):
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=1", (opt_color,))
    conn.commit()
    conn.close()


def intial_color_select():
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("select settings from setting where id=1")
    initial_color=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    conn.close()
    if initial_color=='赤': int_color=0
    elif initial_color=='青': int_color=1
    elif initial_color=='緑': int_color=2
    elif initial_color=='黄': int_color=3
    elif initial_color=='桃': int_color=4
    return int_color


#初期インストール先を保存しているdbのテーブルにアクセス
def intial_install_update(install_place):
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=2", (install_place,))
    conn.commit()
    conn.close()


def intial_install_select():
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("select settings from setting where id=2")
    install_place_set=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    conn.close()
    return install_place_set


def error_path_update(error_path):
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=3", (error_path,))
    conn.commit()
    conn.close()


def error_path_select():
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("select settings from setting where id=3")
    error_place_set=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    conn.close()
    return error_place_set


#dbの初期化
def ini_db():
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("")
    initial_color=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    conn.close()
    #色を赤にする