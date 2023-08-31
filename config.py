# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:55:49 2023

@author: kentang
"""

import re
from itertools import cycle, repeat
from math import pi
from sxtwl import fromSolar
import ephem
from ephem import Date, Ecliptic, Equatorial


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
wuxing_relation_2 = dict(zip(list(map(lambda x: tuple(re.findall("..",x)), wuxing.split(","))), "尅我,我尅,比和,生我,我生".split(",")))
cmonth = list("一二三四五六七八九十") + ["十一","十二"]

jieqi_name = re.findall('..', '冬至小寒大寒立春雨水驚蟄春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪')
jqmc = ["冬至", "小寒", "大寒", "立春", "雨水", "驚蟄", "春分", "清明", "谷雨", "立夏",
     "小滿", "芒種", "夏至", "小暑", "大暑", "立秋", "處暑","白露", "秋分", "寒露", "霜降", 
     "立冬", "小雪", "大雪"]


#%% 基本功能函數
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
    Gan, Zhi = '甲乙丙丁戊己庚辛壬癸', '子丑寅卯辰巳午未申酉戌亥'
    return list(map(lambda x: "{}{}".format(Gan[x % len(Gan)], Zhi[x % len(Zhi)]), list(range(60))))

def Ganzhiwuxing(gangorzhi):
    ganzhiwuxing = dict(zip(list(map(lambda x: tuple(x),"甲寅乙卯震巽,丙巳丁午離,壬亥癸子坎,庚申辛酉乾兌,未丑戊己未辰戌艮坤".split(","))), list("木火水金土")))
    return multi_key_dict_get(ganzhiwuxing, gangorzhi)

def jieqicode(year,month, day):
    return multi_key_dict_get({("冬至", "驚蟄"): "一七四",  "小寒": "二八五",  ("大寒", "春分"): "三九六", "立春":"八五二","雨水":"九六三",  ("清明", "立夏"): "四一七", ("穀雨", "小滿"): "五二八", "芒種": "六三九", ("夏至", "白露"): "九三六", "小暑":"八二五",  ("大暑", "秋分"): "七一四", "立秋":"二五八",  "處暑":"一四七",  ("霜降", "小雪"): "五八二", ("寒露", "立冬"): "六九三", "大雪":"四七一"}, jq(year,month, day))

def findyuen(year, month, day, hour, minute):
    return multi_key_dict_get(findyuen_dict(), gangzhi(year, month, day, hour, minute)[2])

def find_wx_relation(zhi1, zhi2):
    return multi_key_dict_get(wuxing_relation_2, Ganzhiwuxing(zhi1) + Ganzhiwuxing(zhi2))
#換算干支
def gangzhi(year, month, day, hour, minute):
    if hour == 23:
        d = Date(round((Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day+1).zfill(2), str(0).zfill(2)))), 3))
    else:
        d = Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG,mTG,dTG,hTG = "{}{}".format(tian_gan[cdate.getYearGZ().tg], di_zhi[cdate.getYearGZ().dz]), "{}{}".format(tian_gan[cdate.getMonthGZ().tg],di_zhi[cdate.getMonthGZ().dz]), "{}{}".format(tian_gan[cdate.getDayGZ().tg], di_zhi[cdate.getDayGZ().dz]), "{}{}".format(tian_gan[cdate.getHourGZ(dd[3]).tg], di_zhi[cdate.getHourGZ(dd[3]).dz])
    if year < 1900:
        mTG1 = find_lunar_month(yTG).get(lunar_date_d(year, month, day).get("月"))
    else:
        mTG1 = mTG
    hTG1 = find_lunar_hour(dTG).get(hTG[1])
    gangzhi_minute = minutes_jiazi_d().get(str(hour)+":"+str(minute))
    return [yTG, mTG1, dTG, hTG1, gangzhi_minute]
#旬
def shun(gz):
    shun_value = dict(zip(di_zhi, list(range(1,13)))).get(gz[1]) - dict(zip(tian_gan, list(range(1,11)))).get(gz[0])
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

def liujiashun_dict():
    return dict(zip(list(map(lambda x: tuple(x), list(map(lambda x:new_list(jiazi(), x)[0:10], jiazi()[0::10])))), jiazi()[0::10]))

def findyuen_dict():
    return dict(zip(list(map(lambda x:tuple(x), list(map(lambda i:new_list(jiazi(), i)[0:5], jiazi()[0::5])))), ["上元","中元","下元"]*4))
#分干支
def minutes_jiazi_d():
    t = [f"{h}:{m}" for h in range(24) for m in range(60)]
    minutelist = dict(zip(t, cycle(repeat_list(2, jiazi()))))
    return minutelist
#農曆
def lunar_date_d(year, month, day):
    day = fromSolar(year, month, day)
    return {"年":day.getLunarYear(),  "月": day.getLunarMonth(), "日":day.getLunarDay()}

#日空時空
def daykong_shikong(year, month, day, hour, minute):
    guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
    return {"日空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict(), gangzhi(year, month, day, hour, minute)[2])).get("孤"), "時空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict(), gangzhi(year, month, day, hour, minute)[3])).get("孤")}

def find_shier_luck(gan):
    return {**dict(zip(tian_gan[0::2], list(map(lambda y: dict(zip(y, re.findall('..',"長生沐浴冠帶臨冠帝旺") + list("衰病死墓絕胎養"))),list(map(lambda i:new_list(di_zhi, i),list("亥寅寅巳申"))))))), **dict(zip(tian_gan[1::2], [dict(zip(y, list("死病衰") + re.findall('..',"帝旺臨冠冠帶沐浴長生") + list("養胎絕墓"))) for y in list(map(lambda i:new_list(di_zhi, i), list("亥寅寅巳申")))]))}.get(gan)

#奇門排局
def qimen_ju_name(year, month, day, hour, minute):
    find_yingyang = multi_key_dict_get({tuple(jieqi_name[0:12]):"陽遁",tuple(jieqi_name[12:24]):"陰遁" }, jq(year, month, day))
    find_yuen = findyuen(year, month, day, hour, minute)
    jieqi_code = jieqicode(year, month, day)
    return "{}{}局{}".format(find_yingyang,{"上元":jieqi_code[0], "中元":jieqi_code[1], "下元":jieqi_code[2]}.get(find_yuen),find_yuen)

def getgtw(self):
    gtw = re.findall("..","地籥六賊五符天曹地符風伯雷公雨師風雲唐符國印天關")
    newgtw_list = list(map(lambda y: dict(zip(di_zhi, y)) ,list(map(lambda i: new_list(gtw, i),re.findall("..","地籥天關唐符風雲唐符風雲雷公風伯天曹五符")))))
    return dict(zip(tian_gan, newgtw_list))
#排值符
def zhifu_pai(year, month, day, hour, minute):
    yinyang = qimen_ju_name(year, month, day, hour, minute)[0]
    kook = qimen_ju_name(year, month, day, hour, minute)[2]
    pai = {"陽":{"一":"九八七一二三四五六","二":"一九八二三四五六七","三":"二一九三四五六七八","四":"三二一四五六七八九","五":"四三二五六七八九一","六":"五四三六七八九一二","七":"六五四七八九一二三","八":"七六五八九一二三四","九":"八七六九一二三四五"},
                  "陰":{"九":"一二三九八七六五四","八":"九一二八七六五四三","七":"八九一七六五四三二","六":"七八九六五四三二一","五":"六七八五四三二一九","四":"五六七四三二一九八","三":"四五六三二一九八七","二":"三四五二一九八七六","一":"二三四一九八七六五"}}.get(yinyang).get(kook)
    return {"陰":dict(zip(jiazi()[0::10], list(map(lambda x: x+pai, new_list_r(cnumber, kook)[0:6])))), "陽":dict(zip(jiazi()[0::10], list(map(lambda x: x+pai, new_list(cnumber, kook)[0:6]))))}.get(yinyang)
#排值使
def zhishi_pai(year, month, day, hour, minute):
    yinyang = qimen_ju_name(year, month, day, hour, minute)[0]
    kook = qimen_ju_name(year, month, day, hour, minute)[2]
    yanglist = "".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))
    yinlist =  "".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))
    return {"陰":dict(zip(jiazi()[0::10], list(map(lambda i: i+ yinlist[yinlist.index(i)+1:][0:11],new_list_r(cnumber, kook)[0:6])))), "陽":dict(zip(jiazi()[0::10], list(map(lambda i:i+ yanglist[yanglist.index(i)+1:][0:11], new_list(cnumber, kook)[0:6]))))}.get(yinyang)
#八門
def pan_door(year, month, day, hour, minute):
    starting_door = zhifu_n_zhishi(year, month, day, hour, minute).get("值使門宮")[0]
    starting_gong = zhifu_n_zhishi(year, month, day, hour, minute).get("值使門宮")[1]
    rotate = {"陽":clockwise_eightgua, "陰":list(reversed(clockwise_eightgua))}.get(qimen_ju_name(year, month, day, hour, minute)[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,{"陽":new_list(door_r, starting_door), "陰":new_list(list(reversed(door_r)), starting_door)}.get(qimen_ju_name(year, month, day, hour, minute)[0])))
#九星
def pan_star(year, month, day, hour, minute):
    star_r = list("蓬任沖輔英禽柱心")
    starting_star = zhifu_n_zhishi(year, month, day, hour, minute).get("值符星宮")[0].replace("芮", "禽")
    starting_gong = zhifu_n_zhishi(year, month, day, hour, minute).get("值符星宮")[1]
    rotate = {"陽":clockwise_eightgua, "陰":list(reversed(clockwise_eightgua))}.get(qimen_ju_name(year, month, day, hour, minute)[0])
    star_reorder = {"陽":new_list(star_r, starting_star), "陰":new_list(list(reversed(star_r)), starting_star)}.get(qimen_ju_name(year, month, day, hour, minute)[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,star_reorder)), dict(zip(star_reorder, gong_reorder))
#八神
def pan_god(year, month, day, hour, minute):
    starting_gong = zhifu_n_zhishi(year, month, day, hour, minute).get("值符星宮")[1]
    rotate = {"陽":clockwise_eightgua, "陰":list(reversed(clockwise_eightgua)) }.get(qimen_ju_name(year, month, day, hour, minute)[0])
    if starting_gong == "中":
        gong_reorder = new_list(rotate, "坤")
    else:
        gong_reorder = new_list(rotate, starting_gong)
    return dict(zip(gong_reorder,{"陽":list("符蛇陰合勾雀地天"),"陰":list("符蛇陰合虎玄地天")}.get(qimen_ju_name(year, month, day, hour, minute)[0])))
#找值符及值使
def zhifu_n_zhishi(year, month, day, hour, minute):
    gongs_code = dict(zip(cnumber, eight_gua))
    hgan = dict(zip(tian_gan,range(0,11))).get(gangzhi(year, month, day, hour, minute)[3][0])
    chour = multi_key_dict_get(liujiashun_dict(), gangzhi(year, month, day, hour, minute)[3])
    door = dict(zip(list(zhishi_pai(year, month, day, hour, minute).keys()), list(map(lambda i: dict(zip(cnumber, list("休死傷杜中開驚生景"))).get(i[0]), list(zhishi_pai(year, month, day, hour, minute).values()))))).get(chour)
    if door == "中":
        door = "死"
    return {"值符星宮":[dict(zip(list(zhifu_pai(year, month, day, hour, minute).keys()), list(map(lambda i:dict(zip(cnumber, list("蓬芮沖輔禽心柱任英"))).get(i[0]) , list(zhifu_pai(year, month, day, hour, minute).values()))))).get(chour),dict(zip(list(zhifu_pai(year, month, day, hour, minute).keys()), list(map(lambda i:gongs_code.get(i[hgan]), list(zhifu_pai(year, month, day, hour, minute).values()))))).get(chour)], "值使門宮":[door,dict(zip(list(zhishi_pai(year, month, day, hour, minute).keys()),list(map(lambda i:gongs_code.get(i[hgan]), list(zhishi_pai(year, month, day, hour, minute).values()))))).get(chour)]}

def ecliptic_lon(jd_utc):
    return Ecliptic(Equatorial(ephem.Sun(jd_utc).ra,ephem.Sun(jd_utc).dec,epoch=jd_utc)).lon

def sta(jd_num):
    return int(ecliptic_lon(jd_num)*180.0/pi/15)

def iteration(jd_num):
    s1_jd=sta(jd_num)
    s0_jd=s1_jd
    dt=1.0
    while True:
        jd_num+=dt
        s=sta(jd_num)
        if s0_jd!=s:
            s0_jd=s
            dt=-dt/2
        if abs(dt)<0.0000001 and s!=s1_jd:
            break
    return jd_num

def find_jq_date(year, month, day, hour, jie_qi):
    jd_format=Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    e_1=ecliptic_lon(jd_format)
    n_1=int(e_1*180.0/pi/15)+1
    dzlist = []
    for i in range(24):
        if n_1>=24:
            n_1-=24
        jd_d=iteration(jd_format)
        d=Date(jd_d+1/3).tuple()
        bb_1 = {jieqi_name[n_1]: Date("{}/{}/{} {}:{}:00.00".format(str(d[0]).zfill(4), str(d[1]).zfill(2), str(d[2]).zfill(2), str(d[3]).zfill(2) , str(d[4]).zfill(2)))}
        n_1+=1
        dzlist.append(bb_1)
    return list(dzlist[list(map(lambda i:list(i.keys())[0], dzlist)).index(jie_qi)].values())[0]

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
    return dict(zip(new_list(wangzhuai_num, dict(zip(jieqi_name[0::3],wangzhuai_num )).get(multi_key_dict_get(wangzhuai_jieqi, "霜降"))), wangzhuai))

def xzdistance(year, month, day, hour):
    return int(find_jq_date(year, month, day, hour, "夏至") -  Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2))))

def distancejq(year, month, day, hour, jq):
    return int( Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2))) - find_jq_date(year-1, month, day, hour, jq) )

def fjqs(year, month, day, hour):
    jd_format = Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
    n= int(ecliptic_lon(jd_format)*180.0/pi/15)+1
    c = []
    for i in range(1):
        if n>=24:
            n-=24
        d = Date(jd_format+1/3).tuple()
        c.append([jieqi_name[n], Date("{}/{}/{} {}:{}:00.00".format(str(d[0]).zfill(4), str(d[1]).zfill(2), str(d[2]).zfill(2), str(d[3]).zfill(2) , str(d[4]).zfill(2)))])
    return c[0]

#def jq(year, month, day, hour):
#    ct =  Date("{}/{}/{} {}:00:00.00".format(str(year).zfill(4), str(month).zfill(2), str(day).zfill(2), str(hour).zfill(2) ))
#    p = Date(round((ct - 7 ), 3)).tuple()
#    pp = Date(round((ct - 21 ), 3)).tuple()
#    bf = fjqs(p[0], p[1], p[2], p[3])
#    bbf = fjqs(pp[0], pp[1], pp[2], pp[3])
#    if ct < bf[1]:
#        return bbf[0]
#    else:
#        return jieqi_name[jieqi_name.index(bf[0])+1]

def jq(year, month, day):
    dd = fromSolar(year, month, day) 
    while True:
        dd = dd.before(1)
        if dd.hasJieQi():
            return jqmc[dd.getJieQi()]
            break



print(qimen_ju_name(1896, 9, 9, 12, 0))