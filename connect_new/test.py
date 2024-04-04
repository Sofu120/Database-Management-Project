import sqlite3

# 建立與資料庫的連線
con = sqlite3.connect("MyDataBase.db")

if con:
    print("成功連接到資料庫")
else:
    print("連接失敗")

cur = con.cursor()

# 執行 SQL 查詢
res = cur.execute("SELECT TrackID FROM Track")
result = res.fetchone()
# print(result)
while result:
    print(result)
    result = cur.fetchone()


# 印出內容
# for row in cur.execute("SELECT TrackID, Track_Name FROM Track ORDER BY TrackID"):
#     print(row)

con.close