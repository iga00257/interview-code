import pymysql
import csv
import pandas as pd
import time
import os
import datetime
data = pd.read_csv("dns_sample.csv",error_bad_lines=False)
data2 =pd.read_csv("dns_sample.csv",error_bad_lines=False)
del data2["frame.time_epoch"]
timestamp = []
timestamp = data["frame.time_epoch"]
Date=[]
Time=[]
usec=[]
for i in timestamp:
  struct_time = time.localtime(i) # 轉成時間元組
  Date.append(time.strftime("%Y-%m-%d", struct_time))
  Time.append(time.strftime("%H:%M:%S", struct_time))
  i = str(i*(10**6))
  microsc = i[i.find('.')-6:]
  usec.append(microsc)
test = pd.DataFrame({'Date':Date,'Time':Time,"usec":usec})
df = pd.concat([test,data2],axis=1)
df.columns = ["Date","Time",
"usec",
"SourceIP",
"SourcePort",
"DestinationIP",
"DestinationPort",
"DNS"]
df.to_csv("final.csv")
# 資料庫設定
db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "pop12034",
    "db": "test520",
    "charset": "utf8",
}

try:
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cur:
        with open('final.csv', newline='') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.reader(csvfile)
            rows = list(rows)
            # print(rows[0])
            # # 以迴圈輸出每一列
            # # "INSERT INTO root_v('Date', 'Time', 'usec', 'SourceIP', 'SourcePort', 'DestinationIP', 'DestinationPort', 'DNS')"
            # for i in range(len(rows[0])):
            #   print(rows[0][i])
            s = "INSERT INTO root_v("
            for i in rows[0][1:9]:
                s += i + ", "
            s = s[:-2] + ") VALUES("
            print(s)
            v = ""
            for i in rows[1:]:
                k = s
                for j in i[1:9]:
                    # print(j)
                    k += f"'{j}',"
                    # print(f"'{j}'")
                a = k[:-1] + ")"
                cur.execute(a)
                conn.commit()
    os.remove('final.csv')

except Exception as ex:
    print(ex)
