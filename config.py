# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:55:49 2023

@author: kentang
"""

import re
import math
import datetime
from itertools import cycle, repeat
from sxtwl import fromSolar
import ephem

cnum = list("一二三四五六七八九十")
#干支
tian_gan = '甲乙丙丁戊己庚辛壬癸'
di_zhi = '子丑寅卯辰巳午未申酉戌亥'
cnumber = list("一二三四五六七八九")
door_r = list("休生傷杜景死驚開")
eight_gua = list("坎坤震巽中乾兌艮離")
clockwise_eightgua = list("坎艮震巽離坤兌乾")
golen_d = re.findall("..","太乙攝提軒轅招搖天符青龍咸池太陰天乙")
wuxing = "火水金火木金水土土木,水火火金金木土水木土,火火金金木木土土水水,火木水金木水土火金土,木火金水水木火土土金"
wuxing_relation_2 = dict(zip(list(map(
    lambda x: tuple(re.findall("..",x)), wuxing.split(","))),
    "尅我,我尅,比和,生我,我生".split(",")))
cmonth = list("一二三四五六七八九十") + ["十一","十二"]
jieqi_name = re.findall('..', '春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水驚蟄')
jj = {"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}

#%% 基本功能函數
def split_list(lst, chunk_size):
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def new_list(olist, o):
    a = olist.index(o)
    res1 = olist[a:] + olist[:a]
    return res1

def new_list_r(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append(olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code - 1
    return res1

def gendatetime(year, month, day, hour):
    return "{}年{}月{}日{}時".format(year, month, day, hour)

def repeat_list(n, thelist):
    return [repetition for i in thelist for repetition in repeat(i,n)]

#%% 甲子平支
def jiazi():
    return list(map(lambda x: "{}{}".format(tian_gan[x % len(tian_gan)],
                                            di_zhi[x % len(di_zhi)]),
                                            list(range(60))))

def Ganzhiwuxing(gangorzhi):
    gz_list = "甲寅乙卯震巽,丙巳丁午離,壬亥癸子坎,庚申辛酉乾兌,未丑戊己未辰戌艮坤".split(",")
    ganzhiwuxing = dict(zip(list(map(lambda x: tuple(x), gz_list
                                     )), list("木火水金土")))
    return multi_key_dict_get(ganzhiwuxing, gangorzhi)

def jieqicode(year,month, day, hour, minute):
    """以年月日時分節氣找奇門上中下元局"""
    return multi_key_dict_get({("冬至", "驚蟄"): "一七四",
                               "小寒": "二八五",
                               ("大寒", "春分"): "三九六",
                               "立春":"八五二",
                               "雨水":"九六三",
                               ("清明", "立夏"): "四一七",
                               ("穀雨", "小滿"): "五二八",
                               "芒種": "六三九",
                               ("夏至", "白露"): "九三六",
                               "小暑":"八二五",
                               ("大暑", "秋分"): "七一四",
                               "立秋":"二五八",
                               "處暑":"一四七",
                               ("霜降", "小雪"): "五八二",
                               ("寒露", "立冬"): "六九三",
                               "大雪":"四七一"}, 
                              jq(year,month, day,hour, minute))

def jieqicode_jq(jq):
    """以節氣名稱找奇門上中下元局"""
    return multi_key_dict_get({("冬至", "驚蟄"): "一七四",
                               "小寒": "二八五",
                               ("大寒", "春分"): "三九六",
                               "立春":"八五二",
                               "雨水":"九六三",
                               ("清明", "立夏"): "四一七",
                               ("穀雨", "小滿"): "五二八",
                               "芒種": "六三九",
                               ("夏至", "白露"): "九三六",
                               "小暑":"八二五",
                               ("大暑", "秋分"): "七一四",
                               "立秋":"二五八",
                               "處暑":"一四七",
                               ("霜降", "小雪"): "五八二",
                               ("寒露", "立冬"): "六九三",
                               "大雪":"四七一"}, 
                              jq)

def findyuen(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    return multi_key_dict_get(findyuen_dict(), gz[2])

def findyuen_minute(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    return multi_key_dict_get(findyuen_dict(), gz[3])

def find_wx_relation(zhi1, zhi2):
    combine_zhi = Ganzhiwuxing(zhi1) + Ganzhiwuxing(zhi2)
    return multi_key_dict_get(wuxing_relation_2, combine_zhi)
#換算干支
def gangzhi1(year, month, day, hour, minute):
    if hour == 23:
        d = ephem.Date(round((ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day+1).zfill(2),
            str(0).zfill(2)))),3))
    else:
        d = ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day).zfill(2),
            str(hour).zfill(2)))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG,mTG,dTG,hTG = "{}{}".format(
        tian_gan[cdate.getYearGZ().tg],
        di_zhi[cdate.getYearGZ().dz]), "{}{}".format(
            tian_gan[cdate.getMonthGZ().tg],
            di_zhi[cdate.getMonthGZ().dz]), "{}{}".format(
                tian_gan[cdate.getDayGZ().tg],
                di_zhi[cdate.getDayGZ().dz]), "{}{}".format(
                    tian_gan[cdate.getHourGZ(dd[3]).tg],
                    di_zhi[cdate.getHourGZ(dd[3]).dz])
    if year < 1900:
        mTG1 = find_lunar_month(yTG).get(lunar_date_d(year, month, day).get("月"))
    else:
        mTG1 = mTG
    hTG1 = find_lunar_hour(dTG).get(hTG[1])
    return [yTG, mTG1, dTG, hTG1]

def gangzhi(year, month, day, hour, minute):
    if hour == 23:
        d = ephem.Date(round((ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day+1).zfill(2),
            str(0).zfill(2)))),3))
    else:
        d = ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day).zfill(2),
            str(hour).zfill(2)))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG,mTG,dTG,hTG = "{}{}".format(
        tian_gan[cdate.getYearGZ().tg],
        di_zhi[cdate.getYearGZ().dz]), "{}{}".format(
            tian_gan[cdate.getMonthGZ().tg],
            di_zhi[cdate.getMonthGZ().dz]), "{}{}".format(
                tian_gan[cdate.getDayGZ().tg],
                di_zhi[cdate.getDayGZ().dz]), "{}{}".format(
                    tian_gan[cdate.getHourGZ(dd[3]).tg],
                    di_zhi[cdate.getHourGZ(dd[3]).dz])
    if year < 1900:
        mTG1 = find_lunar_month(yTG).get(lunar_date_d(year, month, day).get("月"))
    else:
        mTG1 = mTG
    hTG1 = find_lunar_hour(dTG).get(hTG[1])
    zi = gangzhi1(year, month, day, 0, 0)[3]
    if minute < 10 and minute >=0:
        reminute = "00"
    if minute < 20 and minute >=10:
        reminute = "10"
    if minute < 30 and minute >=20:
        reminute = "20"
    if minute < 40 and minute >=30:
        reminute = "30"
    if minute < 50 and minute >=40:
        reminute = "40"
    if minute < 60 and minute >=50:
        reminute = "50"
    hourminute = str(hour)+":"+str(reminute)
    gangzhi_minute = ke_jiazi_d(zi).get(hourminute)
    return [yTG, mTG1, dTG, hTG1, gangzhi_minute]
#旬
def shun(gz):
    d_value1 = dict(zip(di_zhi, list(range(1,13)))).get(gz[1])
    d_value2 =  dict(zip(tian_gan, list(range(1,11)))).get(gz[0])
    shun_value = d_value1 - d_value2
    if shun_value < 0:
        shun_value = shun_value+12
    return {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}.get(shun_value)
#五虎遁，起正月
def find_lunar_month(year):
    fivetigers = {
    tuple(list('甲己')):'丙寅',
    tuple(list('乙庚')):'戊寅',
    tuple(list('丙辛')):'庚寅',
    tuple(list('丁壬')):'壬寅',
    tuple(list('戊癸')):'甲寅'
    }
    if multi_key_dict_get(fivetigers, year[0]) == None:
        result = multi_key_dict_get(fivetigers, year[1])
    else:
        result = multi_key_dict_get(fivetigers, year[0])
    return dict(zip(range(1,13),new_list(jiazi(), result)[:12]))

#五鼠遁，起子時
def find_lunar_hour(day):
    fiverats = {
    tuple(list('甲己')):'甲子',
    tuple(list('乙庚')):'丙子',
    tuple(list('丙辛')):'戊子',
    tuple(list('丁壬')):'庚子',
    tuple(list('戊癸')):'壬子'
    }
    if multi_key_dict_get(fiverats, day[0]) == None:
        result = multi_key_dict_get(fiverats, day[1])
    else:
        result = multi_key_dict_get(fiverats, day[0])
    return dict(zip(list(di_zhi), new_list(jiazi(), result)[:12]))

#五馬遁，起子刻
def find_lunar_ke(hour):
    fivehourses = {
    tuple(list('丙辛')):'甲午',
    tuple(list('丁壬')):'丙午',
    tuple(list('戊癸')):'戊午',
    tuple(list('甲己')):'庚午',
    tuple(list('乙庚')):'壬午'
    }
    if multi_key_dict_get(fivehourses, hour[0]) == None:
        result = multi_key_dict_get(fivehourses, hour[1])
    else:
        result = multi_key_dict_get(fivehourses, hour[0])
    return new_list(jiazi(), result)

def liujiashun_dict():
    jz = jiazi()[0::10]
    jzlist = list(map(lambda x:new_list(jiazi(), x)[0:10],jz))
    nlist = list(map(lambda x: tuple(x), jzlist))
    return dict(zip(nlist, jiazi()[0::10]))

def findyuen_dict():
    jz = jiazi()[0::5]
    jzlist = list(map(lambda i:new_list(jiazi(), i)[0:5],jz))
    nlist = list(map(lambda x:tuple(x), jzlist))
    return dict(zip(nlist, ["上元","中元","下元"]*4))

#分干支
def minutes_jiazi_d():
    t = [f"{h}:{m}" for h in range(24) for m in range(60)]
    minutelist = dict(zip(t, cycle(repeat_list(2, jiazi()))))
    return minutelist

def ke_jiazi_d(hour):
    t = [f"{h}:{m}0" for h in range(24) for m in range(6)]
    minutelist = dict(zip(t, cycle(repeat_list(1, find_lunar_ke(hour)))))
    return minutelist

#農曆
def lunar_date_d(year, month, day):
    lunar_m = ['占位', '正月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '冬月', '腊月']
    day = fromSolar(year, month, day)
    return {"年":day.getLunarYear(),
            "農曆月": lunar_m[int(day.getLunarMonth())],
            "月":day.getLunarMonth(),
            "日":day.getLunarDay()}

#日空時空
def daykong_shikong(year, month, day, hour, minute):
    guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'},
            '甲戌':{'孤':'申酉', '虛':'寅卯'},
            '甲申':{'孤':'午未', '虛':'子丑'},
            '甲午':{'孤':'辰巳', '虛':'戌亥'},
            '甲辰':{'孤':'寅卯', '虛':'申酉'},
            '甲寅':{'孤':'子丑', '虛':'午未'}}
    gz=gangzhi(year, month, day, hour, minute)
    dk = multi_key_dict_get(liujiashun_dict(), gz[2])
    sk = multi_key_dict_get(liujiashun_dict(), gz[3])
    daykong = multi_key_dict_get(guxu, dk).get("孤")
    shikong = multi_key_dict_get(guxu, sk).get("孤")
    return {"日空":daykong,
            "時空":shikong}

def hourkong_minutekong(year, month, day, hour, minute):
    gz=gangzhi(year, month, day, hour, minute)
    g3 = multi_key_dict_get(liujiashun_dict(), gz[3])
    g4 = multi_key_dict_get(liujiashun_dict(), gz[4])
    guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'},
            '甲戌':{'孤':'申酉', '虛':'寅卯'},
            '甲申':{'孤':'午未', '虛':'子丑'},
            '甲午':{'孤':'辰巳', '虛':'戌亥'},
            '甲辰':{'孤':'寅卯', '虛':'申酉'},
            '甲寅':{'孤':'子丑', '虛':'午未'}}
    daykong = multi_key_dict_get(guxu, g3).get("孤")
    shikong = multi_key_dict_get(guxu, g4).get("孤")
    return {"日空":daykong, "時空":shikong}

def find_shier_luck(gan):
    cs = re.findall('..',"長生沐浴冠帶臨冠帝旺")
    nlist = list(map(lambda i:new_list(di_zhi, i),list("亥寅寅巳申")))
    nnlist = list(map(lambda i:new_list(di_zhi, i), list("亥寅寅巳申")))
    cheungsunlist = list("死病衰") + re.findall('..',"帝旺臨冠冠帶沐浴長生") + list("養胎絕墓")
    cslist2 = list(map(lambda y: dict(zip(y, cs + list("衰病死墓絕胎養"))), nlist))
    cslist = [dict(zip(y, cheungsunlist)) for y in nnlist]
    return {**dict(zip(tian_gan[0::2], cslist2)),
            **dict(zip(tian_gan[1::2], cslist))}.get(gan)
#奇門排局拆補
def qimen_ju_name_chaibu(year, month, day, hour, minute):
    yydun = {tuple(new_list(jieqi_name, "冬至")[0:12]):"陽遁",
             tuple(new_list(jieqi_name, "夏至")[0:12]):"陰遁" }
    jieqi = jq(year, month, day, hour, minute)
    find_yingyang = multi_key_dict_get(yydun, jieqi)
    find_yuen = findyuen(year, month, day, hour, minute)
    jieqi_code = jieqicode(year, month, day, hour, minute)
    return "{}{}局{}".format(find_yingyang,{
        "上元":jieqi_code[0],
        "中元":jieqi_code[1],
        "下元":jieqi_code[2]}.get(find_yuen),
        find_yuen)
#奇門排局置閏除虫用
def qimen_ju_name_zhirun_raw(year, month, day, hour, minute):
    Jieqi = jq(year, month, day, hour, minute)
    jlist = split_list(jiazi(), 5)
    new_jq = new_list(jieqi_name, Jieqi)[1]
    new_jq1 = new_list(jieqi_name, Jieqi)[0]
    new_jq2 = new_list(jieqi_name, Jieqi)[-1]
    jlist = [tuple(i) for i in jlist]
    fuhead = dict(zip(jlist, jiazi()[0::5]))
    yy = {tuple(new_list(jieqi_name, "冬至")[0:12]):"陽遁",
          tuple(new_list(jieqi_name, "夏至")[0:12]):"陰遁" }
    yin_yang = multi_key_dict_get(yy,new_jq1)
    jieqi_code = jieqicode(year, month, day, hour, minute)
    hgz = gangzhi(year, month, day, hour, minute)[3][0]
    dgz = gangzhi(year, month, day, hour, minute)[2]
    fd = multi_key_dict_get(fuhead, dgz)
    zftg = zhifu_tiangan(year, month, day, hour, minute)
    ju_day_dict = {tuple(["甲子","甲午","己卯","己酉"]):"上元",
                   tuple(["甲寅","甲申","己巳","己亥"]):"中元",
                   tuple(["甲辰","甲戌","己丑","己未"]):"下元"}
    three_yuen = multi_key_dict_get(ju_day_dict, fd)
    Jieqi_disance = jq_distance(year, month, day, hour, minute)[0].get(Jieqi)
    current = jq_distance(year, month, day, hour, minute)[1]
    current_ts = datetime.datetime.strptime(current, "%Y/%m/%d %H:%M:%S")
    jq_distance_ts = datetime.datetime.strptime(Jieqi_disance,"%Y/%m/%d %H:%M:%S")
    difference = (current_ts-jq_distance_ts).days
    kooks =  {"上元":jieqi_code[0],
              "中元":jieqi_code[1],
              "下元":jieqi_code[2]}.get(three_yuen)
    jieqi_code1 = jieqicode_jq(new_jq)
    jieqi_code2 = jieqicode_jq(new_jq1)
    jieqi_code0 =  jieqicode_jq(new_jq2)
    kooks1 =  {"上元":jieqi_code1[0],
                  "中元":jieqi_code1[1],
                  "下元":jieqi_code1[2]}.get(three_yuen)
    kooks2 =  {"上元":jieqi_code2[0],
                  "中元":jieqi_code2[1],
                  "下元":jieqi_code2[2]}.get(three_yuen)
    kooks3 =  {"上元":jieqi_code0[0],
                  "中元":jieqi_code0[1],
                  "下元":jieqi_code0[2]}.get(three_yuen)
    lr = lunar_date_d(year, month, day)
    return {"日期時間":"{}年{}月{}日{}時{}分".format(year, month, day, hour, minute),
            "農曆": lr,
            "節氣":Jieqi, 
            "距節氣差日數":difference, 
            "三元":three_yuen, 
            "當前節氣日期":Jieqi_disance,
            "值符天干":zftg,
            "節氣排局":jieqi_code2,
            "陰陽局": yin_yang,
            "當前排局":"{}{}局".format(yin_yang, kooks2),
            "超神接氣正授排局":"{}{}局".format(multi_key_dict_get(yy,new_jq), kooks1),
            "其他排局":"{}{}局".format(yin_yang, kooks3),
            "其他排局1":"{}{}局".format(multi_key_dict_get(yy,new_jq), kooks),
            }

#奇門排局置閏，正授，有超神，有閏奇，有接氣
def qimen_ju_name_zhirun(year, month, day, hour, minute):
    qdict = qimen_ju_name_zhirun_raw(year, month, day, hour, minute)
    jQ = qdict.get("節氣")
    d = qdict.get("距節氣差日數")
    tgft = qimen_ju_name_zhirun_raw(year, month, day, hour, minute).get("值符天干")
    if d > 6  and d <=9  and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月")<= 6 and lunar_date_d(year, month, day).get("農曆月") != "正月" and  tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d > 6 and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("日") > 20 and lunar_date_d(year, month, day).get("月") < 7 and lunar_date_d(year, month, day).get("農曆月") != "正月" and  tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d > 6 and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("日") > 10 and lunar_date_d(year, month, day).get("月") < 7 and lunar_date_d(year, month, day).get("農曆月") != "正月" and  tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >= 7 and lunar_date_d(year, month, day).get("農曆月") != "正月" and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >=6 and lunar_date_d(year, month, day).get("農曆月") == "正月" :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") == "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月":
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") == "冬月"  and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft != "己" and tgft != "戊" and tgft != "庚" and tgft != "壬" and tgft != "癸":
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 20 :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d > 6  and d <=9 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 10 :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    
    #若距節氣差日數等於0或9天
    if d == 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") > 9:
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d == 0 and lunar_date_d(year, month, day).get("農曆月") == "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月":
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d == 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月":
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    #若距節氣差日數介於10至15天
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") > 9:
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") != "正月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") != "正月"  and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 15 :
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月"  and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 15 :
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") == "腊月"  and lunar_date_d(year, month, day).get("農曆月") != "冬月" and jQ == "冬至":
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") == "腊月"  and lunar_date_d(year, month, day).get("農曆月") != "冬月" and jQ != "冬至":
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d >= 10 and d <= 12 and lunar_date_d(year, month, day).get("農曆月") != "腊月"  and lunar_date_d(year, month, day).get("農曆月") == "冬月":
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d >= 12 and lunar_date_d(year, month, day).get("農曆月") != "腊月"  and lunar_date_d(year, month, day).get("農曆月") == "冬月":
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    #若距節氣差日數少或等於6天
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >= 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >= 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") < 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") < 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") != "正月"and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 10 and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 10 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") <= 9 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and tgft in list("戊己庚辛壬癸") and lunar_date_d(year, month, day).get("日") < 20:
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and tgft in list("戊己庚辛壬癸") and lunar_date_d(year, month, day).get("日") > 20 and lunar_date_d(year, month, day).get("日") <= 26:
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and tgft in list("戊己庚辛壬癸") and lunar_date_d(year, month, day).get("日") > 26:
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") == "冬月" and jQ == "冬至" and d <3:
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") == "冬月" and jQ == "冬至":
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") == "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
#奇門排局刻家
def qimen_ju_name_ke(year, month, day, hour, minute):
    hgz = gangzhi(year, month, day, hour, minute)[3]
    find_yingyang = multi_key_dict_get({tuple(list('子丑寅卯辰巳')):"陽遁",
                                        tuple(list('午未申酉戌亥')):"陰遁" },
                                       hgz[1])

    qu = {"陽遁":multi_key_dict_get({tuple(new_list(jieqi_name,"冬至")[0:12]):"一七四",
                             tuple(new_list(jieqi_name,"夏至")[0:12]):"一七四"},
                            jq(year,month, day,hour, minute)),
          "陰遁":multi_key_dict_get({tuple(new_list(jieqi_name,"冬至")[0:12]):"九三六",
                                   tuple(new_list(jieqi_name,"夏至")[0:12]):"九三六"},
                                  jq(year,month, day,hour, minute))}.get(find_yingyang)
    find_yuen = findyuen_minute(year, month, day, hour, minute)
    return "{}{}局{}".format(find_yingyang, qu[dict(zip(["上元","中元","下元"],
                                                       [0,1,2])).get(find_yuen)],
                                                        find_yuen)
def getgtw():
    gtw = re.findall("..","地籥六賊五符天曹地符風伯雷公雨師風雲唐符國印天關")
    gg = re.findall("..","地籥天關唐符風雲唐符風雲雷公風伯天曹五符")
    newmap = list(map(lambda i: new_list(gtw, i),gg))
    newgtw_list = list(map(lambda y: dict(zip(di_zhi,y)),newmap))
    return dict(zip(tian_gan, newgtw_list))

def pan_earth_minute(year, month, day, hour, minute):
    """刻家奇門地盤設置"""
    ke = qimen_ju_name_ke(year,
                                 month,
                                 day,
                                 hour,
                                 minute)
    return dict(zip(list(map(lambda x: dict(zip(cnumber, eight_gua)).get(x),
                    new_list(cnumber, ke[2]))),
                    {"陽遁":list("戊己庚辛壬癸丁丙乙"),
                     "陰遁":list("戊乙丙丁癸壬辛庚己")}.get(ke[0:2])))

def pan_sky_minute(year, month, day, hour, minute ):
    """刻家奇門天盤設置"""
    ke = qimen_ju_name_ke(year,
                                 month,
                                 day,
                                 hour,
                                 minute)
    gz = gangzhi(year, month, day, hour, minute)
    eg = list("坎巽兌離乾震坤中艮")
    another_eg = list("巽震坤坎離艮兌乾中")
    tg = list("乙丙丁戊己庚辛壬癸")
    another_tg = list("乙丙丁癸壬辛庚己戊")
    zf = zhifu_n_zhishi_ke(year, month, day, hour, minute).get('值符星宮')[1]
    zs = zhifu_n_zhishi_ke(year, month, day, hour, minute).get('值使門宮')[1]
    zftg = jj.get(multi_key_dict_get(liujiashun_dict(), gz[4]))
    if zs != "中" and zf != "中":
        return  {"陽":dict(zip(new_list(eg, zf), new_list(tg, zftg))), "陰":dict(zip(list((new_list(another_eg, zf))), new_list(another_tg, zftg)))}.get(ke[0])
    if zs == "中" and zf != "中":
        return {"陽":dict(zip(new_list(another_eg, zf), new_list(tg, zftg))), "陰":dict(zip(new_list(another_eg, zf), list(reversed(new_list(tg, zftg)))))}.get(ke[0])
    if zs == "中" and zf == "中":
        return {"陽":dict(zip(new_list(eg, zf), new_list(tg, zftg))), "陰":dict(zip(new_list(eg, zf), list(reversed(new_list(tg, zftg)))))}.get(ke[0])
    if zs != "中" and zf == "中":
        return pan_earth_minute(year, month, day, hour, minute)
    
def pan_earth_min_r(year, month, day, hour, minute):
    """刻家奇門地盤(逆)設置"""
    pan_earth_v = list(pan_earth_minute(year, month, day, hour, minute).values())
    pan_earth_k = list(pan_earth_minute(year, month, day, hour, minute).keys())
    return dict(zip(pan_earth_v, pan_earth_k))
 
#排值符
def zhifu_pai(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    yinyang = qmju[0]
    kook =  qmju[2]
    pai = {"陽":{"一":"九八七一二三四五六",
                "二":"一九八二三四五六七",
                "三":"二一九三四五六七八",
                "四":"三二一四五六七八九",
                "五":"四三二五六七八九一",
                "六":"五四三六七八九一二",
                "七":"六五四七八九一二三",
                "八":"七六五八九一二三四",
                "九":"八七六九一二三四五"},
           "陰":{"九":"一二三九八七六五四",
                "八":"九一二八七六五四三",
                "七":"八九一七六五四三二",
                "六":"七八九六五四三二一",
                "五":"六七八五四三二一九",
                "四":"五六七四三二一九八",
                "三":"四五六三二一九八七",
                "二":"三四五二一九八七六",
                "一":"二三四一九八七六五"}}.get(yinyang).get(kook)
    yinlist = list(map(lambda x: x+pai, new_list_r(cnumber, kook)[0:6]))
    yanglist = list(map(lambda x: x+pai, new_list(cnumber, kook)[0:6]))
    return {"陰":dict(zip(jiazi()[0::10], yinlist)),
            "陽":dict(zip(jiazi()[0::10], yanglist))}.get(yinyang)

def zhifu_pai_ke(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    yinyang = qmju[0]
    kook =  qmju[2]
    pai = {"陽":{"一":"九八七一二三四五六",
                 "二":"一九八二三四五六七",
                 "三":"二一九三四五六七八",
                 "四":"三二一四五六七八九",
                 "五":"四三二五六七八九一",
                 "六":"五四三六七八九一二",
                 "七":"六五四七八九一二三",
                 "八":"七六五八九一二三四",
                 "九":"八七六九一二三四五"},
           "陰":{"九":"一二三九八七六五四",
                 "八":"九一二八七六五四三",
                 "七":"八九一七六五四三二",
                 "六":"七八九六五四三二一",
                 "五":"六七八五四三二一九",
                 "四":"五六七四三二一九八",
                 "三":"四五六三二一九八七",
                 "二":"三四五二一九八七六",
                 "一":"二三四一九八七六五"}}.get(yinyang).get(kook)
    new_kook = new_list(cnumber, kook)
    new_rkook = new_list_r(cnumber, kook)
    yinlist = list(map(lambda x: x+pai, new_rkook[0:6]))
    yanglist = list(map(lambda x: x+pai, new_kook[0:6]))
    return {"陰":dict(zip(jiazi()[0::10], yinlist)),
            "陽":dict(zip(jiazi()[0::10], yanglist))}.get(yinyang)
#1拆補 #2置閏
def zhishi_pai(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    yinyang = qmju[0]
    kook =  qmju[2]
    new_kook = new_list(cnumber, kook)
    new_rkook = new_list_r(cnumber, kook)
    yanglist = "".join(new_kook)+"".join(new_kook)+"".join(new_kook)
    yinlist =  "".join(new_rkook)+"".join(new_rkook)+"".join(new_rkook)
    yinlist1 = list(map(lambda i:i+yinlist[yinlist.index(i)+1:][0:11],new_rkook[0:6]))
    yanglist1 = list(map(lambda i:i+yanglist[yanglist.index(i)+1:][0:11],new_kook[0:6]))
    return {"陰":dict(zip(jiazi()[0::10], yinlist1)),
            "陽":dict(zip(jiazi()[0::10], yanglist1))}.get(yinyang)

def zhishi_pai_ke(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    yinyang = qmju[0]
    kook = qmju[2]
    new_kook = new_list(cnumber, kook)
    new_rkook = new_list_r(cnumber, kook)
    yanglist = "".join(new_kook)+"".join(new_kook)+"".join(new_kook)
    yinlist =  "".join(new_rkook)+"".join(new_rkook)+"".join(new_rkook)
    yinlist1 = list(map(lambda i:i+ yinlist[yinlist.index(i)+1:][0:11],new_rkook[0:6]))
    yanglist1 = list(map(lambda i:i+ yanglist[yanglist.index(i)+1:][0:11],new_kook[0:6]))
    return {"陰":dict(zip(jiazi()[0::10], yinlist1)),
            "陽":dict(zip(jiazi()[0::10], yanglist1))}.get(yinyang)
#八門
def pan_door(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    zfnzs = zhifu_n_zhishi(year, month, day, hour, minute, option)
    starting_door = zfnzs.get("值使門宮")[0]
    starting_gong = zfnzs.get("值使門宮")[1]
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qmju[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    yydoor = {"陽":new_list(door_r, starting_door),
              "陰":new_list(list(reversed(door_r)), starting_door)}
    return dict(zip(gong_reorder,yydoor.get(qmju[0])))

def pan_door_minute(year, month, day, hour, minute, option):
    qimen_ke = qimen_ju_name_ke(year, month, day, hour, minute)
    zhifu_n_zhishike = zhifu_n_zhishi_ke(year, month, day, hour, minute)
    starting_door = zhifu_n_zhishike.get("值使門宮")[0]
    starting_gong = zhifu_n_zhishike.get("值使門宮")[1]
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qimen_ke[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    yydict = {"陽":new_list(door_r, starting_door),
              "陰":new_list(list(reversed(door_r)), starting_door)}
    return dict(zip(gong_reorder,yydict.get(qimen_ke[0])))
#九星
def pan_star(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    zhifunzhishi = zhifu_n_zhishi(year, month, day, hour, minute, option)
    star_r = list("蓬任沖輔英禽柱心")
    starting_star = zhifunzhishi.get("值符星宮")[0].replace("芮", "禽")
    starting_gong = zhifunzhishi.get("值符星宮")[1]
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qmju[0])
    star_reorder = {"陽":new_list(star_r, starting_star),
                    "陰":new_list(list(reversed(star_r)), starting_star)}.get(qmju[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,star_reorder)), dict(zip(star_reorder, gong_reorder))

def pan_star_minute(year, month, day, hour, minute, option):
    star_r = list("蓬任沖輔英禽柱心")
    zhifu_n_zhishi = zhifu_n_zhishi_ke(year, month, day, hour, minute)
    qimen_ke = qimen_ju_name_ke(year, month, day, hour, minute)
    starting_star = zhifu_n_zhishi.get("值符星宮")[0].replace("芮", "禽")
    starting_gong = zhifu_n_zhishi.get("值符星宮")[1]
    qmke = qimen_ju_name_ke(year, month, day, hour, minute)
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qimen_ke[0])
    star_reorder = {"陽":new_list(star_r, starting_star),
                    "陰":new_list(list(reversed(star_r)),starting_star)}.get(qmke[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,star_reorder)), dict(zip(star_reorder, gong_reorder))
#八神
def pan_god(year, month, day, hour, minute, option):
    qmju = {1:qimen_ju_name_chaibu(year, month, day, hour, minute),
            2:qimen_ju_name_zhirun(year, month, day, hour, minute)}.get(option)
    zfzs = zhifu_n_zhishi(year, month, day, hour, minute, option)
    starting_gong = zfzs.get("值符星宮")[1]
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qmju[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,{"陽":list("符蛇陰合勾雀地天"),
                                  "陰":list("符蛇陰合虎玄地天")}.get(qmju[0])))

def pan_god_minute(year, month, day, hour, minute, option):
    zfzs = zhifu_n_zhishi_ke(year, month, day, hour, minute)
    starting_gong = zfzs.get("值符星宮")[1]
    qmke = qimen_ju_name_ke(year, month, day, hour, minute)
    rotate = {"陽":clockwise_eightgua,
              "陰":list(reversed(clockwise_eightgua))}.get(qmke[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,{"陽":list("符蛇陰合勾雀地天"),
                                  "陰":list("符蛇陰合虎玄地天")}.get(qmke[0])))

#找值符及值使
def zhifu_n_zhishi(year, month, day, hour, minute, option):
    gongs_code = dict(zip(cnumber, eight_gua))
    gz = gangzhi(year, month, day, hour, minute)
    hgan = dict(zip(tian_gan,range(0,11))).get(gz[3][0])
    chour = multi_key_dict_get(liujiashun_dict(), gz[3])
    eg = list("休死傷杜中開驚生景")
    eight_gods = list("蓬芮沖輔禽心柱任英")
    zspai_keys = list(zhishi_pai(year, month, day, hour, minute, option).keys())
    zspai_values = list(zhishi_pai(year, month, day, hour, minute, option).values())
    zf_keys = list(zhifu_pai(year, month, day, hour, minute, option).keys())
    zf_values = list(zhifu_pai(year, month, day, hour, minute, option).values())
    a = list(map(lambda i: dict(zip(cnumber, eg)).get(i[0]), zspai_values))
    b = list(map(lambda i:dict(zip(cnumber, eight_gods)).get(i[0]) , zf_values))
    c = list(map(lambda i:gongs_code.get(i[hgan]), zf_values))
    d = list(map(lambda i:gongs_code.get(i[hgan]), zspai_values))
    door = dict(zip(zspai_keys, a)).get(chour)
    if door == "中":
        door = "死"
    return {"值符天干": [chour, jj.get(chour)],
            "值符星宮":[dict(zip(zf_keys, b)).get(chour),dict(zip(zf_keys, c)).get(chour)], 
            "值使門宮":[door,dict(zip(zspai_keys,d)).get(chour)]}

def zhifu_tiangan(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    jj = {"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}
    chour = multi_key_dict_get(liujiashun_dict(), gz[3])
    return jj.get(chour)

def zhifu_n_zhishi_ke(year, month, day, hour, minute):
    gz = gangzhi(year, month, day, hour, minute)
    qmke = qimen_ju_name_ke(year, month, day, hour, minute)
    chour = multi_key_dict_get(liujiashun_dict(),gz[4])
    #chour2 = multi_key_dict_get(liujiashun_dict(),gz[3])
    ep = pan_earth_min_r(year, month, day, hour, minute)
    zftg =  {"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}.get(multi_key_dict_get(liujiashun_dict(), gz[4]))
    kook = re.findall("..", "陽一陽四陽七陰九陰六陰三")
    liujia = re.findall("..", "甲子甲戌甲申甲午甲辰甲寅")
    stars = [list("蓬芮沖輔禽心"), list("輔禽心柱任英"), list("柱任英蓬芮沖"), list("英任柱心禽輔"), list("心禽輔沖芮蓬"), list("沖芮蓬英任柱")]
    doors = [re.findall("..", "休坎死坤傷震杜巽死中開乾"),
            re.findall("..", "杜巽死中開乾驚兌生艮景離"),
            re.findall("..", "驚兌生艮景離休坎死坤傷震"),
            re.findall("..", "景離生艮驚兌開乾死中杜巽"),
            re.findall("..", "開乾死中杜巽傷震死坤休坎"),
            re.findall("..", "傷震死坤休坎景離生艮驚兌")]
    stars_zhifu = {kook[i]: {liujia[j]: stars[i][j] for j in range(len(liujia))} for i in range(len(kook))}.get("{}{}".format(qmke[0], qmke[2])).get(chour)
    shi_door = {kook[i]: {liujia[j]:doors[i][j] for j in range(len(liujia))} for i in range(len(kook))}.get("{}{}".format(qmke[0], qmke[2])).get(chour)[0]
    shi_door_head = {kook[i]: {liujia[j]:doors[i][j] for j in range(len(liujia))} for i in range(len(kook))}.get("{}{}".format(qmke[0], qmke[2])).get(chour)[1]
    fiftheen_ke_gz = new_list(jiazi(), chour)[0:16]
    door_order ={"陽":new_list(eight_gua, shi_door_head), "陰": new_list(list(reversed(eight_gua)), shi_door_head)}.get(qmke[0])
    fu = ep.get(gz[4][0])
    if fu == None:
        fu = ep.get(zftg)
    zhifu_star = [stars_zhifu, fu]
    zhifu_door = [shi_door,dict(zip(fiftheen_ke_gz, cycle(door_order))).get(gz[4])]
    return {"值符天干":zftg, "值符星宮":zhifu_star, "值使門宮":zhifu_door}

def gong_wangzhuai():
    wangzhuai = list("旺相胎沒死囚休廢")
    wangzhuai_num = [3,4,9,2,7,6,1,8]
    wangzhuai_jieqi = {('春分','清明','穀雨'):'春分',
                        ('立夏','小滿','芒種'):'立夏',
                        ('夏至','小暑','大暑'):'夏至',
                        ('立秋','處暑','白露'):'立秋',
                        ('秋分','寒露','霜降'):'秋分',
                        ('立冬','小雪','大雪'):'立冬',
                        ('冬至','小寒','大寒'):'冬至',
                        ('立春','雨水','驚蟄'):'立春'}
    wzhuai = multi_key_dict_get(wangzhuai_jieqi, "霜降")
    wz = dict(zip(jieqi_name[0::3],wangzhuai_num)).get(wzhuai)
    new_dict = new_list(wangzhuai_num, wz)
    return dict(zip(new_dict, wangzhuai))

def ecliptic_lon(jd_utc):
    s=ephem.Sun(jd_utc)
    equ=ephem.Equatorial(s.ra,s.dec,epoch=jd_utc)
    e=ephem.Ecliptic(equ)
    return e.lon

def sta(jd):
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)
    return n

def iteration(jd,sta):
    s1=sta(jd)
    s0=s1
    dt=1.0
    while True:
        jd+=dt
        s=sta(jd)
        if s0!=s:
            s0=s
            dt=-dt/2
        if abs(dt)<0.0000001 and s!=s1:
            break
    return jd

def change(year, month, day, hour, minute):
    changets = ephem.Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4),
                                               str(month).zfill(2),
                                               str(day).zfill(2),
                                               str(hour).zfill(2),
                                               str(minute).zfill(2)))
    return ephem.Date(changets - 24 * ephem.hour *30)

def jq(year, month, day, hour, minute):
    current = ephem.Date("{}/{}/{} {}:{}:00".format(str(year).zfill(4),
                                              str(month).zfill(2),
                                              str(day).zfill(2),
                                              str(hour).zfill(2),
                                              str(minute).zfill(2)))
    jd = change(year, month, day, hour, minute)
    result = []
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1
    for i in range(3):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=ephem.Date(jd+1/3).tuple()
        dt = ephem.Date("{}/{}/{} {}:{}:00.00".format(d[0],
                                                d[1],
                                                d[2],
                                                d[3],
                                                d[4]).split(".")[0])
        time_info = {dt:jieqi_name[n]}
        n+=1
        result.append(time_info)
    j = [list(i.keys())[0] for i in result]
    if current > j[0] and current > j[1] and current > j[2]:
        return list(result[2].values())[0]
    if current > j[0] and current > j[1] and current <= j[2]:
        return list(result[1].values())[0]
    if current >= j[1] and current < j[2]:
        return list(result[1].values())[0]
    if current < j[1] and current < j[2]:
        return list(result[0].values())[0]

def jq_distance(year, month, day, hour, minute):
    current = "{}/{}/{} {}:{}:00".format(str(year).zfill(4),
                                         str(month).zfill(2),
                                         str(day).zfill(2),str(hour).zfill(2),
                                         str(minute).zfill(2))
    jd = change(year, month, day, hour, minute)
    result = {}
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1
    for i in range(12):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=ephem.Date(jd+1/3).tuple()
        dt = "{}/{}/{} {}:{}:00.00".format(d[0],d[1],d[2],
                                           str(d[3]).zfill(2),
                                           str(d[4]).zfill(2)).split(".")[0]
        time_info = {jieqi_name[n]:dt}
        n+=1
        result.update(time_info)
    return result, current


if __name__ == '__main__':
    year = 2024
    month = 8
    day = 25
    hour = 17
    minute = 50
    print(qimen_ju_name_zhirun_raw(year, month, day, hour, minute))
    print(qimen_ju_name_zhirun(year, month, day, hour, minute))
    #print(qimen_ju_name_zhirun(year, month, day, hour, minute))
    #print(gangzhi(year, month, day, hour, minute))
    #print(pan_door_minute(year, month, day, hour, minute, 2))
    #print(qimen_ju_name_ke(year, month, day, hour, minute))
    #print(zhifu_n_zhishi_ke(year, month, day, hour, minute))
    #print(pan_sky_minute(year, month, day, hour, minute))
    #print(zhifu_n_zhishi(year, month, day, hour, minute, 1))
    #print(zhifu_n_zhishi(year, month, day, hour, minute, 2))
    #print(zhifu_pai(year, month, day, hour, minute, 1))
    #print(zhifu_pai(year, month, day, hour, minute, 2))
