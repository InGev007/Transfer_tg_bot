import sqlite3
log=0

def start(comm_name,id):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT text FROM dialogt WHERE name = '%s' AND id = 1" % comm_name)
    res = res.fetchone()
    mess=res[0]
    res = con.execute("INSERT INTO dialog (`idu`,`dialog`) VALUES ('%s',1);" % id)
    con.commit()
    con.close()
    return mess  

def dialog(text,id):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute("SELECT dialog FROM dialog WHERE idu = '%s' AND answer is NULL" % id)
    res = res.fetchall()
    if log == 1: print(res)
    if len(res) == 0:
        con.close()
        return 0,0
    dial=res[0][0]
    res = con.execute("UPDATE dialog  SET answer='%s' WHERE idu = '%s' AND answer is NULL" % (text,id))
    con.commit()
    res = con.execute("SELECT next FROM dialogt WHERE id = '%s'" % dial)
    res = res.fetchone()
    if res==None:
        res = con.execute("DELETE FROM dialoga WHERE `idu`=%s"% id)
        con.commit()
        res = con.execute("DELETE FROM dialog WHERE `idu`=%s"% id)
        con.commit()
        con.close()
        return
    dialn=res[0]
    res = con.execute("INSERT INTO dialog (`idu`,`dialog`) VALUES ('%s','%s');" % (id,dialn))
    con.commit()
    res = con.execute("SELECT text,next FROM dialogt WHERE id = '%s'" % dialn)
    res = res.fetchone()
    mess= res[0]
    dialn=res[1]
    if log == 1: print(res)
    if dialn==0:
        #получить все диалоги
        res = con.execute("SELECT answer FROM dialog WHERE idu = '%s'" % id)
        res = res.fetchall()
        #записать в 1 лист
        answ=''
        i=0
        if log == 1: print(res)
        if log == 1: print(res[0][0])
        while i <= len(res)-2:
            if log == 1: print(i)
            answ+=str(res[i][0])+' '
            if log == 1: print(answ)
            i+=1
        #Удалить старые ответы если они есть
        res = con.execute("DELETE FROM dialoga WHERE `idu`=%s"% id)
        con.commit()
        #Сделать запись в БД
        res = con.execute("INSERT INTO dialoga (`idu`,`answer`) VALUES (%s,'%s');" % (id,answ))
        con.commit()
        #Удалить диалог из базы
        res = con.execute("DELETE FROM dialog WHERE `idu`=%s"% id)
        con.commit()
        con.close()
        #отравить финальное сообщение или меню
        return 1,mess
    con.close()
    return 2, mess
    
def faq(comm_name):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    # print(comm_name)
    res = con.execute("SELECT text FROM faq WHERE name = '%s'"% comm_name)
    res = res.fetchone()
    # print(res)
    mess=res[0]
    con.close()
    return mess  

def service_comm(comm_name,idu):
    if comm_name[0]=='add':
        return 0
    elif comm_name[0]=='delete':
        return 0
    elif comm_name[0]=='update':
        if comm_name[1]=='faq':
            con = sqlite3.connect("./db/bot.db")
            cur = con.cursor()
            # print(comm_name)
            res = con.execute("SELECT name FROM faq WHERE name = '%s'"% comm_name[2])
            res = res.fetchone()
            if res[0]== None:          
                con.close()
                return "Нет такого FAQ"
            else:
                res = con.execute("INSERT INTO dialog (`idu`,`dialog`) VALUES (%s,'%s');" % (idu,300))
                con.commit()
                con.close()
                return "Введите новое сообщение для данного FAQ"
        # if comm_name[1]=='commands':
        #     con = sqlite3.connect("./db/bot.db")
        #     cur = con.cursor()
        #     # print(comm_name)
        #     res = con.execute("SELECT commands FROM commands WHERE commands = '%s'"% comm_name[2])
        #     res = res.fetchone()
        #     if res[0]== None:          
        #         con.close()
        #         return "Нет такой команды"
        #     else:
        #         res = con.execute("INSERT INTO dialog (`idu`,`dialog`) VALUES (%s,'%s');" % (idu,310))
        #         con.commit()
        #         con.close()
        #         return "Введите новое сообщение для данного FAQ"
        return 0
    elif (comm_name[0]=='list') or (comm_name[0]=='ls'):
        return 0
    return "Чтото пошло не так. Уупс." 
