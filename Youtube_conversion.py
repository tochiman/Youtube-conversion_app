#-*- coding: utf8 -*-

import tkinter as tk
import tkinter.ttk as ttk

import tkinter.messagebox as tkmsg
import youtube_dl
import os
import sys
import tkinter.filedialog as fidi
from tkinter import *
import random


#色の設定
color = '#FFC0CB'

#アプリケーション終了処理
def shutdown():
    stdw_log = tkmsg.askyesno('通知','アプリケーションを終了します。')
    if stdw_log == False:
        pass
    else:
        exit()

def URL_delete():
    URL_Entry.delete(0,tk.END)

#ヘルプページ
def help_page():

    help_root = tk.Toplevel()
    help_root.title('ヘルプページ')
    help_root.geometry("500x200+750+350")
    help_root.configure(bg=color)
    help_root.option_add('*font',['メイリオ',10])
    hese = "1.ダウンロードしたいYouTubeのURLを入れてください。\n"\
        "\n"\
        "2.どこのフォルダに保存するかを指定してください。\n"\
        "\n"\
        "3.mp3かmp4かのどちらかファイル形式を選択してください。\n"\
        "（初期設定はmp3が選択されています。）\n"\
        "\n"\
        "4.「変換する」をクリック。"
    help_sentens = tk.Label(help_root,text=hese,font=('','12'),bg=color)
    help_sentens.pack(padx=40,pady=30)

#アップデート情報ページ
def details_page():
    details_root = tk.Toplevel()
    details_root.title('アップデート情報')
    details_root.geometry("440x220+750+250")
    details_root.configure(bg=color)
    details_root.option_add('*font',['メイリオ',10])

    dese = '～アップデート情報～\n'\
        '\n'\
        '1.1verにて...\n'\
        '・ダウンロード先のディレクトリを指定できるようになりました。\n'\
        '・このアップデート情報のウィンドウを開設しました。\n'\
        '\n'\
        '2.0verにて...\n'\
        '・mp3かmp4で保存するかを選択できるようになりました。\n'\
        '・アイコンを設定しました。\n'

    details_sentens = tk.Label(details_root,text=dese,font=('','12'),bg=color)
    details_sentens.pack(padx=15,pady=30)

#実行処理
def Run():
    #Run_root = tk.Toplevel()
    #Run_root.title('実行中')
    #Run_root.geometry("440x220+750+400")
    #Run_root.iconbitmap(icon)
    #Run_root.option_add('*font',['メイリオ',12])

    #Run_label = tk.Label(Run_root, text='test')
    #Run_label.pack(padx=40)
    #Run_frame = tk.Frame(Run_root)

    url = URL_Entry.get()
    path = path_Entry.get()

    if url == '':
        URL_error = tkmsg.showerror(title='URL',message='URLが入力されていません。')

    if path == '':
        path_error = tkmsg.showerror(title='フォルダを指定',message='どこのフォルダを参照するか指定してください。')

    try:
        if  str_var.get() == 'mp3':
            outtmpl = '%(title)s.%(ext)s'
            down_dir = path + '/'
            ydl_opts = {'outtmpl': down_dir + outtmpl,
            'options':'-k',
            'format' : 'bestaudio',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Run_info = tkmsg.showinfo(title='実行完了',message='mp3として変換が完了しました。')

        elif str_var.get() == 'mp4':
            outtmpl = '%(title)s.%(ext)s'
            down_dir = path + '/'
            ydl_opts = {'outtmpl': down_dir + outtmpl,
            'options':'-k',
            'format' : 'best',
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            Run_info = tkmsg.showinfo(title='実行完了',message='mp4として変換が完了しました。')
            
    finally:
        URL_Entry.delete(0,tk.END)

# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = fidi.askdirectory(initialdir = iDir)
    path_Entry0.set(iDirPath)

if __name__ == '__main__':
    #メインメニュー
    root = tk.Tk()
    root.title('youtube変換アプリ ~2.0ver~')
    root.geometry("1000x500+440+250")
    root.configure(bg=color)
    root.option_add("*font", ["メイリオ",12])

    #ラジオボタンのクラス作成
    str_var = StringVar(value="mp3")
    mp3Radio = ttk.Radiobutton(root,text = "mp3",value="mp3",variable=str_var)
    mp3Radio.place(x = 400,y = 310)
    mp4Radio = ttk.Radiobutton(root,text = "mp4",value="mp4",variable=str_var)
    mp4Radio.place(x = 500, y = 310)

    #labelの設定
    menu_title = tk.Label(root,text='youtube変換（mp3 or mp4)',font=('',"20"))
    menu_title.pack(padx=50,pady=20)

    URL_label = tk.Label(root,text='１．URL：')
    URL_label.place(x=20,y=100)

    path_label = tk.Label(root,text='２．フォルダを指定：')
    path_label.place(x=20,y=200)

    radio_label = tk.Label(root,text='３．ファイル形式を選択：')
    radio_label.place(x=20,y=300)

    Run_label = tk.Label(root, text='４.実行:')
    Run_label.place(x=20,y=400)

    #Entryの設定&内容の取得)
    URL_Entry = tk.Entry(root, bg= 'white', width=77,bd = 5)
    URL_Entry.place(x=110,y=98)

    path_Entry0 = StringVar()
    path_Entry = tk.Entry(root,textvariable=path_Entry0, bg='white',width=69,bd=5)
    path_Entry.place(x=190,y=198)

    #ボタンの作成
    del_URL_Entry = tk.Button(root,bg='white',text='削除')
    del_URL_Entry.place(x= 925,y=98)
    del_URL_Entry["command"] = URL_delete

    Path_button = tk.Button(root,bg = 'white',text='参照')
    Path_button.place(x=925,y=198)
    Path_button["command"] = dirdialog_clicked

    Run_button = tk.Button(root,bg = 'white',text='変換する')
    Run_button.place(x=100,y=395)
    Run_button["command"] = Run

    #メニューバーの作成
    men = tk.Menu(root)
    root.config(menu = men)
    menu_file1 = tk.Menu(root, tearoff = False)
    men.add_cascade(label = "メニュー", menu = menu_file1)
    menu_file1.add_command(label = "ヘルプ", command=help_page)
    menu_file1.add_command(label = 'アップデート情報',command=details_page)
    menu_file1.add_command(label = "終了", command = shutdown)

    root.mainloop()