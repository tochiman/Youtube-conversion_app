# モジュールのインポート
import tkinter as tk
import tkinter.ttk as ttk
import cursor_db
import sqlite3


dbname='main.db'
conn=sqlite3.connect(dbname)
cur=conn.cursor()
sql="select * from history"


# ルートフレームの作成
root = tk.Tk()
# ツリービューの作成
tree = ttk.Treeview(root)

# 列インデックスの作成
tree["columns"] = (1,2,3)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1,width=50)
tree.column(2,width=75)
tree.column(3,width=100)
# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1,text="ID")
tree.heading(2,text="日付")
tree.heading(3,text="URL")

# レコードの作成
# 1番目の引数-配置場所（ツリー形式にしない表設定ではブランクとする）
# 2番目の引数-end:表の配置順序を最下部に配置
#             (行インデックス番号を指定することもできる)
# 3番目の引数-values:レコードの値をタプルで指定する
for i in cur.execute(sql):
    tree.insert ("","end",values=i)

# ツリービューの配置
tree.pack()
conn.commit()
conn.close()
root.mainloop()