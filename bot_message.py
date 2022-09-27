from aiogram import Bot, types
import sqlite3
import asyncio


async def send_msg(bot, msg, idu=None, message=None):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    if idu!=None:
        res = cur.execute('SELECT id FROM users WHERE id=%s AND priv=1'% idu)
        res = res.fetchall()
        if len(res)==0:
            await bot.send_message(idu, "У Вас нет досупа.")
            if message!=None:
                await message.delete()
        else:
            res = cur.execute('SELECT id FROM users')
            res = res.fetchall()
            if len(res)!=0:
                for user in res:
                    await bot.send_message(user[0], msg)
                if message!=None:
                    await bot.send_message(idu, "Сообщение отправлено.")
                    await message.delete()
    else:
        res = cur.execute('SELECT id FROM users')
        res = res.fetchall()
        if len(res)!=0:
            for user in res:
                await bot.send_message(user[0], msg)
    con.close()
    return