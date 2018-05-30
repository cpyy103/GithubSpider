# -*-coding:utf-8-*-
import pymysql


conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='666666',
    db='github',
    charset='utf8'
)

cursor = conn.cursor()


def get_rank(table, item):
    print('----------')
    print(table+'-'+item+'-rank')
    print(table+'\t\t\t\t\t\t\t'+item)
    if table == 'user':
        name = 'name'
    elif table == 'repo':
        name = 'repo'
    cursor.execute('select {name},{item1} from {table} order by {item2} desc limit 20'.format(name=name, item1=item, table=table, item2=item))
    j = 0
    for i in cursor.fetchall():
        j += 1
        print(str(j)+'.\t'+i[0]+'\t\t'+str(i[1]))


def get_language_num():
    print('----------')
    print('repo_language_rank')
    print('language\t\t\tnum')
    cursor.execute('select language,count(*) from repo  group by language')
    rank = cursor.fetchall()
    r = sorted(rank, key=lambda language:language[1], reverse=True)
    j = 0
    for i in r:
        j += 1
        print(str(j)+'.\t'+i[0]+'\t\t'+str(i[1]))


if __name__ == '__main__':
    get_rank('user', 'repositories')
    get_rank('user', 'followers')
    get_rank('user', 'followings')
    get_rank('user', 'stars')
    get_rank('repo', 'fork')
    get_rank('repo', 'star')
    get_language_num()




