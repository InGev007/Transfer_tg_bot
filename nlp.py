import sqlite3
import re

log=0


def nlptest(text):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT * FROM nlp")
    res = res.fetchall()
    if len(res) == 0:
        return "Заполните таблицу связей NLP"
    if log == 1: print(res)
    answ=[]
    for i in res:
        if log == 1: print(i)
        result = re.search(i[0], text)
        if result is not None:
           answ.append(i[1])
    otv=''
    if len(answ)!=0:
        for i in answ:
            if log == 1: print(i)
            sql = con.execute("SELECT text FROM faq WHERE name = '%s'" % i)
            otv+=sql.fetchone()[0]
    con.close()
    return otv

def mattest(text):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT mat FROM mat")
    res = res.fetchall()
    con.close()
    if len(res) == 0:
        return "Заполните таблицу матов"
    if log == 1: print(res)
    otv=0
    for i in res:
        if log == 1: print(i)
        result = re.search(i[0], text)
        if result is not None:
           #answ.append(i[1])
           otv=1
           return otv
    return otv