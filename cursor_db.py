import Youtube_conversion2
import os
import sqlite3
import datetime
import tkinter.messagebox as tkmsg
#changeworkdir
os.chdir('G:\マイドライブ\VS code\python(.py)\Youtube_conversion_app')

dbname='main.db'
conn=sqlite3.connect(dbname)

#背景色をHEXに変換する
def color(name):
    cur=conn.cursor()
    #cur.execute("create table color(id integer primary key autoincrement, color string)")
    cur.execute("select color from color where name = ?", (name,))
    color_code=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    cur.close()
    return color_code


#現在の背景色を保存しているdbのテーブルにアクセス
def intial_color_update(opt_color):
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=1", (opt_color,))
    conn.commit()
    cur.close()


def intial_color_select():
    cur=conn.cursor()
    cur.execute("select settings from setting where id=1")
    initial_color=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    cur.close()
    if initial_color=='赤': int_color=0
    elif initial_color=='青': int_color=1
    elif initial_color=='緑': int_color=2
    elif initial_color=='黄': int_color=3
    elif initial_color=='桃': int_color=4
    return int_color


#初期インストール先を保存しているdbのテーブルにアクセス
def intial_install_update(install_place):
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=2", (install_place,))
    conn.commit()
    cur.close()


def intial_install_select():
    cur=conn.cursor()
    cur.execute("select settings from setting where id=2")
    install_place_set=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    cur.close()
    return install_place_set


def error_path_update(error_path):
    cur=conn.cursor()
    #cur.execute("create table setting(id integer primary key, config string, settings string);")
    cur.execute("update setting set settings=? where id=3", (error_path,))
    conn.commit()
    cur.close()


def error_path_select():
    cur=conn.cursor()
    cur.execute("select settings from setting where id=3")
    error_place_set=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    cur.close()
    return error_place_set


#dbの初期化
def ini_db():
    cur=conn.cursor()
    cur.execute("")
    initial_color=str(cur.fetchall()).replace("[('","").replace("',)]","")
    conn.commit()
    cur.close()
    #色を赤にする


def history_insert(date,ext,url):
    cur=conn.cursor()
    #CREATE TABLE history(id integer primary key, date string, extension string, url string);
    cur.execute("insert into history(date,extension,url) values(?,?,?)",(date,ext,url,))
    conn.commit()
    cur.close()


def history_delete_ask():
    reset_ask=tkmsg.askokcancel("履歴の全削除","変換したURLの履歴を全部削除しますか？")
    if reset_ask==True:
        cur=conn.cursor()
        #create table history(id integer primary key, date string, url stiring)
        cur.execute("delete from history")
        conn.commit()
        cur.close()


def history_delete():
    cur=conn.cursor()
    #create table history(id integer primary key, date string, url stiring)
    cur.execute("delete from history")
    conn.commit()
    cur.close()