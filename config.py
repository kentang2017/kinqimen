# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:55:49 2023

@author: kentang
"""

import re
import math
import datetime
from itertools import cycle, repeat
import  sxtwl
from sxtwl import fromSolar
import swisseph as swe
import ephem

cnum = list("一二三四五六七八九十")
#干支
tian_gan = '甲乙丙丁戊己庚辛壬癸'
di_zhi = '子丑寅卯辰巳午未申酉戌亥'
cnumber = list("一二三四五六七八九")
door_r = list("休生傷杜景死驚開")
star_r = list("蓬任沖輔英禽柱心")
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
door_wuxing = dict(zip(door_r,"水土木木火土金金"))
star_wuxing = dict(zip(star_r,"水土木木火土金金"))
jqmc = ['小寒', '大寒', '立春', '雨水', '驚蟄', '春分', '清明', '穀雨', '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']

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
    return list(map(lambda x: "{}{}".format(tian_gan[x % len(tian_gan)],di_zhi[x % len(di_zhi)]),list(range(60))))

def Ganzhiwuxing(gangorzhi):
    gz_list = "甲寅乙卯震巽,丙巳丁午離,壬亥癸子坎,庚申辛酉乾兌,未丑戊己未辰戌艮坤".split(",")
    ganzhiwuxing = dict(zip(list(map(lambda x: tuple(x), gz_list
                                     )), list("木火水金土")))
    return multi_key_dict_get(ganzhiwuxing, gangorzhi)

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
    return dict(zip(nlist, ["上","中","下"]*4))

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
    j_q = jq(year, month, day, hour, minute)
    jieqi_code = jieqicode_jq(j_q)
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
    jieqi_code = jieqicode_jq(Jieqi)
    #hgz = gangzhi(year, month, day, hour, minute)[3][0]
    dgz = gangzhi(year, month, day, hour, minute)[2]
    fd = multi_key_dict_get(fuhead, dgz)
    zftg = zhifu_tiangan(year, month, day, hour, minute)
    ju_day_dict = {tuple(["甲子","甲午","己卯","己酉"]):"上元",
                   tuple(["甲寅","甲申","己巳","己亥"]):"中元",
                   tuple(["甲辰","甲戌","己丑","己未"]):"下元"}
    three_yuen = multi_key_dict_get(ju_day_dict, fd)
    Jieqi_disance = get_jieqi_start_date(year, month, day, hour, minute)["時間"]
    current = datetime.datetime(year, month, day, hour, minute)
    #current_ts = datetime.datetime.strptime(current, "%Y/%m/%d %H:%M:%S")
    #jq_distance_ts = datetime.datetime.strptime(Jieqi_disance,"%Y/%m/%d %H:%M:%S")
    difference = (current-Jieqi_disance).days
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


#%% 節氣計算
def get_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the current solar term (jieqi) for the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Check if the given date has a solar term
    if day.hasJieQi():
        jq_index = day.getJieQi()
        jd = day.getJieQiJD()
        t = sxtwl.JD2DD(jd)
        return {
            "年": t.Y,
            "月": t.M,
            "日": t.D,
            "時": int(t.h),
            "分": round(t.m),
            "節氣": jqmc[jq_index-1],
            "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
        }
    else:
        # If no solar term on this day, find the previous solar term
        current_day = day
        while True:
            current_day = current_day.before(1)
            if current_day.hasJieQi():
                jq_index = current_day.getJieQi()
                jd = current_day.getJieQiJD()
                t = sxtwl.JD2DD(jd)
                return {
                    "年": t.Y,
                    "月": t.M,
                    "日": t.D,
                    "時": int(t.h),
                    "分": round(t.m),
                    "節氣": jqmc[jq_index-1],
                    "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
                }
            
def get_before_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the next solar term (jieqi) after the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Start searching from the next day
    current_day = day.before(15)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y,
                "月": t.M,
                "日": t.D,
                "時": int(t.h),
                "分": round(t.m),
                "節氣": jqmc[jq_index-1],
                "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.before(1)

def get_next_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the next solar term (jieqi) after the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Start searching from the next day
    current_day = day.after(1)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y,
                "月": t.M,
                "日": t.D,
                "時": int(t.h),
                "分": round(t.m),
                "節氣": jqmc[jq_index-1],
                "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.after(1)


#%% 節氣計算
def jq(year, month, day, hour, minute):
    """
    Get the current solar term (jieqi) for the given date and time.
    Returns the name of the solar term as a string.
    """
    try:
        current_datetime = datetime.datetime(year, month, day, hour, minute)
        jq_start_dict = get_jieqi_start_date(year, month, day, hour, minute)
        next_jq_start_dict = get_next_jieqi_start_date(year, month, day, hour, minute)
        
        if not (isinstance(jq_start_dict, dict) and isinstance(next_jq_start_dict, dict) and 
                "時間" in jq_start_dict and "時間" in next_jq_start_dict and
                "節氣" in jq_start_dict and "節氣" in next_jq_start_dict):
            raise ValueError(f"Invalid jieqi dictionary format for {year}-{month}-{day} {hour}:{minute}")
        
        jq_start_datetime = jq_start_dict["時間"]
        next_jq_start_datetime = next_jq_start_dict["時間"]
        jq_name = jq_start_dict["節氣"]
        
        if not (isinstance(jq_start_datetime, datetime.datetime) and isinstance(next_jq_start_datetime, datetime.datetime)):
            raise ValueError(f"Jieqi times are not datetime objects: {jq_start_datetime}, {next_jq_start_datetime}")
        
        # Check if current_datetime is within the current jieqi period
        if jq_start_datetime <= current_datetime < next_jq_start_datetime:
            return jq_name
        # If before the current jieqi start, get the previous jieqi
        elif current_datetime < jq_start_datetime:
            prev_jq_start_dict = get_before_jieqi_start_date(year, month, day, hour, minute)
            if not (isinstance(prev_jq_start_dict, dict) and "節氣" in prev_jq_start_dict):
                raise ValueError(f"Invalid previous jieqi dictionary format for {year}-{month}-{day}")
            return prev_jq_start_dict["節氣"]
        else:
            raise ValueError(f"Current datetime {current_datetime} not within any valid jieqi period")
    except Exception as e:
        raise ValueError(f"Error in jq for {year}-{month}-{day} {hour}:{minute}: {str(e)}")

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
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    #若距節氣差日數介於10至15天
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") > 9:
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") != "正月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") == "正月" and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") < 15 :
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d >= 10 and d <= 15 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("農曆月") != "正月"  and lunar_date_d(year, month, day).get("月") <= 9 and lunar_date_d(year, month, day).get("日") >= 15 :
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
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
        return "{}{}".format(qdict.get('當前排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") >= 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") < 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and lunar_date_d(year, month, day).get("月") < 9 and lunar_date_d(year, month, day).get("日") >= 15 and tgft not in list("戊己庚辛壬癸"):
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
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
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") != "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" and jQ != "冬至":
        return "{}{}".format(qdict.get('其他排局'), qdict.get('三元'))
    if d <= 6 and d != 0 and lunar_date_d(year, month, day).get("農曆月") == "腊月" and lunar_date_d(year, month, day).get("農曆月") != "冬月" :
        return "{}{}".format(qdict.get('其他排局1'), qdict.get('三元'))
    else:
        return "{}{}".format(qdict.get('超神接氣正授排局'), qdict.get('三元'))
        
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
    return "{}{}局{}元".format(find_yingyang, qu[dict(zip(["上","中","下"],
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



#刻家奇門 五行旺衰
def wuxing_strong_week_minute(jq):
    j = new_list(jieqi_name, "小寒")
    sw = list("旺相休囚死")
    fs_order = ["土金火木水",
                "土金火木水",
                "木火水金土",
                "木火水金土",
                "木火水金土",
                "木火水金土",
                "土金火木水",
                "土金火木水",
                "火土木水金",
                "火土木水金",
                "火土木水金",
                "火土木水金",
                "土金火木水",
                "土金火木水",
                "金水土火木",
                "金水土火木",
                "金水土火木",
                "金水土火木",
                "土金火木水",
                "土金火木水",
                "水木金土火",
                "水木金土火",
                "水木金土火",
                "水木金土火"]
    fs_list = [dict(zip(i,sw)) for i in fs_order]
    return dict(zip(j, fs_list)).get(jq)
#五行旺衰
def wuxing_strong_week(jq):
    season = find_season(jq)
    sw = list("旺相休囚死")
    fs = list("春夏秋冬")
    fs_order = ["木火水金土",
                "火土木水金",
                "金水土火木",
                "水木金土火"]
    fs_list = [dict(zip(i,sw)) for i in fs_order]
    return dict(zip(fs, fs_list)).get(season)


def pan_sky_minute(year, month, day, hour, minute ):
    kgz = gangzhi(year, month, day, hour, minute)[4]
    """刻家奇門天盤設置"""
    zfzs = zhifu_n_zhishi_ke(year, month, day, hour, minute)
    zftg = zfzs.get("值符天干")
    zfgong = zfzs.get("值符星宮")[1]
    eg = list("坎坤震巽乾兌艮離")
    kook_setting = [tuple(["陰三","陽七"]),tuple(["陽四","陰六"]), tuple(["陰九","陽一"])]
    skypan_orders = [[
    list("戊丁辛己丙壬庚乙癸"),
    list("己戊丁庚丙辛乙癸壬"),
    list("庚己戊乙丙丁癸壬辛"),
    list("丁辛壬戊丙癸己庚乙"),
    list("乙庚己癸丙戊壬辛丁"),
    list("辛壬癸丁丙乙戊己庚"),
    list("壬癸乙辛丙庚丁戊己"),
    list("癸乙庚壬丙己辛丁戊")
    ],[
    list("戊丁丙辛己乙壬癸庚"),
    list("辛戊丁壬己丙癸庚乙"),
    list("壬辛戊癸己丁庚乙丙"),
    list("丁丙乙戊己庚辛壬癸"),
    list("癸壬辛庚己戊乙丙丁"),
    list("丙乙庚丁己癸戊辛壬"),
    list("乙庚癸丙己壬丁戊辛"),
    list("庚癸壬乙己辛丙丁戊")
    ],[
    list("乙丙丁癸壬辛庚己戊"),
    list("辛戊己丁壬庚丙乙癸"),
    list("丁辛戊丙壬己乙癸庚"),
    list("己庚癸戊壬乙辛丁丙"),
    list("丙丁辛乙壬戊癸庚己"),
    list("庚癸乙己壬丙戊辛丁"),
    list("癸乙丙庚壬丁己戊辛"),
    list("乙丙丁癸壬辛庚己戊"),
    ]]
    sky_pan_orders = dict(zip(kook_setting, skypan_orders))
    liujia = list("戊己庚辛壬癸")
    orders = [[[0,1,2,3,1,4,5,6,7],[1,2,4,0,2,7,3,5,6],[2,4,7,1,4,6,0,3,5],[5,3,0,6,3,1,7,4,2],[6,5,3,7,5,0,4,2,1],[7,6,5,4,6,3,2,1,0]],
              [[0,1,2,3,1,4,5,6,7],[5,3,0,6,3,1,7,4,2],[7,6,5,4,6,3,2,1,0],[1,2,4,0,2,7,3,5,6],[2,4,7,1,4,6,0,3,5],[4,7,6,2,7,5,1,0,3]],
              [[0,1,2,3,1,4,5,6,7],[3,0,1,5,0,2,6,7,4],[5,3,0,6,3,1,7,4,2],[1,2,4,0,2,7,3,5,6],[3,0,1,5,0,2,6,7,4],[6,5,3,7,5,0,4,2,1]]]
    get_zf_orders = dict(zip(kook_setting, orders))
    ke = qimen_ju_name_ke(year, month, day, hour, minute)
    kook = "{}{}".format(ke[0],ke[2])
    kook1 = kook + kgz
    getzf_orders = multi_key_dict_get(get_zf_orders, kook)
    get_humhead = dict(zip(liujia, getzf_orders)).get(zftg)
    #坎坤震巽中乾兌艮離
    if kook1 in "陰三辛未,陰三丁丑,陰三戊子,陰三癸卯,陰三乙巳,陰三庚申".split(","):
        return dict(zip(eight_gua,list("癸乙庚壬丙己辛丁戊")))
    if kook1 in "陰三庚午,陰三乙亥,陰三癸巳,陰三戊戌,陰三丁未,陰三辛酉".split(","):
        return dict(zip(eight_gua,list("戊丁辛己丙壬庚乙癸")))
    if kook1 in "陰三丁卯,陰三戊寅,陰三丙戌,陰三己丑,陰三壬寅,陰三癸丑,陰三乙卯".split(","):
        return dict(zip(eight_gua,list("乙庚己癸丙戊壬辛丁")))
    if kook1 in "陰三壬申,陰三辛巳,陰三丁亥,陰三乙未,陰三庚戌,陰三丙辰,陰三己未".split(","):
        return dict(zip(eight_gua,list("壬癸乙辛丙庚丁戊己")))
    if kook1 in "陰三乙丑,陰三癸未,陰三壬辰,陰三丙申,陰三己亥,陰三戊申,陰三丁巳".split(","):
        return dict(zip(eight_gua,list("丁辛壬戊丙癸己庚乙")))
    if kook1 in "陰三丙寅,陰三己巳,陰三庚辰,陰三乙酉,陰三丁酉,陰三辛亥,陰三壬戌".split(","):
        return dict(zip(eight_gua,list("己戊丁庚丙辛乙癸壬")))
    if kook1 in "陰三癸酉,陰三壬午,陰三辛卯,陰三庚子,陰三丙午,陰三己酉,陰三戊午".split(","):
        return dict(zip(eight_gua,list("辛壬癸丁丙乙戊己庚")))
    if kook1 in "陰三甲子,陰三戊辰,陰三甲戌,陰三丙子,陰三己卯,陰三甲申,陰三庚寅,陰三甲午,陰三辛丑,陰三甲辰,陰三壬子,陰三甲寅,陰三癸亥".split(","):
        return dict(zip(eight_gua,list("庚己戊乙丙丁癸壬辛")))
    if kook1 in "陰六甲子,陰六戊辰,陰六甲戌,陰六己卯,陰六壬午,陰六甲申,陰六庚寅,陰六甲午,陰六辛丑,陰六甲辰,陰六己酉,陰六壬子,陰六甲寅,陰六癸亥".split(","):
        return dict(zip(eight_gua,list("癸壬辛庚己戊乙再丁")))
    if kook1 in "陰六辛未,陰六癸未,陰六乙酉,陰六己亥,陰六壬寅,陰六癸丑,陰六庚申".split(","):
        return dict(zip(eight_gua,list("壬辛戊癸己丁庚乙丙")))
    if kook1 in "陰六丙寅,陰六戊寅,陰六己丑,陰六壬辰,陰六丁酉,陰六戊申,陰六辛酉".split(","):
        return dict(zip(eight_gua,list("乙庚癸丙己壬丁戊辛")))
    if kook1 in "陰六乙丑,陰六丁丑,陰六辛卯,陰六丙申,陰六丁未,陰六戊午".split(","):
        return dict(zip(eight_gua,list("丙乙庚丁己癸戊辛壬")))
    if kook1 in "陰六庚午,陰六丙子,陰六戊子,陰六乙未,陰六丙午,陰六丁巳".split(","):
        return dict(zip(eight_gua,list("丁丙乙戊己庚辛壬癸")))
    if kook1 in "陰六丁卯,陰六辛巳,陰六癸巳,陰六戊戌,陰六辛亥,陰六己未,陰六壬戌".split(","):
        return dict(zip(eight_gua,list("庚癸壬乙己辛丙丁戊")))
    if kook1 in "陰六戊午,陰六己巳,陰六壬申,陰六庚辰,陰六丙戌,陰六癸卯,陰六庚戌,陰六乙卯".split(","):
        return dict(zip(eight_gua,list("辛戊丁壬己丙癸庚乙")))
    if kook1 in "陰六癸酉,陰六乙亥,陰六丁亥,陰六庚子,陰六乙巳,陰六丙辰".split(","):
        return dict(zip(eight_gua,list("戊丁丙辛己乙壬癸庚")))
    if kook1 in "陰九丁卯,陰九辛巳,陰九戊子,陰九丙申,陰九壬寅,陰九癸丑,陰九己未,陽一庚午,陽一癸未,陽一乙酉,陽一己亥,陽一壬寅,陽一癸丑,陽一丙辰".split(","):
        return dict(zip(eight_gua,list("丁辛戊丙壬己乙癸庚")))
    if kook1 in "陰九辛未,陰九戊寅,陰九己丑,陰九丁酉,陰九乙巳,陰九庚申,陽一癸酉,陽一乙亥,陽一丙戌,陽一庚子,陽一乙巳,陽一丁巳".split(","):
        return dict(zip(eight_gua,list("丙丁辛乙壬戊癸庚己")))
    if kook1 in "陰九甲子,陰九戊辰,陰九甲戌,陰九己卯,陰九甲申,陰九庚寅,陰九甲午,陰九辛丑,陰九甲辰,陰九丙午,陰九壬子,陰九甲寅,陰九癸亥".split(","):
        return dict(zip(eight_gua,list("乙庚丁癸壬辛庚己戊")))
    if kook1 in "陰九癸酉,陰九乙亥,陰九丙戌,陰九壬辰,陰九庚子,陰九戊申,陰九丁巳".split(","):
        return dict(zip(eight_gua,list("己庚癸戊壬乙辛丁丙")))
    if kook1 in "陰九丙寅,陰九壬申,陰九丁丑,陰九辛卯,陰九乙未,陰九庚戌,陰九戊午".split(","):
        return dict(zip(eight_gua,list("辛戊己丁壬庚丙乙癸")))
    if kook1 in "陰九庚午,陰九癸未,陰九乙酉,陰九己亥,陰九辛亥,陰九丙辰,陰九壬戌".split(","):
        return dict(zip(eight_gua,list("庚癸乙己壬丙戊辛丁")))
    if kook1 in "陰九乙丑,陰九丙子,陰九壬午,陰九丁亥,陰九癸卯,陰九己酉,陰九辛酉".split(","):
        return dict(zip(eight_gua,list("戊己庚辛壬癸丁丙乙")))
    if kook1 in "陰九己巳,陰九庚辰,陰九癸巳,陰九戊戌,陰九丁未,陰九乙卯".split(","):
        return dict(zip(eight_gua,list("癸乙丙庚壬丁己戊辛")))   
    if kook1 in "陽一乙丑,陽一丙子,陽一丁亥,陽一癸卯,陽一丙午,陽一辛酉".split(","):
        return dict(zip(eight_gua,list("乙丙丁癸壬辛庚己戊")))
    if kook1 in "陽一丙寅,陽一丁丑,陽一辛卯,陽一乙未,陽一丁未,陽一戊午".split(","):
        return dict(zip(eight_gua,list("癸乙丙庚壬丁己戊辛")))
    if kook1 in "陽一己巳,陽一壬申,陽一庚辰,陽一癸巳,陽一戊戌,陽一庚戌,陽一乙卯".split(","):
        return dict(zip(eight_gua,list("辛戊己丁壬庚丙乙癸")))
    if kook1 in "陽一辛未,陽一戊寅,陽一己丑,陽一壬辰,陽一丁酉,陽一戊申,陽一庚申".split(","):
        return dict(zip(eight_gua,list("己庚癸戊壬乙辛丁丙")))
    if kook1 in "陽一丁卯,陽一辛巳,陽一戊子,陽一丙申,陽一辛亥,陽一己未,陽一壬戌".split(","):
        return dict(zip(eight_gua,list("庚癸乙己壬丙戊辛丁")))
    if kook1 in "陽一甲子,陽一戊辰,陽一甲戌,陽一己卯,陽一壬午,陽一壬午,陽一甲申,陽一庚寅,陽一甲午,陽一辛丑,陽一甲辰,陽一己酉,陽一壬子,陽一甲寅,陽一癸亥".split(","):
        return dict(zip(eight_gua,list("戊己庚辛壬癸丁丙乙")))
    if kook1 in "陽七甲子,陽七戊辰,陽七甲戌,陽七己卯,陽七甲申,陽七庚寅,陽七甲午,陽七辛丑,陽七甲辰,陽七丙午,陽七壬子,陽七甲寅,陽七癸亥".split(","):
        return dict(zip(eight_gua,list("辛壬癸丁丙乙戊己庚")))
    if kook1 in "陽七乙丑,陽七癸未,陽七丙戌,陽七壬辰,陽七己亥,陽七戊申,陽七丁巳".split(","):
        return dict(zip(eight_gua,list("乙庚己癸丙戊壬辛丁")))
    if kook1 in "陽七丁卯,陽七戊寅,陽七己丑,陽七丙申,陽七壬寅,陽七癸丑,陽七乙卯".split(","):
        return dict(zip(eight_gua,list("丁辛壬戊丙癸己庚乙")))
    if kook1 in "陽七己巳,陽七庚辰,陽七乙酉,陽七丁酉,陽七辛亥,陽七丙辰,陽七壬戌".split(","):
        return dict(zip(eight_gua,list("壬癸乙辛丙庚丁戊己")))
    if kook1 in "陽七丙寅,陽七壬申,陽七辛巳,陽七丁亥,陽七乙未,陽七庚戌,陽七己未".split(","):
        return dict(zip(eight_gua,list("己戊丁庚丙辛乙癸壬")))
    if kook1 in "陽七癸酉,陽七丙子,陽七壬午,陽七辛卯,陽七庚子,陽七己酉,陽七戊午".split(","):
        return dict(zip(eight_gua,list("庚己戊乙丙丁癸壬辛")))
    if kook1 in "陽七辛未,陽七丁丑,陽七戊子,陽七癸卯,陽七乙巳,陽七庚申".split(","):
        return dict(zip(eight_gua,list("戊丁辛己丙壬庚乙癸")))
    if kook1 in "陽七庚午,陽七乙亥,陽七癸巳,陽七戊戌,陽七丁未,陽七辛酉".split(","):
        return dict(zip(eight_gua,list("癸乙庚壬丙己辛丁戊")))
    if kook1 in "陽四庚午,陽四壬午,陽四戊子,陽四乙未,陽四丙午,陽四己酉,陽四丁巳".split(","):
        return dict(zip(eight_gua,list("癸壬辛庚己戊乙丙丁")))
    if kook1 in "陽四壬申,陽四戊寅,陽四丙戌,陽四己丑,陽四癸卯,陽四庚戌,陽四乙卯".split(","):
        return dict(zip(eight_gua,list("乙庚癸丙己壬丁戊辛")))
    if kook1 in "陽四丙寅,陽四己巳,陽四庚辰,陽四壬辰,陽四丁酉,陽四戊申,陽四辛酉".split(","):
        return dict(zip(eight_gua,list("辛戊丁壬己丙癸庚乙")))
    if kook1 in "陽四甲子,陽四戊辰,陽四甲戌,陽四丙子,陽四己卯,陽四甲申,陽四庚寅,陽四甲午,陽四辛丑,陽四甲辰,陽四壬子,陽四甲寅,陽四癸亥".split(","):
        return dict(zip(eight_gua,list("丁丙乙戊己庚辛壬癸")))
    if kook1 in "陽四辛未,陽四丁丑,陽四乙酉,陽四壬寅,陽四癸丑,陽四庚申".split(","):
        return dict(zip(eight_gua,list("丙乙庚丁己癸戊辛壬")))
    if kook1 in "陽四乙丑,陽四癸未,陽四辛卯,陽四丙申,陽四己亥,陽四丁未,陽四戊午".split(","):
        return dict(zip(eight_gua,list("壬辛戊癸己丁庚乙丙")))
    if kook1 in "陽四癸酉,陽四辛巳,陽四丁亥,陽四庚子,陽四乙巳,陽四丙辰,陽四己未".split(","):
        return dict(zip(eight_gua,list("庚癸壬乙己辛丙丁戊")))
    if kook1 in "陽四丁卯,陽四乙亥,陽四癸巳,陽四戊戌,陽四辛亥,陽四壬戌".split(","):
        return dict(zip(eight_gua,list("戊丁丙辛己乙壬癸庚")))
        
    else:
        return dict(zip(eight_gua,multi_key_dict_get(sky_pan_orders, kook)[dict(zip(eight_gua, get_humhead)).get(zfgong)]))
#暗干
angan = {'陰三甲子': ['庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '丙坤'],
'陰三乙丑': ['己巳', '戊辰', '丁卯', '庚午', '丙寅', '辛未', '乙丑', '癸酉', '壬申', '丙兌'],
'陰三丙寅': ['戊辰', '丁卯', '辛未', '己巳', '丙寅', '壬申', '庚午', '乙丑', '癸酉', '丙坎'],
'陰三丁卯': ['癸酉', '乙丑', '庚午', '壬申', '丙寅', '己巳', '辛未', '丁卯', '戊辰', '丙震'],
'陰三戊辰': ['壬申', '癸酉', '乙丑', '辛未', '丙寅', '庚午', '丁卯', '戊辰', '己巳', '丙坤'],
'陰三己巳': ['辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '丙坎'],
'陰三庚午': ['乙丑', '庚午', '壬申', '癸酉', '丙寅', '戊辰', '壬申', '辛未', '丁卯', '丙巽'],
'陰三辛未': ['己巳', '戊辰', '丁卯', '庚午', '丙寅', '辛未', '乙丑', '癸酉', '壬申', '丙乾'],
'陰三壬申': ['丁卯', '辛未', '壬申', '戊辰', '丙寅', '庚午', '己巳', '庚午', '乙丑', '丙離'],
'陰三癸酉': ['庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '丙艮'],
'陰三甲戌': ['庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '丙坤'],
'陰三乙亥': ['己卯', '戊寅', '丁丑', '庚辰', '丙子', '辛巳', '乙亥', '癸未', '壬午', '丙巽'],
'陰三丙子': ['壬午', '癸未', '乙亥', '辛巳', '丙子', '庚辰', '丁丑', '戊寅', '己卯', '丙坤'],
'陰三丁丑': ['辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '丙乾'],
'陰三戊寅': ['丁丑', '辛巳', '壬午', '戊寅', '丙子', '癸未', '己卯', '庚辰', '乙亥', '丙震'],
'陰三己卯': ['癸未', '乙亥', '庚辰', '壬午', '丙子', '己卯', '辛巳', '丁丑', '戊寅', '丙坤'],
'陰三庚辰': ['庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '丙坎'],
'陰三辛巳': ['戊寅', '丁丑', '辛巳', '己卯', '丙子', '壬午', '庚辰', '乙亥', '癸未', '丙離'],
'陰三壬午': ['乙亥', '庚辰', '己卯', '癸未', '丙子', '戊寅', '壬午', '辛巳', '丁丑', '丙艮'],
'陰三癸未': ['庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '丙兌'],
'陰三甲申': ['庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '丙坤'],
'陰三乙酉': ['辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '丙坎'],
'陰三丙戌': ['丁亥', '辛卯', '壬辰', '戊子', '丙戌', '癸巳', '己丑', '庚寅', '乙酉', '丙震'],
'陰三丁亥': ['戊子', '丁亥', '辛卯', '己丑', '丙戌', '壬辰', '庚寅', '乙酉', '癸巳', '丙離'],
'陰三戊子': ['壬辰', '癸巳', '乙酉', '辛卯', '丙戌', '庚寅', '丁亥', '戊子', '己丑', '丙乾'],
'陰三己丑': ['乙酉', '庚寅', '己丑', '癸巳', '丙戌', '戊子', '壬辰', '辛卯', '丁亥', '丙震'],
'陰三庚寅': ['己丑', '戊子', '丁亥', '庚寅', '丙戌', '辛卯', '乙酉', '癸巳', '壬辰', '丙坤'],
'陰三辛卯': ['癸巳', '乙酉', '庚寅', '壬辰', '丙戌', '己丑', '辛卯', '丁亥', '戊子', '丙艮'],
'陰三壬辰': ['乙酉', '庚寅', '己丑', '癸巳', '丙戌', '戊子', '壬辰', '辛卯', '丁亥', '丙兌'],
'陰三癸巳': ['庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '丙巽'],
'陰三甲午': ['庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '丙坤'],
'陰三乙未': ['乙未', '庚子', '己亥', '癸卯', '丙申', '戊戌', '壬寅', '辛丑', '丁酉', '丙離'],
'陰三丙申': ['癸卯', '乙未', '庚子', '壬寅', '丙申', '己亥', '辛丑', '丁酉', '戊戌', '丙兌'],
'陰三丁酉': ['己亥', '戊戌', '丁酉', '庚子', '丙申', '辛丑', '乙未', '癸卯', '壬寅', '丙坎'],
'陰三戊戌': ['丁酉', '辛丑', '壬寅', '戊戌', '丙申', '癸卯', '己亥', '庚子', '乙未', '丙巽'],
'陰三己亥': ['壬寅', '癸卯', '乙未', '辛丑', '丙申', '庚子', '丁酉', '戊戌', '己亥', '丙兌'],
'陰三庚子': ['戊戌', '丁酉', '辛丑', '己亥', '丙申', '壬寅', '庚子', '乙未', '癸卯', '丙艮'],
'陰三辛丑': ['丁酉', '辛丑', '壬寅', '戊戌', '丙申', '癸卯', '己亥', '庚子', '乙未', '丙坤'],
'陰三壬寅': ['辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '丙震'],
'陰三癸卯': ['庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '丙乾'],
'陰三甲辰': ['庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '丙坤'],
'陰三乙巳': ['乙巳', '庚戌', '己酉', '癸丑', '丙午', '戊申', '壬子', '辛亥', '丁未', '丙乾'],
'陰三丙午': ['戊申', '丁未', '辛亥', '己酉', '丙午', '壬子', '庚戌', '乙巳', '癸丑', '丙艮'],
'陰三丁未': ['辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '丙巽'],
'陰三戊申': ['癸丑', '乙巳', '庚戌', '壬子', '丙午', '己酉', '辛亥', '丁未', '戊申', '丙兌'],
'陰三己酉': ['丁未', '辛亥', '壬子', '戊申', '丙午', '癸丑', '己酉', '庚戌', '乙巳', '丙艮'],
'陰三庚戌': ['辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '丙離'],
'陰三辛亥': ['壬子', '癸丑', '乙巳', '辛未', '丙午', '庚戌', '丁未', '戊申', '己酉', '丙坎'],
'陰三壬子': ['己酉', '戊申', '丁未', '庚戌', '丙午', '辛亥', '乙巳', '癸丑', '壬子', '丙坤'],
'陰三癸丑': ['庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '丙震'],
'陰三甲寅': ['庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '丙坤'],
'陰三乙卯': ['丁巳', '辛酉', '壬戌', '戊午', '丙辰', '癸亥', '己未', '庚申', '乙卯', '丙震'],
'陰三丙辰': ['壬戌', '癸亥', '乙卯', '辛酉', '丙辰', '庚申', '丁巳', '戊午', '己未', '丙坎'],
'陰三丁巳': ['乙卯', '庚申', '己未', '癸亥', '丙辰', '戊午', '壬戌', '辛酉', '丁巳', '丙兌'],
'陰三戊午': ['辛酉', '壬戌', '癸亥', '丁巳', '丙辰', '乙卯', '戊午', '己未', '庚申', '丙艮'],
'陰三己未': ['壬戌', '癸亥', '乙卯', '辛酉', '丙辰', '庚申', '丁巳', '戊午', '己未', '丙離'],
'陰三庚申': ['癸亥', '乙卯', '庚申', '壬戌', '丙辰', '己未', '辛酉', '丁巳', '戊午', '丙乾'],
'陰三辛酉': ['戊午', '丁巳', '辛酉', '己未', '丙辰', '壬戌', '庚申', '乙卯', '癸亥', '丙巽'],
'陰三壬戌': ['己未', '戊午', '丁巳', '庚申', '丙辰', '辛酉', '乙卯', '癸亥', '壬戌', '丙坎'],
'陰三癸亥': ['庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '丙坤'],
'陰六甲子': ['癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '己坤'],
'陰六乙丑': ['辛未', '戊辰', '丁卯', '壬申', '己已', '丙寅', '癸酉', '庚午', '乙丑', '己離'],
'陰六丙寅': ['丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '己乾'],
'陰六丁卯': ['壬申', '辛未', '戊辰', '癸酉', '己巳', '丁卯', '庚午', '乙丑', '丙寅', '己震'],
'陰六戊辰': ['辛未', '戊辰', '丁卯', '壬申', '己巳', '丙寅', '癸酉', '庚午', '乙丑', '己坤'],
'陰六己巳': ['戊辰', '丁卯', '丙寅', '辛末', '己巳', '乙丑', '壬申', '癸酉', '庚午', '己巽'],
'陰六庚午': ['庚午', '癸酉', '壬申', '乙丑', '己巳', '辛未', '丙寅', '丁卯', '戊辰', '己艮'],
'陰六辛未': ['乙丑', '庚午', '癸酉', '丙寅', '己巳', '壬申', '丁卯', '戊辰', '辛未', '己坎'],
'陰六壬申': ['丙寅', '乙丑', '庚午', '丁卯', '己巳', '癸酉', '戊辰', '辛未', '壬申', '己巽'],
'陰六癸酉': ['癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '己兌'],
'陰六甲戌': ['癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '己坤'],
'陰六乙亥': ['辛巳', '戊寅', '丁丑', '壬午', '己卯', '丙子', '癸未', '庚辰', '乙亥', '己兌'],
'陰六丙子': ['庚辰', '癸未', '壬午', '乙亥', '己卯', '辛巳', '丙子', '丁丑', '戊寅', '己艮'],
'陰六丁丑': ['癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '己離'],
'陰六戊寅': ['壬午', '辛巳', '戊寅', '癸未', '己卯', '丁丑', '庚辰', '乙亥', '丙子', '己乾'],
'陰六己卯': ['丙子', '乙亥', '庚辰', '丁丑', '己卯', '癸未', '戊寅', '辛巳', '壬午', '己坤'],
'陰六庚辰': ['丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '己巽'],
'陰六辛巳': ['戊寅', '丁丑', '丙子', '辛巳', '己卯', '乙亥', '壬午', '癸未', '庚辰', '己震'],
'陰六壬午': ['乙亥', '庚辰', '癸未', '丙子', '己卯', '壬午', '丁丑', '戊寅', '辛巳', '己坤'],
'陰六癸未': ['癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '己坎'],
'陰六甲申': ['癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '己坤'],
'陰六乙酉': ['丙戌', '乙酉', '庚寅', '丁亥', '己丑', '癸巳', '戊子', '辛卯', '壬辰', '己坎'],
'陰六丙戌': ['乙酉', '庚寅', '癸巳', '丙戌', '己丑', '壬辰', '丁亥', '戊子', '辛卯', '己巽'],
'陰六丁亥': ['庚寅', '癸巳', '壬辰', '乙酉', '己丑', '辛卯', '丙戌', '丁亥', '戊子', '己兌'],
'陰六戊子': ['戊子', '丁亥', '丙戌', '辛卯', '己丑', '乙酉', '壬辰', '癸巳', '庚寅', '己艮'],
'陰六己丑': ['辛卯', '戊子', '丁亥', '壬辰', '己丑', '丙戌', '癸巳', '庚寅', '乙酉', '己乾'],
'陰六庚寅': ['壬辰', '辛卯', '戊子', '癸巳', '己丑', '丁亥', '庚寅', '乙酉', '丙戌', '己坤'],
'陰六辛卯': ['丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '己離'],
'陰六壬辰': ['乙酉', '庚寅', '癸巳', '丙戌', '己丑', '壬辰', '丁亥', '戊子', '辛卯', '己乾'],
'陰六癸巳': ['癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '己震'],
'陰六甲午': ['癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '己坤'],
'陰六乙未': ['壬寅', '辛丑', '戊戌', '癸卯', '己亥', '丁酉', '庚子', '乙未', '丙申', '己艮'],
'陰六丙申': ['辛丑', '戊戌', '丁酉', '壬寅', '己亥', '丙申', '癸卯', '庚子', '乙未', '己離'],
'陰六丁酉': ['乙未', '庚子', '癸卯', '丙申', '己亥', '壬寅', '丁酉', '戊戌', '辛丑', '己乾'],
'陰六戊戌': ['丙申', '乙未', '庚子', '丁酉', '己亥', '癸卯', '戊戌', '辛丑', '壬寅', '己坤'],
'陰六己亥': ['丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '己艮'],
'陰六庚子': ['庚子', '癸卯', '壬寅', '乙未', '己亥', '辛丑', '丙申', '丁酉', '戊戌', '己兌'],
'陰六辛丑': ['壬寅', '辛丑', '戊戌', '癸卯', '己亥', '丁酉', '庚子', '乙未', '丙申', '己坤'],
'陰六壬寅': ['戊戌', '丁酉', '丙申', '辛丑', '己亥', '乙未', '壬寅', '癸卯', '庚子', '己坎'],
'陰六癸卯': ['癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '己巽'],
'陰六甲辰': ['癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '己坤'],
'陰六乙巳': ['壬子', '辛亥', '戊申', '癸丑', '己酉', '丁未', '庚戌', '乙巳', '丙午', '己兌'],
'陰六丙午': ['丙午', '乙巳', '庚戌', '丁未', '己酉', '癸丑', '戊申', '辛亥', '壬子', '己艮'],
'陰六丁未': ['丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '己離'],
'陰六戊申': ['戊申', '丁未', '丙午', '辛亥', '己酉', '乙巳', '壬子', '癸丑', '庚戌', '己乾'],
'陰六己酉': ['乙巳', '庚戌', '癸丑', '丙午', '己酉', '壬子', '丁未', '戊申', '辛亥', '己坤'],
'陰六庚戌': ['癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '己巽'],
'陰六辛亥': ['辛亥', '戊申', '丁未', '壬子', '己酉', '丙午', '癸丑', '庚戌', '乙巳', '己震'],
'陰六壬子': ['庚戌', '癸丑', '壬子', '乙巳', '己酉', '辛亥', '丙午', '丁未', '戊申', '己坤'],
'陰六癸丑': ['癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '己坎'],
'陰六甲寅': ['癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '己坤'],
'陰六乙卯': ['丁巳', '丙辰', '乙卯', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '己巽'],
'陰六丙辰': ['戊午', '丁巳', '丙辰', '辛酉', '己未', '乙卯', '壬戌', '癸亥', '庚申', '己兌'],
'陰六丁巳': ['辛酉', '戊午', '丁巳', '壬戌', '己未', '丙辰', '癸亥', '庚申', '乙卯', '己艮'],
'陰六戊午': ['丙辰', '乙卯', '庚申', '丁巳', '己未', '癸亥', '戊午', '辛酉', '壬戌', '己離'],
'陰六己未': ['庚申', '癸亥', '壬戌', '乙卯', '己未', '辛酉', '丙辰', '丁巳', '戊午', '己震'],
'陰六庚申': ['壬戌', '辛酉', '戊午', '癸亥', '己未', '丁巳', '庚申', '乙卯', '丙辰', '己坎'],
'陰六辛酉': ['乙卯', '庚申', '癸亥', '丙辰', '己未', '壬戌', '丁巳', '戊午', '辛酉', '己乾'],
'陰六壬戌': ['庚申', '癸亥', '壬戌', '乙卯', '己未', '辛酉', '丙辰', '丁巳', '戊午', '己震'],
'陰六癸亥': ['癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '己坤'],
'陰九甲子': ['乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '壬坤'],
'陰九乙丑': ['癸酉', '乙丑', '丙寅', '庚午', '壬申', '丁卯', '己巳', '戊辰', '辛未', '壬艮'],
'陰九丙寅': ['庚午', '癸酉', '乙丑', '己巳', '壬申', '丙寅', '戊辰', '辛未', '丁卯', '壬兌'],
'陰九丁卯': ['丙寅', '丁卯', '辛未', '乙丑', '壬申', '戊辰', '癸酉', '庚午', '己巳', '壬巽'],
'陰九戊辰': ['辛未', '戊辰', '己巳', '丁卯', '壬申', '庚午', '丙寅', '乙丑', '癸酉', '壬坤'],
'陰九己巳': ['己巳', '庚午', '癸酉', '戊辰', '壬申', '乙丑', '辛未', '丁卯', '丙寅', '壬震'],
'陰九庚午': ['丁卯', '辛未', '戊辰', '丙寅', '壬申', '己巳', '乙丑', '癸酉', '庚午', '壬乾'],
'陰九辛未': ['辛未', '戊辰', '己巳', '丁卯', '壬申', '庚午', '丙寅', '乙丑', '癸酉', '壬坎'],
'陰九壬申': ['戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '壬兌'],
'陰九癸酉': ['乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '壬離'],
'陰九甲戌': ['乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '壬坤'],
'陰九乙亥': ['癸未', '乙亥', '丙子', '庚辰', '壬午', '丁丑', '己卯', '戊寅', '辛巳', '壬離'],
'陰九丙子': ['丁丑', '辛巳', '戊寅', '丙子', '壬午', '己卯', '乙亥', '癸未', '庚辰', '壬艮'],
'陰九丁丑': ['戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '壬兌'],
'陰九戊寅': ['庚辰', '癸未', '乙亥', '己卯', '壬午', '丙子', '戊寅', '辛巳', '丁丑', '壬坎'],
'陰九己卯': ['辛巳', '戊寅', '己卯', '丁丑', '壬午', '庚辰', '丙子', '乙亥', '癸未', '壬坤'],
'陰九庚辰': ['戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '壬震'],
'陰九辛巳': ['己卯', '庚辰', '癸未', '戊寅', '壬午', '乙亥', '辛巳', '丁丑', '丙子', '壬巽'],
'陰九壬午': ['丙子', '丁丑', '辛巳', '乙亥', '壬午', '戊寅', '癸未', '庚辰', '己卯', '壬艮'],
'陰九癸未': ['乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '壬乾'],
'陰九甲申': ['乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '壬坤'],
'陰九乙酉': ['辛卯', '戊子', '己丑', '丁亥', '壬辰', '庚寅', '丙戌', '乙酉', '癸巳', '壬乾'],
'陰九丙戌': ['己丑', '庚寅', '癸巳', '戊子', '壬辰', '乙酉', '辛卯', '丁亥', '丙戌', '壬離'],
'陰九丁亥': ['癸巳', '乙酉', '丙戌', '庚寅', '壬辰', '丁亥', '己丑', '戊子', '辛卯', '壬艮'],
'陰九戊子': ['戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '壬巽'],
'陰九己丑': ['己丑', '庚寅', '癸巳', '戊子', '壬辰', '乙酉', '辛卯', '丁亥', '丙戌', '壬坎'],
'陰九庚寅': ['庚寅', '癸巳', '乙酉', '己丑', '壬辰', '丙戌', '戊子', '辛卯', '丁亥', '壬坤'],
'陰九辛卯': ['丁亥', '辛卯', '戊子', '丙戌', '壬辰', '己丑', '乙酉', '癸巳', '庚寅', '壬兌'],
'陰九壬辰': ['丙戌', '丁亥', '辛卯', '乙酉', '壬辰', '戊子', '癸巳', '庚寅', '己丑', '壬離'],
'陰九癸巳': ['乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '壬震'],
'陰九甲午': ['乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '壬坤'],
'陰九乙未': ['丁酉', '辛丑', '戊戌', '丙申', '壬寅', '己亥', '乙未', '癸卯', '庚子', '壬兌'],
'陰九丙申': ['戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '壬巽'],
'陰九丁酉': ['丙申', '丁酉', '辛丑', '乙未', '壬寅', '戊戌', '癸卯', '庚子', '己亥', '壬坎'],
'陰九戊戌': ['丁酉', '辛丑', '戊戌', '丙申', '壬寅', '己亥', '乙未', '癸卯', '庚子', '壬震'],
'陰九己亥': ['辛丑', '戊戌', '己亥', '丁酉', '壬寅', '庚子', '丙申', '乙未', '癸卯', '壬乾'],
'陰九庚子': ['癸卯', '乙未', '丙申', '庚子', '壬寅', '丁酉', '己亥', '戊戌', '辛丑', '壬離'],
'陰九辛丑': ['庚子', '癸卯', '乙未', '己亥', '壬寅', '丙申', '戊戌', '辛丑', '丁酉', '壬坤'],
'陰九壬寅': ['己亥', '庚子', '癸卯', '戊戌', '壬寅', '乙未', '辛丑', '丁酉', '丙申', '壬巽'],
'陰九癸卯': ['乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '壬艮'],
'陰九甲辰': ['乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '壬坤'],
'陰九乙巳': ['丁未', '辛亥', '戊申', '丙午', '壬子', '己酉', '乙巳', '癸丑', '庚戌', '壬坎'],
'陰九丙午': ['癸丑', '乙巳', '丙午', '庚戌', '壬子', '丁未', '己酉', '戊申', '辛亥', '壬坤'],
'陰九丁未': ['乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '壬震'],
'陰九戊申': ['丙午', '丁未', '辛亥', '乙巳', '壬子', '戊申', '癸丑', '庚戌', '己酉', '壬離'],
'陰九己酉': ['己酉', '庚戌', '癸丑', '戊申', '壬子', '乙巳', '辛亥', '丁未', '丙午', '壬艮'],
'陰九庚戌': ['戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '壬兌'],
'陰九辛亥': ['辛亥', '戊申', '己酉', '丁未', '壬子', '庚戌', '丙午', '乙巳', '癸丑', '壬乾'],
'陰九壬子': ['庚戌', '癸丑', '乙巳', '己酉', '壬子', '丙午', '戊申', '辛亥', '丁未', '壬坤'],
'陰九癸丑': ['乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '壬巽'],
'陰九甲寅': ['乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '壬坤'],
'陰九乙卯': ['己未', '庚申', '癸亥', '戊午', '壬戌', '乙卯', '辛酉', '丁巳', '丙辰', '壬巽'],
'陰九丙辰': ['庚申', '癸亥', '乙卯', '己未', '壬戌', '丙辰', '戊午', '辛酉', '丁巳', '壬乾'],
'陰九丁巳': ['癸亥', '乙卯', '丙辰', '庚申', '壬戌', '丁巳', '己未', '戊午', '辛酉', '壬離'],
'陰九戊午': ['辛酉', '戊午', '己未', '丁巳', '壬戌', '庚申', '丙辰', '乙卯', '癸亥', '壬兌'],
'陰九己未': ['丁巳', '辛酉', '戊午', '丙辰', '壬戌', '己未', '乙卯', '癸亥', '庚申', '壬巽'],
'陰九庚申': ['丙辰', '丁巳', '辛酉', '乙卯', '壬戌', '戊午', '癸亥', '庚申', '己未', '壬坎'],
'陰九辛酉': ['戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '丁巳', '丙辰', '乙卯', '壬艮'],
'陰九壬戌': ['庚申', '癸亥', '乙卯', '己未', '壬戌', '丙辰', '戊午', '辛酉', '丁巳', '壬乾'],
'陰九癸亥': ['乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '壬坤'],
'陽一甲子': ['戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '壬坤'],
'陽一乙丑': ['辛未', '戊辰', '己巳', '丁卯', '壬申', '庚午', '丙寅', '乙丑', '癸酉', '壬艮'],
'陽一丙寅': ['丁卯', '辛未', '戊辰', '丙寅', '壬申', '己巳', '乙丑', '癸酉', '庚午', '壬兌'],
'陽一丁卯': ['己巳', '庚午', '癸酉', '戊辰', '壬申', '乙丑', '辛未', '丁卯', '丙寅', '壬巽'],
'陽一戊辰': ['辛未', '戊辰', '己巳', '丁卯', '壬申', '庚午', '丙寅', '乙丑', '癸酉', '壬坤'],
'陽一己巳': ['丙寅', '丁卯', '辛未', '乙丑', '壬申', '戊辰', '癸酉', '庚午', '己巳', '壬震'],
'陽一庚午': ['庚午', '癸酉', '乙丑', '己巳', '壬申', '丙寅', '戊辰', '辛未', '丁卯', '壬乾'],
'陽一辛未': ['癸酉', '乙丑', '丙寅', '庚午', '壬申', '丁卯', '己巳', '戊辰', '辛未', '壬坎'],
'陽一壬申': ['乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '壬震'],
'陽一癸酉': ['戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '壬離'],
'陽一甲戌': ['戊寅', '已卯', '庚辰', '辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '壬坤'],
'陽一乙亥': ['辛巳', '戊寅', '己卯', '丁丑', '壬午', '庚辰', '丙子', '乙亥', '癸未', '壬離'],
'陽一丙子': ['庚辰', '癸未', '乙亥', '己卯', '壬午', '丙子', '戊寅', '辛巳', '丁丑', '壬艮'],
'陽一丁丑': ['戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '壬兌'],
'陽一戊寅': ['丁丑', '辛巳', '戊寅', '丙子', '壬午', '己卯', '乙亥', '癸未', '庚辰', '壬坎'],
'陽一己卯': ['癸未', '乙亥', '丙子', '庚辰', '壬午', '丁丑', '己卯', '戊寅', '辛巳', '壬坤'],
'陽一庚辰': ['乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '壬震'],
'陽一辛巳': ['丙子', '丁丑', '辛巳', '乙亥', '壬午', '戊寅', '癸未', '庚辰', '己卯', '壬巽'],
'陽一壬午': ['己卯', '庚辰', '癸未', '戊寅', '壬午', '乙亥', '辛巳', '丁丑', '丙子', '壬坤'],
'陽一癸未': ['戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '壬乾'],
'陽一甲申': ['戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '壬坤'],
'陽一乙酉': ['癸巳', '乙酉', '丙戌', '庚寅', '壬辰', '丁亥', '己丑', '戊子', '辛卯', '壬乾'],
'陽一丙戌': ['己丑', '庚寅', '癸巳', '戊子', '壬辰', '乙酉', '辛卯', '丁亥', '丙戌', '壬離'],
'陽一丁亥': ['辛卯', '戊子', '己丑', '丁亥', '壬辰', '庚寅', '丙戌', '乙酉', '癸巳', '壬艮'],
'陽一戊子': ['乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '壬巽'],
'陽一己丑': ['丙戌', '丁亥', '辛卯', '乙酉', '壬辰', '戊子', '癸巳', '庚寅', '己丑', '壬坎'],
'陽一庚寅': ['丁亥', '辛卯', '戊子', '丙戌', '壬辰', '己丑', '乙酉', '癸巳', '庚寅', '壬坤'],
'陽一辛卯': ['庚寅', '癸巳', '乙酉', '己丑', '壬辰', '丙戌', '戊子', '辛卯', '丁亥', '壬兌'],
'陽一壬辰': ['己丑', '庚寅', '癸巳', '戊子', '壬辰', '乙酉', '辛卯', '丁亥', '丙戌', '壬坎'],
'陽一癸巳': ['戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '壬震'],
'陽一甲午': ['戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '壬坤'],
'陽一乙未': ['丁酉', '辛丑', '戊戌', '丙申', '壬寅', '己亥', '乙未', '癸卯', '庚子', '壬兌'],
'陽一丙申': ['乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '壬巽'],
'陽一丁酉': ['己亥', '庚子', '癸卯', '戊戌', '壬寅', '乙未', '辛丑', '丁酉', '丙申', '壬坎'],
'陽一戊戌': ['庚子', '癸卯', '乙未', '己亥', '壬寅', '丙申', '戊戌', '辛丑', '丁酉', '壬震'],
'陽一己亥': ['癸卯', '乙未', '丙申', '庚子', '壬寅', '丁酉', '己亥', '戊戌', '辛丑', '壬乾'],
'陽一庚子': ['辛丑', '戊戌', '己亥', '丁酉', '壬寅', '庚子', '丙申', '乙未', '癸卯', '壬離'],
'陽一辛丑': ['丁酉', '辛丑', '戊戌', '丙申', '壬寅', '己亥', '乙未', '癸卯', '庚子', '壬坤'],
'陽一壬寅': ['丙申', '丁酉', '辛丑', '乙未', '壬寅', '戊戌', '癸卯', '庚子', '己亥', '壬乾'],
'陽一癸卯': ['戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '壬艮'],
'陽一甲辰': ['戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '壬坤'],
'陽一乙巳': ['丁未', '辛亥', '戊申', '丙午', '壬子', '己酉', '乙巳', '癸丑', '庚戌', '壬離'],
'陽一丙午': ['癸丑', '乙巳', '丙午', '庚戌', '壬子', '丁未', '己酉', '戊申', '辛亥', '壬艮'],
'陽一丁未': ['乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '壬兌'],
'陽一戊申': ['丙午', '丁未', '辛亥', '乙巳', '壬子', '戊申', '癸丑', '庚戌', '己酉', '壬坎'],
'陽一己酉': ['己酉', '庚戌', '癸丑', '戊申', '壬子', '乙巳', '辛亥', '丁未', '丙午', '壬坤'],
'陽一庚戌': ['戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '壬震'],
'陽一辛亥': ['辛亥', '戊申', '己酉', '丁未', '壬子', '庚戌', '丙午', '乙巳', '癸丑', '壬巽'],
'陽一壬子': ['庚戌', '癸丑', '乙巳', '己酉', '壬子', '丙午', '戊申', '辛亥', '丁未', '壬坤'],
'陽一癸丑': ['戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '壬乾'],
'陽一甲寅': ['戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '丁巳', '丙辰', '乙卯', '壬坤'],
'陽一乙卯': ['丙辰', '丁巳', '辛酉', '乙卯', '壬戌', '戊午', '癸亥', '庚申', '己未', '壬震'],
'陽一丙辰': ['丁巳', '辛酉', '戊午', '丙辰', '壬戌', '己未', '乙卯', '癸亥', '庚申', '壬乾'],
'陽一丁巳': ['辛酉', '戊午', '己未', '丁巳', '壬戌', '庚申', '丙辰', '乙卯', '癸亥', '壬離'],
'陽一戊午': ['癸亥', '乙卯', '丙辰', '庚申', '壬戌', '丁巳', '己未', '戊午', '辛酉', '壬兌'],
'陽一己未': ['庚申', '癸亥', '乙卯', '己未', '壬戌', '丙辰', '戊午', '辛酉', '丁巳', '壬巽'],
'陽一庚申': ['己未', '庚申', '癸亥', '戊午', '壬戌', '乙卯', '辛酉', '丁巳', '丙辰', '壬坎'],
'陽一辛酉': ['乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '壬艮'],
'陽一壬戌': ['庚申', '癸亥', '乙卯', '己未', '壬戌', '丙辰', '戊午', '辛酉', '丁巳', '壬巽'],
'陽一癸亥': ['戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '丁巳', '丙辰', '乙卯', '壬坤'],
'陽七甲子': ['辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '丙坤'],
'陽七乙丑': ['壬申', '癸酉', '乙丑', '辛未', '丙寅', '庚午', '丁卯', '戊辰', '己巳', '丙兌'],
'陽七丙寅': ['癸酉', '乙丑', '庚午', '壬申', '丙寅', '己巳', '辛未', '丁卯', '戊辰', '丙離'],
'陽七丁卯': ['戊辰', '丁卯', '辛未', '己巳', '丙寅', '壬申', '庚午', '乙丑', '癸酉', '丙震'],
'陽七戊辰': ['己巳', '戊辰', '丁卯', '庚午', '丙寅', '辛未', '乙丑', '癸酉', '壬申', '丙坤'],
'陽七己巳': ['庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '癸酉', '壬申', '辛未', '丙坎'],
'陽七庚午': ['丁卯', '辛未', '壬申', '戊辰', '丙寅', '癸酉', '己巳', '庚午', '乙丑', '丙巽'],
'陽七辛未': ['己巳', '戊辰', '丁卯', '庚午', '丙寅', '辛未', '乙丑', '癸酉', '壬申', '丙乾'],
'陽七壬申': ['乙丑', '庚午', '己巳', '癸酉', '丙寅', '戊辰', '壬申', '辛未', '丁卯', '丙離'],
'陽七癸酉': ['辛未', '壬申', '癸酉', '丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '丙艮'],
'陽七甲戌': ['辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '丙坤'],
'陽七乙亥': ['壬午', '癸未', '乙亥', '辛巳', '丙子', '庚辰', '丁丑', '戊寅', '己卯', '丙巽'],
'陽七丙子': ['己卯', '戊寅', '丁丑', '庚辰', '丙子', '辛巳', '乙亥', '癸未', '壬午', '丙艮'],
'陽七丁丑': ['庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '丙乾'],
'陽七戊寅': ['乙亥', '庚辰', '己卯', '癸未', '丙子', '戊寅', '壬午', '辛巳', '丁丑', '丙震'],
'陽七己卯': ['戊寅', '丁丑', '辛巳', '己卯', '丙子', '壬午', '庚辰', '乙亥', '癸未', '丙坤'],
'陽七庚辰': ['庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '癸未', '壬午', '辛巳', '丙坎'],
'陽七辛巳': ['癸未', '乙亥', '庚辰', '壬午', '丙子', '己卯', '辛巳', '丁丑', '戊寅', '丙離'],
'陽七壬午': ['丁丑', '辛巳', '壬午', '戊寅', '丙子', '癸未', '己卯', '庚辰', '乙亥', '丙艮'],
'陽七癸未': ['辛巳', '壬午', '癸未', '丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '丙兌'],
'陽七甲申': ['辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '丙坤'],
'陽七乙酉': ['庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '癸巳', '壬辰', '辛卯', '丙坎'],
'陽七丙戌': ['乙酉', '庚寅', '己丑', '癸巳', '丙戌', '戊子', '壬辰', '辛卯', '丁亥', '丙兌'],
'陽七丁亥': ['癸巳', '乙酉', '庚寅', '壬辰', '丙戌', '己丑', '辛卯', '丁亥', '戊子', '丙離'],
'陽七戊子': ['己丑', '戊子', '丁亥', '庚寅', '丙戌', '辛卯', '乙酉', '癸巳', '壬辰', '丙乾'],
'陽七己丑': ['乙酉', '庚寅', '己丑', '癸巳', '丙戌', '戊子', '壬辰', '辛卯', '丁亥', '丙震'],
'陽七庚寅': ['壬辰', '癸巳', '乙酉', '辛卯', '丙戌', '庚寅', '丁亥', '戊子', '己丑', '丙坤'],
'陽七辛卯': ['戊子', '丁亥', '辛卯', '己丑', '丙戌', '壬辰', '庚寅', '乙酉', '癸巳', '丙艮'],
'陽七壬辰': ['丁亥', '辛卯', '壬辰', '戊子', '丙戌', '癸巳', '己丑', '庚寅', '乙酉', '丙兌'],
'陽七癸巳': ['辛卯', '壬辰', '癸巳', '丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '丙巽'],
'陽七甲午': ['辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '丙坤'],
'陽七乙未': ['丁酉', '辛丑', '壬寅', '戊戌', '丙申', '癸卯', '己亥', '庚子', '乙未', '丙離'],
'陽七丙申': ['戊戌', '丁酉', '辛丑', '己亥', '丙申', '壬寅', '庚子', '乙未', '癸卯', '丙震'],
'陽七丁酉': ['壬寅', '癸卯', '乙未', '辛丑', '丙申', '庚子', '丁酉', '戊戌', '己亥', '丙坎'],
'陽七戊戌': ['丁酉', '辛丑', '壬寅', '戊戌', '丙申', '癸卯', '己亥', '庚子', '乙未', '丙巽'],
'陽七己亥': ['己亥', '戊戌', '丁酉', '庚子', '丙申', '辛丑', '乙未', '癸卯', '壬寅', '丙兌'],
'陽七庚子': ['癸卯', '乙未', '庚子', '壬寅', '丙申', '己亥', '辛丑', '丁酉', '戊戌', '丙艮'],
'陽七辛丑': ['乙未', '庚子', '己亥', '癸卯', '丙申', '戊戌', '壬寅', '辛丑', '丁酉', '丙坤'],
'陽七壬寅': ['庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '癸卯', '壬寅', '辛丑', '丙震'],
'陽七癸卯': ['辛丑', '壬寅', '癸卯', '丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '丙乾'],
'陽七甲辰': ['辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '丙坤'],
'陽七乙巳': ['丁未', '辛亥', '壬子', '戊申', '丙午', '癸丑', '己酉', '庚戌', '乙巳', '丙乾'],
'陽七丙午': ['癸丑', '乙巳', '庚戌', '壬子', '丙午', '己酉', '辛亥', '丁未', '戊申', '丙坤'],
'陽七丁未': ['辛亥', '壬子', '癸丑', '丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '丙巽'],
'陽七戊申': ['戊申', '丁未', '辛亥', '己酉', '丙午', '壬子', '庚戌', '乙巳', '癸丑', '丙兌'],
'陽七己酉': ['乙巳', '庚戌', '己酉', '癸丑', '丙午', '戊申', '壬子', '辛亥', '丁未', '丙艮'],
'陽七庚戌': ['庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '丙離'],
'陽七辛亥': ['己酉', '戊申', '丁未', '庚戌', '丙午', '辛亥', '乙巳', '癸丑', '壬子', '丙坎'],
'陽七壬子': ['己酉', '戊申', '丁未', '庚戌', '丙午', '辛亥', '乙巳', '癸丑', '壬子', '丙坤'],
'陽七癸丑': ['庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '癸丑', '壬子', '辛亥', '丙震'],
'陽七甲寅': ['庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '丙坤'],
'陽七乙卯': ['丁巳', '辛酉', '壬戌', '戊午', '丙辰', '癸亥', '己未', '庚申', '乙卯', '丙震'],
'陽七丙辰': ['壬戌', '癸亥', '乙卯', '辛酉', '丙辰', '庚申', '丁巳', '戊午', '己未', '丙離'],
'陽七丁巳': ['乙卯', '庚申', '己未', '癸亥', '丙辰', '戊午', '壬戌', '辛酉', '丁巳', '丙兌'],
'陽七戊午': ['辛酉', '壬戌', '癸亥', '丁巳', '丙辰', '乙卯', '戊午', '己未', '庚申', '丙艮'],
'陽七己未': ['壬戌', '癸亥', '乙卯', '辛酉', '丙辰', '庚申', '丁巳', '戊午', '己未', '丙離'],
'陽七庚申': ['癸亥', '乙卯', '庚申', '壬戌', '丙辰', '己未', '辛酉', '丁巳', '戊午', '丙乾'],
'陽七辛酉': ['戊午', '丁巳', '辛酉', '己未', '丙辰', '壬戌', '庚申', '乙卯', '癸亥', '丙巽'],
'陽七壬戌': ['己未', '戊午', '丁巳', '庚申', '丙辰', '辛酉', '乙卯', '癸亥', '壬戌', '丙坎'],
'陽七癸亥': ['庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '癸亥', '壬戌', '辛酉', '丙坤'],
'陽四甲子': ['丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '己坤'],
'陽四乙丑': ['辛未', '戊辰', '丁卯', '壬申', '己巳', '丙寅', '癸酉', '庚午', '乙丑', '己離'],
'陽四丙寅': ['癸酉', '壬申', '辛未', '庚午', '己巳', '戊辰', '乙丑', '丙寅', '丁卯', '己乾'],
'陽四丁卯': ['丙寅', '乙丑', '庚午', '丁卯', '己巳', '癸酉', '戊辰', '辛未', '壬申', '己震'],
'陽四戊辰': ['乙丑', '庚午', '癸酉', '丙寅', '己巳', '壬申', '丁卯', '戊辰', '辛未', '己坤'],
'陽四己巳': ['庚午', '癸酉', '壬申', '乙丑', '己巳', '辛未', '丙寅', '丁卯', '戊辰', '己乾'],
'陽四庚午': ['戊辰', '丁卯', '丙寅', '辛未', '己巳', '乙丑', '壬申', '癸酉', '庚午', '己艮'],
'陽四辛未': ['辛未', '戊辰', '丁卯', '壬申', '己巳', '丙寅', '癸酉', '庚午', '乙丑', '己坎'],
'陽四壬申': ['壬申', '辛未', '戊辰', '癸酉', '己巳', '丁卯', '庚午', '乙丑', '丙寅', '己巽'],
'陽四癸酉': ['丁卯', '丙寅', '乙丑', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '己兌'],
'陽四甲戌': ['丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '己坤'],
'陽四乙亥': ['辛巳', '戊寅', '丁丑', '壬午', '己卯', '丙子', '癸未', '庚辰', '乙亥', '己震'],
'陽四丙子': ['庚辰', '癸未', '壬午', '乙亥', '己卯', '辛巳', '丙子', '丁丑', '戊寅', '己坤'],
'陽四丁丑': ['癸未', '壬午', '辛巳', '庚辰', '己卯', '戊寅', '乙亥', '丙子', '丁丑', '己坎'],
'陽四戊寅': ['壬午', '辛巳', '戊寅', '癸未', '己卯', '丁丑', '庚辰', '乙亥', '丙子', '己巽'],
'陽四己卯': ['丙子', '乙亥', '庚辰', '丁丑', '己卯', '癸未', '戊寅', '辛巳', '壬午', '己坤'],
'陽四庚辰': ['丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '己乾'],
'陽四辛巳': ['戊寅', '丁丑', '丙子', '辛巳', '己卯', '乙亥', '壬午', '癸未', '庚辰', '己兌'],
'陽四壬午': ['乙亥', '庚辰', '癸未', '丙子', '己卯', '壬午', '丁丑', '戊寅', '辛巳', '己艮'],
'陽四癸未': ['丁丑', '丙子', '乙亥', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '己離'],
'陽四甲申': ['丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '己坤'],
'陽四乙酉': ['壬辰', '辛卯', '戊子', '癸巳', '己丑', '丁亥', '庚寅', '乙酉', '丙戌', '己坎'],
'陽四丙戌': ['辛卯', '戊子', '丁亥', '壬辰', '己丑', '丙戌', '癸巳', '庚寅', '乙酉', '己巽'],
'陽四丁亥': ['戊子', '丁亥', '丙戌', '辛卯', '己丑', '乙酉', '壬辰', '癸巳', '庚寅', '己兌'],
'陽四戊子': ['庚寅', '癸巳', '壬辰', '乙酉', '己丑', '辛卯', '丙戌', '丁亥', '戊子', '己艮'],
'陽四己丑': ['乙酉', '庚寅', '癸巳', '丙戌', '己丑', '壬辰', '丁亥', '戊子', '辛卯', '己乾'],
'陽四庚寅': ['丙戌', '乙酉', '庚寅', '丁亥', '己丑', '癸巳', '戊子', '辛卯', '壬辰', '己坤'],
'陽四辛卯': ['癸巳', '壬辰', '辛卯', '庚寅', '己丑', '戊子', '乙酉', '丙戌', '丁亥', '己離'],
'陽四壬辰': ['乙酉', '庚寅', '癸巳', '丙戌', '己丑', '壬辰', '丁亥', '戊子', '辛卯', '己乾'],
'陽四癸巳': ['丁亥', '丙戌', '乙酉', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '己震'],
'陽四甲午': ['丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '己坤'],
'陽四乙未': ['丙申', '乙未', '庚子', '丁酉', '己亥', '癸卯', '戊戌', '辛丑', '壬寅', '己艮'],
'陽四丙申': ['乙未', '庚子', '癸卯', '丙申', '己亥', '壬寅', '丁酉', '戊戌', '辛丑', '己離'],
'陽四丁酉': ['辛丑', '戊戌', '丁酉', '壬寅', '己亥', '丙申', '癸卯', '庚子', '乙未', '己乾'],
'陽四戊戌': ['壬寅', '辛丑', '戊戌', '癸卯', '己亥', '丁酉', '庚子', '乙未', '丙申', '己震'],
'陽四己亥': ['癸卯', '壬寅', '辛丑', '庚子', '己亥', '戊戌', '乙未', '丙申', '丁酉', '己離'],
'陽四庚子': ['戊戌', '丁酉', '丙申', '辛丑', '己亥', '乙未', '壬寅', '癸卯', '庚子', '己兌'],
'陽四辛丑': ['壬寅', '辛丑', '戊戌', '癸卯', '己亥', '丁酉', '庚子', '乙未', '丙申', '己坤'],
'陽四壬寅': ['庚子', '癸卯', '壬寅', '乙未', '己亥', '辛丑', '丙申', '丁酉', '戊戌', '己坎'],
'陽四癸卯': ['丁酉', '丙申', '乙未', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '己巽'],
'陽四甲辰': ['丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '己坤'],
'陽四乙巳': ['丙午', '乙巳', '庚戌', '丁未', '己酉', '癸丑', '戊申', '辛亥', '壬子', '己兌'],
'陽四丙午': ['壬子', '辛亥', '戊申', '癸丑', '己酉', '丁未', '庚戌', '乙巳', '丙午', '己艮'],
'陽四丁未': ['癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '己離'],
'陽四戊申': ['庚戌', '癸丑', '壬子', '乙巳', '己酉', '辛亥', '丙午', '丁未', '戊申', '己乾'],
'陽四己酉': ['辛亥', '戊申', '丁未', '壬子', '己酉', '丙午', '癸丑', '庚戌', '乙巳', '己艮'],
'陽四庚戌': ['癸丑', '壬子', '辛亥', '庚戌', '己酉', '戊申', '乙巳', '丙午', '丁未', '己巽'],
'陽四辛亥': ['乙巳', '庚戌', '癸丑', '丙午', '己酉', '壬子', '丁未', '戊申', '辛亥', '己震'],
'陽四壬子': ['戊申', '丁未', '丙午', '辛亥', '己酉', '乙巳', '壬子', '癸丑', '庚戌', '己坤'],
'陽四癸丑': ['丁未', '丙午', '乙巳', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '己坎'],
'陽四甲寅': ['丁巳', '丙辰', '乙卯', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '己坤'],
'陽四乙卯': ['癸亥', '壬戌', '辛酉', '庚申', '己未', '戊午', '乙卯', '丙辰', '丁巳', '己巽'],
'陽四丙辰': ['庚申', '癸亥', '壬戌', '乙卯', '己未', '辛酉', '丙辰', '丁巳', '戊午', '己兌'],
'陽四丁巳': ['乙卯', '庚申', '癸亥', '丙辰', '己未', '壬戌', '丁巳', '戊午', '辛酉', '己艮'],
'陽四戊午': ['壬戌', '辛酉', '戊午', '癸亥', '己未', '丁巳', '庚申', '乙卯', '丙辰', '己離'],
'陽四己未': ['庚申', '癸亥', '壬戌', '乙卯', '己未', '辛酉', '丙辰', '丁巳', '戊午', '己兌'],
'陽四庚申': ['丙辰', '乙卯', '庚申', '丁巳', '己未', '癸亥', '戊午', '辛酉', '壬戌', '己坎'],
'陽四辛酉': ['辛酉', '戊午', '丁巳', '壬戌', '己未', '丙辰', '癸亥', '庚申', '乙卯', '己乾'],
'陽四壬戌': ['戊午', '丁巳', '辛酉', '丙辰', '己未', '乙卯', '壬戌', '癸亥', '庚申', '己震'],
'陽四癸亥': ['丁巳', '丙辰', '乙卯', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥', '己坤']}


if __name__ == '__main__':
    year = 1976
    month = 12
    day = 28
    hour = 0
    minute = 44
    #print(liujiashun_dict())
    #print(qimen_ju_name_zhirun_raw(year, month, day, hour, minute))
    print(f"{year}-{month}-{day} {hour}:{minute}")
    #print( get_jieqi_start_date(year, month, day, hour, minute))
    #print( get_next_jieqi_start_date(year, month, day, hour, minute))
    #print( get_before_jieqi_start_date(year, month, day, hour, minute))
    print(jq(year, month, day, hour, minute))
    #print(findyuen(year, month, day, hour, minute))
    print(qimen_ju_name_zhirun(year, month, day, hour, minute))
    #print(gangzhi(year, month, day, hour, minute))
    #print(zhifu_n_zhishi_ke(year, month, day, hour, minute))
    print(qimen_ju_name_ke(year, month, day, hour, minute))
    #print(pan_sky_minute(year, month, day, hour, minute))
    #print(zhifu_n_zhishi(year, month, day, hour, minute, 2))
    #print(qimen_ju_name_ke(year, month, day, hour, minute))
    #print(zhifu_n_zhishi_ke(year, month, day, hour, minute))
    #print(pan_sky_minute(year, month, day, hour, minute))
    #print(qimen_ju_name_ke(year, month, day, hour, minute))
    #print(zhifu_n_zhishi_ke(year, month, day, hour, minute))
    #print(pan_sky_minute(year, month, day, hour, minute))
    #print(zhifu_n_zhishi(year, month, day, hour, minute, 1))
    #print(zhifu_n_zhishi(year, month, day, hour, minute, 2))
    #print(zhifu_pai(year, month, day, hour, minute, 1))
    #print(zhifu_pai(year, month, day, hour, minute, 2))
