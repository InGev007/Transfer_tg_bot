from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

import asyncio
import aioschedule

import nlp,dialog
import dbutil, sqlite3
import bot_message

dbutil.checkandupdatedb()
bot= Bot(token=os.getenv("TOKEN_Transfer_tg_bot"))
dp = Dispatcher(bot)
botname=""

async def myname(bot):
    MyUser =await bot.get_me()
    botname=MyUser["username"]
    return botname


def get_command():
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT commands FROM commands ")
    res = res.fetchall()
    con.close()
    commandsgrab=[]
    for i in res:
        commandsgrab.append(i[0])
    return commandsgrab

    
def get_command_data(comm_name):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT dialog,faq FROM commands WHERE commands='%s'"% comm_name)
    res = res.fetchone()
    con.close()
    # print(res)
    if res[0]=='0':
        return 1,res[1]
    else:
        return 0,res[0]
#print(get_command_data('заказ'))


def checkuser(message):
    if message.from_user.id!=message.chat.id:
        con = sqlite3.connect("./db/bot.db")
        cur = con.cursor()
        res = con.execute("SELECT id FROM users WHERE id = %s"%message.from_user.id)
        res=res.fetchall()
        coll=len(res)
        user=[message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code]
        if coll!=0:
            con.execute('UPDATE users SET first_name="%s",last_name="%s",username="%s",language_code="%s",chatbot=0 WHERE id=%s;'% (user[1],user[2],user[3],user[4],user[0]))
        else:
            con.execute('INSERT INTO users (id,first_name,last_name,username,language_code,chatbot,priv) VALUES (%s,"%s","%s","%s","%s",%s,%s);'% (user[0],user[1],user[2],user[3],user[4],0,0))
        con.commit()
        con.close()
    return


@dp.message_handler(commands=['start','help','info'])
async def command_start(message : types.Message):
    if message.from_user.id==message.chat.id:
        con = sqlite3.connect("./db/bot.db")
        cur = con.cursor()
        res = cur.execute("SELECT text FROM faq WHERE name = 'info'")
        res = res.fetchone()
        await bot.send_message(message.from_id, res[0])
        await message.delete()
        res = con.execute("SELECT id FROM users WHERE id = %s"%message.from_user.id)
        res=res.fetchall()
        coll=len(res)
        user=[message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code]
        if coll!=0:
            con.execute('UPDATE users SET first_name="%s",last_name="%s",username="%s",language_code="%s",chatbot=1 WHERE id=%s;'% (user[1],user[2],user[3],user[4],user[0]))
        else:
            con.execute('INSERT INTO users (id,first_name,last_name,username,language_code,chatbot,priv) VALUES (%s,"%s","%s","%s","%s",%s,%s);'% (user[0],user[1],user[2],user[3],user[4],1,0))
        con.commit()
        res = con.execute("DELETE FROM dialoga WHERE `idu`=%s"% message.from_user.id)
        con.commit()
        res = con.execute("DELETE FROM dialog WHERE `idu`=%s"% message.from_user.id)
        con.commit()
        con.close()
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()


#Service command
@dp.message_handler(commands=['add','delete','update','list','ls'])
async def command_service(message : types.Message):
    if message.from_user.id==message.chat.id:
        await bot.send_message(message.from_id, service_comm(message.text.strip('/').split(),message.from_id))
        await message.delete()
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()
    return


@dp.message_handler(commands=['dumpdb'])
async def command_service(message : types.Message):
    if message.from_user.id==message.chat.id:
        await dbutil.dumpdb(bot,message.from_id)
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()
    return
@dp.message_handler(commands=['msg'])
async def command_msg(message : types.Message):
    if message.from_user.id==message.chat.id:
        if message.from_user.is_bot != True:
            msg = message.text.strip('/msg ')
            await bot_message.send_msg(bot, msg, message.from_id, message)
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()
    return
@dp.message_handler(commands=['message'])
async def command_msg(message : types.Message):
    if message.from_user.id==message.chat.id:
        if message.from_user.is_bot != True:
            msg = message.text.strip('/message ')
            await bot_message.send_msg(bot, msg, message.from_id, message)
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()
    return


@dp.message_handler(commands=get_command())
async def command_client(message : types.Message):
    if message.from_user.id==message.chat.id:
        if message.from_user.is_bot != True:
            comm_data,comm_name = get_command_data(message.text.strip('/'))
            if comm_data==0:
                #start dialog
                await bot.send_message(message.from_id, dialog.start(comm_name, message.from_id))
                await message.delete()
            else:
                #start faq
                await bot.send_message(message.from_id, dialog.faq(comm_name))
                await message.delete()
    else:
        await message.reply("Для общения с ботом напиши ему в ЛС @%s"%botname)
        await message.delete()
    return


@dp.message_handler()
async def echo_send(message : types.Message):
    checkuser(message)
    dial, textdiag= dialog.dialog(message.text, message.from_id)
    if dial==2:
        await message.answer(textdiag)
    elif dial==1:
        #отравить финальное сообщение или меню
        await message.answer(textdiag)
        #Получить id админов
        con = sqlite3.connect("./db/bot.db")
        cur = con.cursor()
        res = cur.execute("SELECT id FROM users WHERE priv=1")
        admins = res.fetchall()
        #Получить ответы пользователя
        res = cur.execute("SELECT answer FROM dialoga WHERE idu=%s"%message.from_id)
        answer = res.fechone()
        con.close()
        #отправить админам сообщение
        for admin in admins:
            await bot.send_message(admin, answer)
    elif dial==0:
        result = nlp.nlptest(message.text.lower())
        if result != '':
            await message.reply(result)
        result = nlp.mattest(message.text.lower())
        if result != 0:
            await message.reply('Пожалуйста при мне не материтесь!')
            await message.delete()
    #await bot.send_message(message.from_user.id,message.text)

async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Для сброса и возвращения в главное меню"),
        types.BotCommand(command="/order", description="Для заказа билета"),
    ]
    await bot.set_my_commands(bot_commands)

async def scheduler():
    #aioschedule.every(1).minutes.do(send)
    while True:
        #await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    global botname
    await setup_bot_commands()
    await bot_message.send_msg(bot, "Бот снова с Вами :)")
    asyncio.create_task(scheduler())
    botname = await myname(bot)
    print(botname)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
