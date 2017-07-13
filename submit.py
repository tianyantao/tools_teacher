#coding=utf-8
import requests
import time
import pymssql
import random
import re


def submit(subject,homework_title,group_No):
    # subject = 'ShuXue'
    # homework_title = '333'
    # group_No = 667723

    username_list = []

    conn = pymssql.connect(host='sqlserver.233.mistong.com',user='ETeacher',password='ETeacher',database='ETeacher')
    cur = conn.cursor()
    #查找qid list
    cur.execute("SELECT hr.Content FROM ETeacher_Homework_Resource hr  WHERE hr.Title = "+"'"+homework_title+"'")

    qid_list =  eval(cur.fetchall()[0][0])
    #查找groupid
    cur.execute("SELECT gh.GroupID FROM	ETeacher_Group_HomeworkGroup gh JOIN ETeacher_Homework_Resource hr ON gh.HomeworkID = hr.HomeworkID JOIN ETeacher_Group g ON g.ID = gh.GroupID WHERE hr.Title = "+"'"+homework_title+"'"+" AND g.GroupNo = "+str(group_No))
    group_id = cur.fetchall()[0][0]
    #查找homeworkid
    cur.execute("SELECT gh.HomeworkID FROM	ETeacher_Group_HomeworkGroup gh JOIN ETeacher_Homework_Resource hr ON gh.HomeworkID = hr.HomeworkID JOIN ETeacher_Group g ON g.ID = gh.GroupID WHERE hr.Title = "+"'"+homework_title+"'"+" AND g.GroupNo = "+str(group_No))
    homework_id = cur.fetchall()[0][0]

    #查找userid list
    cur.execute("SELECT gs.UserID FROM ETeacher_Group_StudentGroup gsg JOIN ETeacher_Group_Student gs ON gsg.StudentID = gs.ID  WHERE gsg.GroupID = "+str(group_id))
    userid_list = cur.fetchall()
    cur.close()
    conn.close()
    #查找username
    conn = pymssql.connect(host='sqlserver.233.mistong.com',user='CeShi',password='28c5be9426611a12',database='UserCenter')
    cur = conn.cursor()
    for i in userid_list:
        cur.execute("SELECT UserName FROM UC_Member WHERE ID = "+str(i[0]))
        username_list.append(cur.fetchall()[0][0])
    cur.close()
    conn.close()

    q = {}
    for qid in qid_list:
        q[qid] = []
    #查找qid对应的选项id
    conn = pymssql.connect(host='sqlserver.233.mistong.com',user='CeShi',password='28c5be9426611a12',database='TiKu')
    cur = conn.cursor()
    for qid in qid_list:
        cur.execute('SELECT ID FROM TiKu_TiMu_Gao_'+subject+'_Options  WHERE TiMuID= '+"'"+str(qid)+"'")
        options = cur.fetchall()
        for i in options:
            q[qid].append(i[0])
    cur.close()
    conn.close()

    # 答题
    for username in username_list:
        answer = ""
        for i in qid_list:
            answer = answer + str(i) + ":" + str(random.choice(q[i])) + ","
        answer = answer[:-1]
        t = re.findall("(?<=user=tk=).*?(?=;)",str(requests.get('http://my.233.mistong.com/login/prelogin?sid=2&username='+username+'&password=123456').headers))[0]
        print username, requests.post('http://teacher.233.mistong.com/student/myhomework/submitexam',data='g='+str(group_id)+'&h='+str(homework_id)+'&a='+answer+'&t=00%3A00%3A16',headers={'Content-Type':'application/x-www-form-urlencoded','cookie':'user=tk='+t}).content

submit('ShuXue','333',667723)




