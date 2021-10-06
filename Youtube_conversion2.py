import os
import sqlite3
import subprocess
import threading
import time
import tkinter as tk
import tkinter.filedialog as fidi
import tkinter.messagebox as tkmsg
import tkinter.ttk as ttk
import webbrowser
from tkinter import *

import youtube_dl

import cursor_db

#app_version
app_ver='2.0ver'
#様々な関数をまとめたクラス
class var_def():
    #webサイトに飛ぶための関数
    def jump_to_link(self,url):
        webbrowser.open_new(url)
    #アプリケーション終了処理
    def shutdown(self):
        stdw_log = tkmsg.askyesno('通知','アプリケーションを終了します。')
        if stdw_log == False:pass
        else:exit()
    def URL_delete(self):
        URL_Entry.delete(0,tk.END)
#スクリーンを設定もしくは作成する
class var_def_scr():
    #メニューバーの作成
    def menu_bar(self,framewindow):
        men = tk.Menu(framewindow)
        framewindow.config(menu = men)
        menu_file1 = tk.Menu(framewindow, tearoff = False)
        men.add_cascade(label = "メニュー", menu = menu_file1)
        men.add_cascade(label='ヘルプ',command=lambda:help_page.tkraise())
        menu_file1.add_command(label='メインメニューに戻る',command=lambda:main.tkraise())
        menu_file1.add_command(label='設定を開く',command=lambda:setting_screen.tkraise())
        menu_file1.add_command(label='説明書',command=lambda:how_to.tkraise())
        menu_file1.add_command(label='変更履歴（アップデート情報）',command=update_page)
        menu_file1.add_command(label = "終了", command = var_def.shutdown)
    #画面サイズの設定（ウィンドウが中央に行くようになっている）
    def screen_size(self,screen,width,height):
        screen.update_idletasks()
        ww=screen.winfo_screenwidth()
        wh=screen.winfo_screenheight()
        lw=screen.winfo_width()
        lh=screen.winfo_height()
        screen.geometry(str(width)+"x"+str(height)+"+"+str(int(ww/2-width/2))+"+"+str(int(wh/2-height/2)) )
#実行処理
def Run():
    url = URL_Entry.get()
    path = path_Entry.get()
    extension=str_var.get()
    if url == '':
        URL_error = tkmsg.showerror(title='URL',message='URLが入力されていません。')
        return
    if path == '':
        path_error = tkmsg.showerror(title='フォルダを指定',message='どこのフォルダを参照するか指定してください。')
        return
    try:
        print(1)
        import datetime
        dt_now=datetime.datetime.now()
        print(2)
        cursor_db.history_insert(date=dt_now,ext=extension,url=url)
        print(3)
        path_error_select=cursor_db.error_path_select()
        print(4)
        Run_button['state']=tk.DISABLED #変換中に何度も押せないように無効化
        print(5)
        print(6)
        print(path_error_select)
        if  str_var.get() == 'mp3':
            outtmpl = '%(title)s.%(ext)s'
            down_dir = path + '/'
            ydl_opts = {'outtmpl': down_dir + outtmpl,
            'options':'-k',
            'format' : 'bestaudio',
            }
            def down(p):
                try:
                    p.start(15)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    p.stop()
                    Run_info = tkmsg.showinfo(title='実行完了',message='mp3として変換が完了しました。')
                    prog.destroy()
                except Exception as e:
                    if path_error_select=='ここにエラーテキストの出力先を指定してください':
                        tkmsg.showerror("エラー","エラーテキストの出力先を指定していません。")
                        prog.destroy()
                    else:
                        os.chdir(path_error_select)
                        import glob
                        tkmsg.showerror("エラー","エラーが発生しました。詳しくはエラーテキストをご参照ください。")
                        files = glob.glob(f"{path_error_select}\error*.txt")
                        if len(files)==0:
                            with open(file="error1.txt",mode="w") as f:
                                f.write(str(e))
                        else:
                            filenum=int(files[-1].replace(f"{path_error_select}\\error","").replace(".txt",""))+1
                            with open(f'error{filenum}.txt',"w") as f:
                                f.write(str(e))
                    p.stop()
                    prog.destroy()  
            prog = tk.Toplevel()
            var_def_scr.screen_size(screen=prog,width=350,height=60)
            prog.overrideredirect(True)
            p = ttk.Progressbar(prog,mode="indeterminate",maximum=100,length=300)
            p.pack(ipady=5)
            prog_text=ttk.Label(prog,text='ダウンロード中…')

            prog_text.pack()
            t = threading.Thread(target=down, kwargs={"p":p})  #スレッド立ち上げ
            t.start()   #スレッド開始           
        elif str_var.get() == 'mp4':
            outtmpl = '%(title)s.%(ext)s'
            down_dir = path + '/'
            ydl_opts = {'outtmpl': down_dir + outtmpl,
            'options':'-k',
            'format' : 'best',
            }
            def down(p):
                try:
                    p.start(15)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    p.stop()
                    Run_info = tkmsg.showinfo(title='実行完了',message='mp4として変換が完了しました。')
                    prog.destroy()
                except Exception as e:
                    if path_error_select=='ここにエラーテキストの出力先を指定してください':
                        tkmsg.showerror("エラー","エラーテキストの出力先を指定していません。")
                        prog.destroy()
                    else:
                        os.chdir(path_error_select)
                        import glob
                        tkmsg.showerror("エラー","エラーが発生しました。詳しくはエラーテキストをご参照ください。")
                        files = glob.glob(f"{path_error_select}\error*.txt")
                        if len(files)==0:
                            with open(file="error1.txt",mode="w") as f:
                                f.write(str(e))
                        else:
                            filenum=int(files[-1].replace(f"{path_error_select}\\error","").replace(".txt",""))+1
                            with open(f'error{filenum}.txt',"w") as f:
                                f.write(str(e))
                    p.stop()
                    prog.destroy()  
            prog = tk.Toplevel()
            var_def_scr.screen_size(screen=prog,width=350,height=60)
            prog.overrideredirect(True)
            p = ttk.Progressbar(prog,mode="indeterminate",maximum=100,length=300)
            p.pack(ipady=5)
            prog_text=ttk.Label(prog,text='ダウンロード中…')

            prog_text.pack()
            t = threading.Thread(target=down, kwargs={"p":p})  #スレッド立ち上げ
            t.start()   #スレッド開始    
    except Exception as e: 
        print(e)       
        tkmsg.showerror(title='ダウンロードエラー',message='ダウンロード中にエラーが発生しました。詳しくは、ヘルプページを参照してください。')
    finally:
        URL_Entry.delete(0,tk.END)
        Run_button['state']=tk.NORMAL

#アップデート情報ページ
def update_page():
    update_page = tk.Toplevel()
    update_page.title('アップデート情報')
    var_def_scr.menu_bar(framewindow=update_page)
    var_def_scr.screen_size(screen=update_page,width=950,height=435)
    #details_root.configure(bg=color)
    update_page.option_add('*font',['メイリオ',10])

    tk.Label(update_page, text="～アップデート情報～",font=('',"20")).grid(row=0,column=0,pady=10)
    update_page_destroy=ttk.Button(update_page,text='閉じる',command=lambda:update_page.destroy())
    update_page_destroy.grid(row=5,column=2)
    scrollbar_frame = tk.Frame(update_page)
    scrollbar_frame.grid(row=4,padx=10, pady=10)
    listbox2 = tk.Listbox(scrollbar_frame,width=90,height=17,font=("",13),justify='center')
    dese = ['1.1verにて...\n',
        '・ダウンロード先のディレクトリを指定できるようになりました。\n',
        '・このアップデート情報のウィンドウを開設しました。\n',
        '・mp3かmp4で保存するかを選択できるようになりました。\n',
        '・アイコンを設定しました。\n',
        '\n',
        '2.0verにて...(大型アップデート)\n',
        '・メニュー画面を作成しました。\n',
        '・何を変換したか確認できるようになりました。（変換履歴）\n',
        '・見た目の変更を行いました。（モダン風にしました）\n',
        '・設定画面を追加しました。\n',
        '・初期化ボタンを設置しました。\n',
        '・設定画面にてインストール先を設定しておくことができるようになりました。\n',
        '・設定画面にて背景色を変更できるようになりました。（5色対応）\n',
        '・インストーラ中はprogressbar(進捗状況)が確認できるようになりました。\n',
        '・ヘルプページを作成しました。\n',
        '----------------------以下に続きます----------------------\n',
        '・エラーが発生した際に、設定画面にて設定した場所にエラーメッセージをテキストとして保存するようにしました。\n',
        '・URLが入力されていない状態で、「変換する」を押すと、アプリケーションを再起動しない限り、\n',
        '「変換する」ボタンが押せなくなるバグを修正しました。\n',
    ]
    for i in range(len(dese)):
        listbox2.insert(tk.END, str(dese[i]))
    listbox2.grid(row=1,column=0)
    scroll_bar =tk.Scrollbar(scrollbar_frame, command=listbox2.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox2.config(yscrollcommand=scroll_bar.set)
# フォルダ指定の関数
def dirdialog_clicked():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = fidi.askdirectory(initialdir = iDir)
    path_Entry0.set(iDirPath)
#標準インストール先の設定
def dirdialog_clicked2():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = fidi.askdirectory(initialdir = iDir)
    path_Entry1.set(iDirPath)
#標準インストール先の設定
def dirdialog_clicked3():
    iDir = os.path.abspath(os.path.dirname(__file__))
    iDirPath = fidi.askdirectory(initialdir = iDir)
    path_Entry2.set(iDirPath)
def callbackFunc(event):
    opt_get=opt.get()   
    mainmenu.configure(bg=cursor_db.color(name=opt_get))  #ここでbgの色をdbから呼び出す
    cursor_db.intial_color_update(opt_color=opt_get)      #変更した内容をdbにコミットする。
def callbackFunk1():
    install_pass_get=path_Entry1.get()
    cursor_db.intial_install_update(install_place=install_pass_get)
def callbackFunk2():
    error_pass_get=path_Entry2.get()
    cursor_db.error_path_update(error_path=error_pass_get)
def initialize():
    initialize_ask=tkmsg.askokcancel("初期化の確認","すべての設定を初期化しますか？")
    if initialize_ask==True:
        opt.current(0)
        mainmenu.configure(bg=cursor_db.color(name='赤'))
        cursor_db.intial_color_update(opt_color="赤")
        cursor_db.intial_install_update(install_place="ここにインストール先を指定してください。")
        cursor_db.error_path_update(error_path="ここにエラーテキストの出力先を指定してください")
        cursor_db.history_delete()


if __name__ == '__main__':
    var_def=var_def()
    var_def_scr=var_def_scr()
    mainmenu=tk.Tk()                                                  #ウィンドウの用意
    mainmenu.title(f'変換ソフト~{app_ver}~')
    mainmenu.resizable(0, 0)                                          #ウィンドウ最大化無効
    var_def_scr.menu_bar(framewindow=mainmenu)                        #メニューバーの関数の呼び出し
    var_def_scr.screen_size(screen=mainmenu,width=1000,height=500)    #ウィンドウサイズの定義（関数呼び出し）
    mainmenu.iconbitmap(default='youtube.ico')
    mainmenu.option_add("*font",["メイリオ",12])
    mainmenu.grid_columnconfigure(0,weight=1)
    mainmenu.grid_rowconfigure(0,weight=1)

    #メイン画面のフレームの用意
    main=ttk.Frame(mainmenu)
    main.grid(row=0,column=0,sticky="nsew",pady=20)
    #メイン画面のラベル配置
    title_label=ttk.Label(main,text='～メインメニュー～',font=("",20))
    title_label.grid(row=0,column=1)
    #メイン画面のボタン配置
    app_start_button=ttk.Button(main,text="アプリ起動",command=lambda:app_window.tkraise())
    Conversion_his_button=ttk.Button(main,text="変換履歴",command=lambda:chan_his.tkraise(),)
    chan_his_button=ttk.Button(main,text="アップデート情報",command=update_page)
    manual=ttk.Button(main,text='説明書',command=lambda:how_to.tkraise())
    help_button=ttk.Button(main,text="ヘルプ",command=lambda:help_page.tkraise())
    shut_button=ttk.Button(main,text="終了",command=var_def.shutdown)
    app_start_button.grid(row=1,column=0,ipadx=100,padx=70,ipady=10,pady=45)
    Conversion_his_button.grid(row=2,column=0,ipadx=100,padx=70,ipady=10,pady=45)
    chan_his_button.grid(row=3,column=0,ipadx=100,padx=70,ipady=10,pady=45)
    manual.grid(row=1,column=2,ipadx=100,padx=10,ipady=10,pady=45)
    help_button.grid(row=2,column=2,ipadx=100,padx=10,ipady=10,pady=45)
    shut_button.grid(row=3,column=2,ipadx=100,padx=10,ipady=10,pady=45)

    #アプリ起動フレーム
    app_window=ttk.Frame(mainmenu)
    app_window.grid(row=0,column=0,sticky="nsew",pady=20)
    #ラジオボタンのクラス作成
    str_var = StringVar(value="mp3")
    mp3Radio = ttk.Radiobutton(app_window,text = "mp3",value="mp3",variable=str_var).place(x = 400,y = 300)
    mp4Radio = ttk.Radiobutton(app_window,text = "mp4",value="mp4",variable=str_var).place(x = 550, y = 300)
    #labelの設定
    menu_title = tk.Label(app_window,text='変換画面（mp3 or mp4)',font=('',"20")).pack(padx=50,pady=20)
    URL_label = tk.Label(app_window,text='１．URL：').place(x=20,y=100)
    path_label = tk.Label(app_window,text='２．フォルダを指定：').place(x=20,y=200)
    radio_label = tk.Label(app_window,text='３．ファイル形式を選択：').place(x=20,y=300)
    Run_label = tk.Label(app_window, text='４.実行:').place(x=20,y=400)
    #Entryの設定&内容の取得)
    URL_Entry = ttk.Entry(app_window, width=77)
    URL_Entry.place(x=110,y=98)
    path_Entry0 = StringVar()
    path_Entry = ttk.Entry(app_window,textvariable=path_Entry0,width=69)
    path_Entry.insert(0,cursor_db.intial_install_select())
    path_Entry.place(x=190,y=198)
    #ボタンの作成
    del_URL_Entry = ttk.Button(app_window,text='削除',command=var_def.URL_delete).place(x = 910,y = 100)
    Path_button = ttk.Button(app_window,text='参照',command=dirdialog_clicked).place(x=910,y=200)
    Run_button = ttk.Button(app_window,text='変換する',command=Run)
    Run_button.place(x=100,y=405)
    menu_return=ttk.Button(app_window,text='メインメニューに戻る',command=lambda:main.tkraise()).place(x = 850,y = 405)

    #説明書のフレームの作成
    how_to=ttk.Frame(mainmenu)
    how_to.grid(row=0,column=0,sticky="nsew",pady=20)
    #説明書のページの表示
    man = "最初にメインメニューからアプリ起動を選択します。\n"\
        "\n"\
        "1.ダウンロードしたいサイト（※１）のURLを入れてください。\n"\
        "\n"\
        "2.どこのフォルダに保存するかを指定してください。\n"\
        "\n"\
        "3.mp3かmp4かのどちらかファイル形式を選択してください。\n"\
        "（初期設定はmp3が選択されています。）\n"\
        "\n"\
        "4.「変換する」をクリック。\n"\
        "\n"\
        "\n"\
        "※１詳しくはヘルプページを参照してください。"
    help_sentens = tk.Label(how_to,text=man,font=('','17'))
    help_sentens.pack(padx=50,pady=50)
    menu_return=ttk.Button(how_to,text='メインメニューに戻る',command=lambda:main.tkraise())
    menu_return.pack(side='bottom')

    #ヘルプページのフレーム作成
    help_page=ttk.Frame(mainmenu)
    help_page.grid(row=0,column=0,sticky="nsew",pady=20)
    #ヘルプページの表示
    hese ="Q:ダウンロードエラーが発生したら？\n"\
        "A:ダウンロード先が必ずダウンロードできる場所であるか確認してください。\n"\
        "また、URLが正しくない場合はダウンロードができません。\n"\
        "例１：対応しているサイト※１。\n 例２：Youtubeの場合YoutubePremiumに加入していないと見ることができないもの）\n"\
        "\n"\
        "\n"\
        "※１対応しているサイトは次のサイトから確認できます。↓"
    help_sentens = tk.Label(help_page,text=hese,font=('','17'))
    help_sentens.grid(row=0,padx=100,pady=25)
    web = tk.Label(help_page, text="【https://ytdl-org.github.io/youtube-dl/supportedsites.html】", foreground="#449", cursor="hand1")
    web.bind("<Button-1>", lambda e:var_def.jump_to_link("https://ytdl-org.github.io/youtube-dl/supportedsites.html"))
    web.grid(row=1,padx=160)
    menu_return=ttk.Button(help_page,text='メインメニューに戻る',command=lambda:main.tkraise())
    menu_return.grid(row=2,padx=160,pady=50)

    #設定画面のフレーム作成
    setting_screen=ttk.Frame(mainmenu)
    setting_screen.grid(row=0,column=0,sticky="nsew",pady=20)
    setting_title=ttk.Label(setting_screen, text='～設定～',font=("",20))
    setting_title.grid(row=0,column=1,sticky='n')
    #for i in range(3):
    #    setting_screen.grid_columnconfigure(i,weight=1)
    setting_screen.grid_columnconfigure(0,weight=1)   
    setting_screen.grid_columnconfigure(1,weight=1)
    setting_screen.grid_columnconfigure(2,weight=1)
    setting_screen.grid_columnconfigure(3,weight=1)
    setting_screen.grid_rowconfigure(1,weight=30)
    setting_screen.grid_rowconfigure(2,weight=30)
    setting_screen.grid_rowconfigure(3,weight=30)
    setting_screen.grid_rowconfigure(4,weight=30)
    #背景色の設定する
    ttk.Label(setting_screen, text="1:背景色の設定").grid(row=1,column=0, sticky="w",padx=5)
    ttk.Label(setting_screen, text="色").grid(row=1,column=2,sticky='e',ipadx=15)
    opt=ttk.Combobox(setting_screen, values=('赤','青','緑','黄','桃'),width=3)
    opt.grid(row=1, column=1,sticky='e')
    opt.current(cursor_db.intial_color_select())        #dbの色を持ってくる
    mainmenu.configure(bg=cursor_db.color(name=opt.get()))  #ここでbgを現在のcomboboxのやつに適用する。
    opt.bind("<<ComboboxSelected>>", callbackFunc)
    #標準インストール先を指定する
    ttk.Label(setting_screen,text="2.標準インストール先(再起動後に適用)").grid(row=2,column=0,sticky="w",padx=5)
    Path_button1 = ttk.Button(setting_screen,text='参照',command=dirdialog_clicked2).grid(row=2,column=2,sticky='e',padx=10)
    path_Entry1 = StringVar()
    install_path=tk.Entry(setting_screen,textvariable=path_Entry1,width=60,validate="focusout",validatecommand=callbackFunk1)
    install_path.insert(0,cursor_db.intial_install_select())
    install_path.grid(row=2,column=1,sticky=tk.W)
    #エラーテキスト出力先ディレクトリ
    ttk.Label(setting_screen,text="3.エラーテキスト出力先\n            ディレクトリ(再起動後に適用)").grid(row=3,column=0,sticky="w",padx=5)
    Path_button1 = ttk.Button(setting_screen,text='参照',command=dirdialog_clicked3).grid(row=3,column=2,sticky='e',padx=10)
    path_Entry2 = StringVar()
    install_path=tk.Entry(setting_screen,textvariable=path_Entry2,width=60,validate="focusout",validatecommand=callbackFunk2)
    install_path.insert(0,cursor_db.error_path_select())
    install_path.grid(row=3,column=1,sticky=tk.W)
    #初期化ボタン
    ttk.Label(setting_screen,text='4.全初期化(すべての設定が初期化されます）').grid(row=4,column=0,sticky='w',padx=5)
    ttk.Button(setting_screen, text='初期化する',command=initialize).grid(row=4,column=1,sticky='e')


    #変換履歴のフレーム作成
    chan_his=ttk.Frame(mainmenu)
    chan_his.grid(row=0,column=0,sticky="nsew",pady=20)
    chan_his_tit=ttk.Label(chan_his, text='～変換履歴～',font=("",20)).grid(row=0,column=0,pady=10)
    history_allreset=ttk.Button(chan_his,text='履歴の全削除',command=lambda:cursor_db.history_delete_ask())
    history_allreset.grid(row=1,column=1,ipadx=15,sticky=tk.N)
    chan_his_return=ttk.Button(chan_his,text='メインメニューに戻る',command=lambda:main.tkraise())
    chan_his_return.grid(row=1,column=1,pady=10,sticky=tk.S)
    dbname='main.db'
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    tuple_history="select * from history"
    tree=ttk.Treeview(chan_his,height=16)
    tree["columns"]=("ID","date","extension","URL")
    tree["show"]="headings"
    #各列の設定幅の設定
    tree.column("ID",width=50)
    tree.column("date",width=150)
    tree.column("extension",width=45)
    tree.column("URL",width=550)
    #各列のヘッダー設定
    tree.heading("ID",text="ID")
    tree.heading("date",text="日付(y-M-d h:m:s.ms)")
    tree.heading("extension",text="拡張子")
    tree.heading("URL",text="URL")
    i=0
    for r in cur.execute(tuple_history):
        tree.insert("","end",tags=i,values=r)
        if i&2:
            # tagが奇数(レコードは偶数)の場合のみ、背景色の設定
            tree.tag_configure(i,background="red")
        i+=1
    tree.grid(row=1,column=0,pady=20,padx=30)
    conn.commit()
    conn.close()

    main.tkraise()  #メイン画面のフレームを一番上に持っていく
    mainmenu.mainloop()