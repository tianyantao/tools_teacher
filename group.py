#coding: utf-8

import requests
import hashlib
import re
import time
import pymssql



# flag = 233
flag = 235

# 创建圈子
def group(uid,title):
    key = 'teacherbd61a36617ac680ebb83c160d'
    m = hashlib.md5()
    m.update(key + title + uid + key)
    sign = m.hexdigest()
    print requests.post('http://teacher.'+str(flag)+'.mistong.com/api/creategroup',
                        data={'uid':uid,'title':title,'sign':sign}).content
# group('80034683', '杭州市第二中学')


# 关联多个管理员账号
def add_admin(uid,gid):
    key = 'teacherbd61a36617ac680ebb83c160d'
    m = hashlib.md5()
    m.update(key + gid + uid + key)
    sign = m.hexdigest()
    print requests.post('http://teacher.'+str(flag)+'.mistong.com/api/AddAdmin',
                        data={'uid':uid,'gid':gid,'sign':sign}).content
# add_admin("80036684,80036686",'487277')


def join_group1(username,groupid):
    t = re.findall("(?<=user=tk=).*?(?=;)",str(requests.get(
        'http://my.'+str(flag)+'.mistong.com/login/prelogin?sid=2&username='+username+'&password=123456').headers))[0]
    print username, requests.post('http://teacher.'+str(flag)+'.mistong.com/student/myclass/applygroup',
                                  data='gno='+groupid+'&msg='+username,
                                  headers={'Content-Type':'application/x-www-form-urlencoded','cookie':'user=tk='+t}).content
# join_group1('xuesheng102', '737214')


# 加入班级,num个学生加入目标groupid的班级
def join_group(groupid, num=100):
    for username in open('usernames'+str(flag)+'.txt','r').readlines()[:num]:
        t = re.findall("(?<=user=tk=).*?(?=;)",str(requests.get(
            'http://my.'+str(flag)+'.mistong.com/login/prelogin?sid=2&username='+username+'&password=123456').headers))[0]
        print username, requests.post('http://teacher.'+str(flag)+'.mistong.com/student/myclass/applygroup',
                                      data='gno='+str(groupid)+'&msg='+username,
                                      headers={'Content-Type':'application/x-www-form-urlencoded','cookie':'user=tk='+t}).content

# join_group(442708, 22)


# SELECT id FROM ETeacher_Group WHERE groupno = 667723
# SELECT id,StudentID,message FROM ETeacher_Group_Apply  WHERE GroupID = (SELECT id FROM ETeacher_Group WHERE groupno = 667723)
# 教师端处理加入申请
def accept(groupid):

    while True:
        if flag == 235:
            t = re.findall("(?<=user=tk=).*?(?=;)", str(requests.get(
                'http://my.'+str(flag)+'.mistong.com/login/prelogin?sid=2&username=' + 'laoshi001' + '&password=123456').headers))[0]
        else:
            t = re.findall("(?<=user=tk=).*?(?=;)", str(requests.get(
                'http://my.' + str(
                    flag) + '.mistong.com/login/prelogin?sid=2&username=' + 'teacher061201' + '&password=123456').headers))[
                0]
        if flag == 233:
            conn = pymssql.connect(host='sqlserver.233.mistong.com', user='ETeacher', password='ETeacher', database='ETeacher')
        else:
            conn = pymssql.connect(host='10.0.0.64', user='ewt360', password='ewt360@123', database='ETeacher')
        cur = conn.cursor()
        cur.execute("SELECT top 10 id,StudentID,message FROM ETeacher_Group_Apply  WHERE GroupID = (SELECT id FROM ETeacher_Group WHERE groupno ="+str(groupid)+")")
        res = cur.fetchall()

        with open('ids.txt', 'w') as f:
            for i in res:
                for j in i:
                    # print j
                    f.write(str(j)+' ')
                f.write('\n')
        ids = []
        for p in open('ids.txt', 'r').readlines():
            p_id = p.split()[0]
            # p_sid = p.split()[1]
            # p_username = p.split()[2]
            ids.append(int(p_id))
        print requests.post('http://teacher.'+str(flag)+'.mistong.com/teacher/classes/BatchAccept',
                            data='ids='+str(ids),
                            headers={'Content-Type':'application/x-www-form-urlencoded', 'cookie': 'user=tk='+ t}).content
        time.sleep(2)


# accept(487277)


