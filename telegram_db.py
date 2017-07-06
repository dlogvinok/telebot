import datetime
import parse
import re

def check(s):
    try:
        return s
    except:
        return ''

def add_user(m, conn, base):
    """
    Сохранение доступной информации о пользователе
    """
    try:
        base.execute("insert into users VALUES (?,?,?,?,?)",
                     (m.chat.id, m.chat.first_name, m.chat.last_name,m.chat.username, datetime.datetime.today()))
        conn.commit()
        print('Ok')
    except Exception as e:
        print(e)
        pass

def insert_line(conn, base):
    try:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = parse.get_line()
        if len(line) > 0:
            base.execute("select count(*) from events where last_upd >= datetime('now', 'localtime', '+12 hour')")
            last_upd = base.fetchall()
            if last_upd[0][0] > 0 :
                base.execute("DELETE FROM events")
                print('Линия удалена')
                conn.commit()
                for i in line:
                    base.execute("insert into events VALUES (?,?,?,?,?,?)",
                                 (check(i[0]),
                                  check(i[1]),
                                  check(i[2]),
                                  check(i[3]),
                                  check(i[4]),
                                  now)
                                )
                    conn.commit()
    except:
        pass

def get_event_name(con, base, s):
    n = []
    try:
        s = "select distinct name, id from events where name like '%{}%'".format(s[1:])
        # print(s)
        base.execute(s)
        n = base.fetchall()
    except:
        pass
    return n

def get_event_hour(conn, base, h, f):
    try:
        sql = "select distinct name, id from events " \
              "where start_time <= datetime('now', 'localtime', '+{} hour') " \
              "and name like '%{}%' " \
              "and start_time >= datetime('now', 'localtime')".format(h, re.findall('[а-яА-Я]+', f)[0][1:])
        base.execute(sql)
        r = base.fetchall()
    except:
        r = ''
    return r