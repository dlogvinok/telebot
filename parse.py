import requests
import json
import datetime

"""Линия для лайва"""
url = 'https://line.fbwebdn.com/live/currentLine/ru/'
r = requests.get(url, timeout = 10)
f = json.loads(r.text)
sports = f['sports']
events = f['events']
scores = f['eventMiscs']

def char_code(c):
    return c.decode('utf-8')

def get_events(foot):
    """Функция возвращает массив всех событий выбранного вида спорта"""
    m = []
    for sport in sports:
        if str(foot).lower() in str(sport['name']).lower() and sport['id'] != 1:
            m.append((sport['name'],sport['id']))
    return sorted(list(m))

def get_result(vid):
    """Функция возвращает событие, счет, время"""
    m = []
    for event in events:
        if event['sportId'] == int(vid) and event['rootKind'] == 1:
            for s in [i for i in scores if i['id'] == event['id']]:
                if len(s) > 0:
                    # m.append(sport['name'])
                    m.append('{} <b>{}</b> : <b>{}</b> {} {} мин'.format(event['team1'], s['score1'], s['score2'], event['team2'],
                                                        round(int(s['timerSeconds']) / 60)))
    return m

def get_champ(vid):
    """Функция возвращает название чемпионата"""
    try:
        s = [i['name'] for i in sports if i['id'] == int(vid)]
        return s
    except:
        pass


def get_line():
    m = []
    url = 'https://line.fbwebdn.com/line/currentLine/ru/'
    r = requests.get(url, timeout=10)
    f = json.loads(r.text)

    sports = f['sports']
    events = f['events']

    for sport in sports:
        try:
            if sport['parentId']:
                for event in events:
                    if sport['id'] == event['sportId']:
                        m.append(
                            (sport['id'],
                             sport['name'],
                             event['team1'],
                             event['team2'],
                             datetime.datetime.fromtimestamp(int(event['startTime'])).strftime('%Y-%m-%d %H:%M:%S'))
                        )
        except Exception as a:
            pass
    return m

# for i in get_events('Волейбол'):
#     print(i)
            # print(sport)

# for sport in sports:
#     if str('Волейбол').lower() in str(sport['name']).lower() and sport['id'] != 1 and sport['name'] != 'Волейбол':

# def get_result(foot):
#     m = []
# for sport in sports:
#     # print(foot)
#     if str('Волейбол').lower() in str(sport['name']).lower():
#         # print(foot, sport['name'])
#         for event in events:
#             if sport['id'] == event['sportId'] and event['rootKind'] == 1:
#                 s = [i for i in scores if i['id'] == event['id']]
#                 if len(s) > 0:
#                     print(s)
#                         m.append(sport['name'])
#                         m.append('{} {} : {} {}'.format(event['team1'], s[0]['score1'], s[0]['score2'], event['team2']))
#     return m

# print(get_events('Баскетбол'))
# print(get_result('Баскетбол'))
# 6
# 40228

# for i in events:
#     if i['sportId'] == 36555 and i['rootKind'] != 1:
#         print(i)

# print(get_result(36555))
# print(len(get_events('Хоккей')))
# print(get_events('Хоккей'))

# for sport in sports:
#     if str('Хоккей').lower() in str(sport['name']).lower() and sport['id'] != 1:
#         print(sport)
        # m.append((sport['name'], sport['id']))

# for i in sports:
#     # 12584
#     if i['id'] == 12584:
#         print(i)
#
# s = [i['name'] for i in sports if i['id'] == 12584]
# print(s)
# print(s[0]['name'])
# print(len(s))
