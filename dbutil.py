from aiogram import Bot, types
from aiogram.types import InputFile
import sqlite3
import os
import updatedb

def checkandupdatedb():
    try:
        con = sqlite3.connect("./db/bot.db")
    except sqlite3.OperationalError:
        os.mkdir('db')
    finally:
        con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res=con.executescript(updatedb.updatesql)
    con.commit()
    con.close()
    
async def dumpdb(bot, idu):
    con = sqlite3.connect("./db/bot.db")
    res = cur.execute('SELECT id FROM users WHERE id=%s AND priv=1'% idu)
    res = res.fetchall()
    if len(res)==0:
        await bot.send_message(idu, "У Вас нет досупа.")
        return
    else:
        with open('./db/dump.sql', 'w', encoding='UTF8') as f:
            for line in con.iterdump():
                f.write('%s\n' % line)
        con.close()
        db=InputFile("./db/dump.sql")
        await bot.send_document(chat_id=idu, document=db)
        return