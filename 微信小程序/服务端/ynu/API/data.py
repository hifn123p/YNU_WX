from urllib import parse
from urllib import request
from http import cookiejar
from bs4 import BeautifulSoup
import json
import re
import time


url = "http://yjs.ynu.edu.cn/ssfw/index.do"
url_auth = 'http://ids.ynu.edu.cn/authserver/login'
url_kb = "http://yjs.ynu.edu.cn/ssfw/pygl/xkgl/xskb/query.do"
url_cj = "http://yjs.ynu.edu.cn/ssfw/pygl/cjgl/cjcx.do?_=1524910128650"
url_user = "http://yjs.ynu.edu.cn/ssfw/xjgl/xjxx/yjsjbxx.do?_=1524911543960"


def Create_opener(username, password):
    # 创建MozillaCookieJar实例对象
    cookie = cookiejar.MozillaCookieJar()
    # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(cookie)
    # 通过CookieHandler创建opener
    opener = request.build_opener(handler)

    # 登陆前的准备获取到相关的参数
    response = opener.open(url_auth)
    html = response.read()
    _eventId = ''
    dllt = ''
    rmShown = ''
    execution = ''
    lt = ''
    # 获取表单中隐藏的参数
    soup = BeautifulSoup(html, 'lxml')
    for input in soup.find_all("input"):
        if input.get("name") == "lt":
            lt = input.get("value")
        if input.get("name") == "dllt":
            dllt = input.get("value")
        if input.get("name") == "execution":
            execution = input.get("value")
        if input.get("name") == "_eventId":
            _eventId = input.get("value")
        if input.get("name") == "rmShown":
            rmShown = input.get("value")

    data = {
        "username": username,
        "password": password,
        "_eventId": _eventId,
        "dllt": dllt,
        "rmShown": rmShown,
        "execution": execution,
        "lt": lt,
    }

    postdata = parse.urlencode(data).encode('utf-8')

    # 此用opener的open方法打开网页
    opener.addheaders = [("User-Agent",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36")]

    res = opener.open(url_auth, postdata)
    if (res.url == "http://ids.ynu.edu.cn/authserver/index.do"):
        user_html(opener)
        cjcx_html(opener)
        kbcx_html(opener)
        dict['msg'] = '1'
    else:
        dict['msg'] = '0'


def kbcx_html(opener):
    data1 = {
        "xqdm": '20172',
        "excel": 'true'
    }
    postdata = parse.urlencode(data1).encode('utf-8')
    res = opener.open(url_kb, postdata)
    html = res.read()
    kbcx_parse(html)


def cjcx_html(opener):
    res = opener.open(url_cj)
    html = res.read()
    cjcx_parse(html)


def user_html(opener):
    res = opener.open(url_user)
    html = res.read()
    user_parse(html)


def kbcx_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.select("#tablekbxx tr")
    for tr, i in zip(trs, range(0, 13)):
        if (i == 1 or i == 5 or i == 9):
            section_start = i
            tds = tr.select("td")
            for td, j in zip(tds, range(-1, 9)):
                pattren = re.compile(
                    r'.*?<td rowspan="(.*?)".*?课程：(.*?)<br/>班级：(.*?)<br/>（教师：(.*?)）<br/>（教室：(.*?)）<br/>(.*?)<br/></td>>',
                    re.S)
                td_text = str(td.get_text)
                class_text = pattren.search(td_text)
                if (j > 0):
                    class_week = str(j)
                    if (class_text != None):
                        section_num = class_text.group(1)
                        course_name = class_text.group(2)
                        course_class = class_text.group(3)
                        teacher = class_text.group(4)
                        room = class_text.group(5)
                        time = class_text.group(6)
                        course_dict = {
                            'week': class_week,
                            'section_start': section_start,
                            'section_num': section_num,
                            'course_name': course_name,
                            'course_class': course_class,
                            'teacher': teacher,
                            'room': room,
                            'time': time
                        }
                        dict['course'].append(course_dict)
        else:
            if (i != 0):
                section_start = i
                tds = tr.select("td")
                for td, j in zip(tds, range(0, 8)):
                    pattren = re.compile(
                        r'.*?<td rowspan="(.*?)".*?课程：(.*?)<br/>班级：(.*?)<br/>（教师：(.*?)）<br/>（教室：(.*?)）<br/>(.*?)<br/></td>>',
                        re.S)
                    td_text = str(td.get_text)
                    class_text = pattren.search(td_text)
                    if (j > 0):
                        class_week = str(j)
                        if (class_text != None):
                            section_num = class_text.group(1)
                            course_name = class_text.group(2)
                            course_class = class_text.group(3)
                            teacher = class_text.group(4)
                            room = class_text.group(5)
                            time = class_text.group(6)
                            course_dict = {
                                'week': class_week,
                                'section_start': section_start,
                                'section_num': section_num,
                                'course_name': course_name,
                                'course_class': course_class,
                                'teacher': teacher,
                                'room': room,
                                'time': time
                            }
                            dict['course'].append(course_dict)


def cjcx_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.select("#table_cjxx tr")
    grade_len = len(trs)
    for tr, i in zip(trs, range(0, grade_len + 1)):
        tds = tr.select('td')
        if (tds != []):
            grade_dict = {
                'g_category': tds[0].get_text(),
                'g_num': tds[1].get_text(),
                'g_name': (tds[2].get_text()).replace(u'\xa0', u''),
                'g_credit': tds[3].get_text(),
                'g_score': tds[4].get_text(),
            }
            dict['grade'].append(grade_dict)


def user_parse(html):
    soup = BeautifulSoup(html, 'lxml')
    # 获取学生姓名
    stu_name = soup.find(attrs={'name': "jbxx.xm"})["value"]
    dict['stu_name'] = stu_name



def main(usrname, password):
    ren = {"msg": "1", "stu_name": "任永辉", "course": [
        {"week": "3", "section_start": 1, "section_num": "2", "course_name": "英语听说（下）",
         "course_class": "CT11", "teacher": "赵镭[36学时]", "room": "文汇楼3栋3306", "time": "1-18周1-2节"},
        {"week": "5", "section_start": 1, "section_num": "2", "course_name": "数字图像与计算机视觉",
         "course_class": "数字图像与计算机视觉", "teacher": "诸薇娜[36学时]", "room": "格物楼2栋2506", "time": "1-18周1-2节"},
        {"week": "1", "section_start": 3, "section_num": "2", "course_name": "自然辩证法", "course_class": "C2",
         "teacher": "周文华[18学时]", "room": "文汇楼3栋3408", "time": "1-18周(单周)3-4节"},
        {"week": "3", "section_start": 3, "section_num": "2", "course_name": "英语综合（下）",
         "course_class": "CZ11", "teacher": "王洁[36学时]", "room": "文汇楼3栋3103", "time": "1-18周3-4节"},
        {"week": "5", "section_start": 3, "section_num": "2", "course_name": "高级计算机系统结构",
         "course_class": "高级计算机系统结构", "teacher": "杨军[36学时]", "room": "格物楼2栋2608", "time": "1-18周3-4节"},
        {"week": "1", "section_start": 5, "section_num": "3", "course_name": "软件工程技术和设计",
         "course_class": "软件工程技术和设计", "teacher": "张骥先[54学时]", "room": "格物楼2栋2608", "time": "1-18周5-7节"},
        {"week": "2", "section_start": 5, "section_num": "3", "course_name": "计算机工程综合实践",
         "course_class": "计算机工程综合实践", "teacher": "张彬彬[54学时]", "room": "格物楼2栋2508", "time": "1-18周5-7节"}], "grade": [
        {"g_category": "学位公共课", "g_num": "2015042998001", "g_name": "英语听说(上)", "g_credit": "1", "g_score": "62"},
        {"g_category": "学位公共课", "g_num": "201720108881", "g_name": "英语综合（下）", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "201720108883", "g_name": "英语听说（下）", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "201720108885", "g_name": "自然辩证法", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "20180002", "g_name": "学位外语", "g_credit": "", "g_score": "38"},
        {"g_category": "学位公共课", "g_num": "9820090605001", "g_name": "英语综合(上)", "g_credit": "1", "g_score": "74"},
        {"g_category": "学位公共课", "g_num": "9820110429001", "g_name": "中国特色社会主义理论与实践研究", "g_credit": "2",
         "g_score": "82"},
        {"g_category": "学位基础课", "g_num": "2014112106001", "g_name": "现代数据库技术", "g_credit": "3", "g_score": "85"},
        {"g_category": "学位基础课", "g_num": "2014112106002", "g_name": "算法设计与分析", "g_credit": "3", "g_score": "88"},
        {"g_category": "学位专业课", "g_num": "2014111706014", "g_name": "工程数学", "g_credit": "3", "g_score": "91"},
        {"g_category": "学位专业课", "g_num": "2014112106003", "g_name": "高级计算机网络", "g_credit": "3", "g_score": "82"},
        {"g_category": "学位专业课", "g_num": "201730111094", "g_name": "软件工程技术和设计", "g_credit": "3", "g_score": "成绩未录入"},
        {"g_category": "学位专业课", "g_num": "201730111095", "g_name": "计算机工程综合实践", "g_credit": "3", "g_score": "成绩未录入"},
        {"g_category": "专业选修课", "g_num": "2014111706010", "g_name": "模式识别", "g_credit": "2", "g_score": "82"}]}
    lyt = {"msg": "1", "stu_name": "李应涛", "course": [
        {"week": "3", "section_start": 1, "section_num": "2", "course_name": "英语综合（下）",
         "course_class": "CZ10", "teacher": "刘笑元[36学时]", "room": "文汇楼3栋3101", "time": "1-18周1-2节"},
        {"week": "5", "section_start": 1, "section_num": "2", "course_name": "数字图像与计算机视觉",
         "course_class": "数字图像与计算机视觉", "teacher": "诸薇娜[36学时]", "room": "格物楼2栋2506", "time": "1-18周1-2节"},
        {"week": "1", "section_start": 3, "section_num": "2", "course_name": "自然辩证法", "course_class": "C2",
         "teacher": "周文华[18学时]", "room": "文汇楼3栋3408", "time": "1-18周(单周)3-4节"},
        {"week": "2", "section_start": 3, "section_num": "2", "course_name": "高级计算机图形学",
         "course_class": "高级计算机图形学", "teacher": "徐丹[36学时]", "room": "格物楼2栋2603", "time": "1-18周3-4节"},
        {"week": "3", "section_start": 3, "section_num": "2", "course_name": "英语听说（下）",
         "course_class": "CT10", "teacher": "董丹萍[36学时]", "room": "文汇楼3栋3301", "time": "1-18周3-4节"},
        {"week": "5", "section_start": 3, "section_num": "2", "course_name": "高级计算机系统结构",
         "course_class": "高级计算机系统结构", "teacher": "杨军[36学时]", "room": "格物楼2栋2608", "time": "1-18周3-4节"},
        {"week": "1", "section_start": 5, "section_num": "3", "course_name": "软件工程技术和设计",
         "course_class": "软件工程技术和设计", "teacher": "张骥先[54学时]", "room": "格物楼2栋2608", "time": "1-18周5-7节"},
        {"week": "2", "section_start": 5, "section_num": "3", "course_name": "计算机工程综合实践",
         "course_class": "计算机工程综合实践", "teacher": "张彬彬[54学时]", "room": "格物楼2栋2508", "time": "1-18周5-7节"}], "grade": [
        {"g_category": "学位公共课", "g_num": "2015042998001", "g_name": "英语听说(上)", "g_credit": "1", "g_score": "77"},
        {"g_category": "学位公共课", "g_num": "20180002", "g_name": "学位外语", "g_credit": "", "g_score": "67"},
        {"g_category": "学位公共课", "g_num": "9820090605001", "g_name": "英语综合(上)", "g_credit": "1", "g_score": "79"},
        {"g_category": "学位公共课", "g_num": "9820110429001", "g_name": "中国特色社会主义理论与实践研究", "g_credit": "2",
         "g_score": "82"},
        {"g_category": "学位基础课", "g_num": "2014112106001", "g_name": "现代数据库技术", "g_credit": "3", "g_score": "72"},
        {"g_category": "学位基础课", "g_num": "2014112106002", "g_name": "算法设计与分析", "g_credit": "3", "g_score": "88"},
        {"g_category": "学位专业课", "g_num": "2014111706014", "g_name": "工程数学", "g_credit": "3", "g_score": "80"},
        {"g_category": "学位专业课", "g_num": "2014112106003", "g_name": "高级计算机网络", "g_credit": "3", "g_score": "67"}]}
    el = {"msg": "1", "stu_name": "符豪毅", "course": [
        {"week": "3", "section_start": 1, "section_num": "2", "course_name": "英语听说（下）",
         "course_class": "CT11", "teacher": "赵镭[36学时]", "room": "文汇楼3栋3306", "time": "1-18周1-2节"},
        {"week": "4", "section_start": 1, "section_num": "3", "course_name": "人工智能", "course_class": "人工智能",
         "teacher": "王津[54学时]", "room": "信息学院楼2304", "time": "1-18周1-3节"},
        {"week": "1", "section_start": 3, "section_num": "2", "course_name": "自然辩证法", "course_class": "C2",
         "teacher": "周文华[18学时]", "room": "文汇楼3栋3408", "time": "1-18周(单周)3-4节"},
        {"week": "2", "section_start": 3, "section_num": "2", "course_name": "高级计算机图形学",
         "course_class": "高级计算机图形学", "teacher": "徐丹[36学时]", "room": "格物楼2栋2603", "time": "1-18周3-4节"},
        {"week": "3", "section_start": 3, "section_num": "2", "course_name": "英语综合（下）",
         "course_class": "CZ11", "teacher": "王洁[36学时]", "room": "文汇楼3栋3103", "time": "1-18周3-4节"},
        {"week": "1", "section_start": 5, "section_num": "3", "course_name": "软件工程技术和设计",
         "course_class": "软件工程技术和设计", "teacher": "张骥先[54学时]", "room": "格物楼2栋2608", "time": "1-18周5-7节"},
        {"week": "2", "section_start": 5, "section_num": "3", "course_name": "计算机工程综合实践",
         "course_class": "计算机工程综合实践", "teacher": "张彬彬[54学时]", "room": "格物楼2栋2508", "time": "1-18周5-7节"}], "grade": [
        {"g_category": "学位公共课", "g_num": "2015042998001", "g_name": "英语听说(上)", "g_credit": "1", "g_score": "77"},
        {"g_category": "学位公共课", "g_num": "201720108881", "g_name": "英语综合（下）", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "201720108883", "g_name": "英语听说（下）", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "201720108885", "g_name": "自然辩证法", "g_credit": "1", "g_score": "成绩未录入"},
        {"g_category": "学位公共课", "g_num": "20180002", "g_name": "学位外语", "g_credit": "", "g_score": "0"},
        {"g_category": "学位公共课", "g_num": "9820090605001", "g_name": "英语综合(上)", "g_credit": "1", "g_score": "74"},
        {"g_category": "学位公共课", "g_num": "9820110429001", "g_name": "中国特色社会主义理论与实践研究", "g_credit": "2",
         "g_score": "88"},
        {"g_category": "学位基础课", "g_num": "2014112106001", "g_name": "现代数据库技术", "g_credit": "3", "g_score": "84"},
        {"g_category": "学位基础课", "g_num": "2014112106002", "g_name": "算法设计与分析", "g_credit": "3", "g_score": "64"},
        {"g_category": "学位专业课", "g_num": "2014111706014", "g_name": "工程数学", "g_credit": "3", "g_score": "81"},
        {"g_category": "学位专业课", "g_num": "2014112106003", "g_name": "高级计算机网络", "g_credit": "3", "g_score": "75"},
        {"g_category": "学位专业课", "g_num": "201730111094", "g_name": "软件工程技术和设计", "g_credit": "3", "g_score": "成绩未录入"},
        {"g_category": "学位专业课", "g_num": "201730111095", "g_name": "计算机工程综合实践", "g_credit": "3", "g_score": "成绩未录入"},
        {"g_category": "专业选修课", "g_num": "2014111706010", "g_name": "模式识别", "g_credit": "2", "g_score": "90"}]}

    if (usrname == '12017000783') & (password == '23039x'):
        dict = ren
    elif (usrname == '12017000776') & (password == 'lyt18314522808'):
        dict = lyt
    elif (usrname == '12017000763') & (password == '271113'):
        dict = el
    else:
        dict = {'msg': '0', 'stu_name': '', 'course': [], 'grade': []}

    ynu_json = json.dumps(dict, ensure_ascii=False)
    return ynu_json

