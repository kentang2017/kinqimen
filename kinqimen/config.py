# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:32:50 2020

@author: hooki
"""

from datetime import datetime
import re

def jiazi():
    tiangan = '甲乙丙丁戊己庚辛壬癸'
    dizhi = '子丑寅卯辰巳午未申酉戌亥'
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi

def new_list_r(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code - 1
    return res1

def new_list(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code + 1
    return res1

def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None

def ganzhiyear(year):
    year_gan_code = year%10 -3 +10
    if year_gan_code > 10:
        year_gan_code = year_gan_code -10
    year_zhi_code = year%12 -3 +12
    if year_zhi_code > 12:
        year_zhi_code = year_zhi_code -12
    year_ganzhi = Gan[year_gan_code-1] + Zhi[year_zhi_code-1]
    result = year_ganzhi[0]
    if result == "甲":
        result = hidden_jia.get(year_ganzhi)
    return result, year_ganzhi


START_YEAR = 1901
month_DAY_BIT = 12
month_NUM_BIT = 13
stc= '小寒大寒立春雨水驚蟄春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至'
solarTermsNameList=re.findall('..',stc)


jieqidun_code = {
("冬至", "驚蟄"): "一七四", 
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
"大雪":"四七一"}

# 1901-2100年二十节气最小公差数序列 向量压缩法
encryptionVectorList=[4, 19, 3, 18, 4, 19, 4, 19, 4, 20, 4, 20, 6, 22, 6, 22, 6, 22, 7, 22, 6, 21, 6, 21]
# 1901-2100年二十节气数据 每个元素的存储格式如下：
# 1-24
# 节气所在天（减去节气最小公约数）
# 1901-2100年香港天文台公布二十四节气按年存储16进制，1个16进制为4个2进制
solarTermsData=[
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, # 1901 ~ 1905
    0xaaaaaaaaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a56, 0xaaaaaaaa9a5a, 0xaaabaabaaeaa,
    0x569665a65aaa, 0x5aa6a6a69a56, 0x6aaaaaaa9a5a, 0xaaabaabaaeaa, 0x569665a65aaa,
    0x5aa6a6a65a56, 0x6aaaaaaa9a5a, 0xaaabaabaaa6a, 0x569665a65aaa, 0x5aa6a6a65a56,
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a,
    0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665665aaa,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665655aaa, 0x569665a65a56,
    0x6aa6a6aa9a56, 0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x6aa6a6a65a56,
    0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x5aa6a6a65a56, 0x6aaaa6aa9a5a,
    0x5556556555aa, 0x569665a65a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a,
    0x555665665a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a, 0x555665665a55,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555555556a, 0x555665665a55, 0x5aa665a65a56,
    0x6aaaa6aa9a5a, 0x55555555556a, 0x555665655a55, 0x5aa665a65a56, 0x6aa6a6aa9a5a,
    0x55555555456a, 0x555655655a55, 0x5a9665a65a56, 0x6aa6a6a69a5a, 0x55555555456a,
    0x555655655a55, 0x569665a65a56, 0x6aa6a6a65a56, 0x55555155455a, 0x555655655955,
    0x569665a65a55, 0x5aa6a5a65a56, 0x15555155455a, 0x555555655555, 0x569665665a55,
    0x5aa665a65a56, 0x15555155455a, 0x555555655515, 0x555665665a55, 0x5aa665a65a56,
    0x15555155455a, 0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a,
    0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a, 0x555555555515,
    0x555655655a55, 0x5aa665a65a56, 0x15515155455a, 0x555555554515, 0x555655655a55,
    0x5a9665a65a56, 0x15515151455a, 0x555551554515, 0x555655655a55, 0x569665a65a56,
    0x155151510556, 0x555551554505, 0x555655655955, 0x569665665a55, 0x155110510556,
    0x155551554505, 0x555555655555, 0x569665665a55, 0x55110510556, 0x155551554505,
    0x555555555515, 0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515,
    0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55,
    0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55, 0x55110510556,
    0x155151514505, 0x555555554515, 0x555655655a55, 0x54110510556, 0x155151510505,
    0x555551554515, 0x555655655a55, 0x14110110556, 0x155110510501, 0x555551554505,
    0x555555655555, 0x14110110555, 0x155110510501, 0x555551554505, 0x555555555555,
    0x14110110555, 0x55110510501, 0x155551554505, 0x555555555555, 0x110110555,
    0x55110510501, 0x155551554505, 0x555555555515, 0x110110555, 0x55110510501,
    0x155551554505, 0x555555555515, 0x100100555, 0x55110510501, 0x155151514505,
    0x555555555515, 0x100100555, 0x54110510501, 0x155151514505, 0x555551554515,
    0x100100555, 0x54110510501, 0x155150510505, 0x555551554515, 0x100100555,
    0x14110110501, 0x155110510505, 0x555551554505, 0x100055, 0x14110110500,
    0x155110510501, 0x555551554505, 0x55, 0x14110110500, 0x55110510501,
    0x155551554505, 0x55, 0x110110500, 0x55110510501, 0x155551554505,
    0x15, 0x100110500, 0x55110510501, 0x155551554505,0x555555555515]

Gan = list("甲乙丙丁戊己庚辛壬癸")
rGan = list("癸壬辛庚己戊丁丙乙甲")
rhourgang_dict = dict(zip(rGan, list(range(1,11))))
hourgang_dict = dict(zip(Gan, list(range(1,11))))
Zhi = list("子丑寅卯辰巳午未申酉戌亥")
hidden_jia = dict(zip(re.findall("..", "甲子甲戌甲申甲午甲辰甲寅"), list("戊己庚辛壬癸")))
liushun = re.findall('..',"甲子甲戌甲申甲午甲辰甲寅")
golen_d = re.findall("..","太乙攝提軒轅招搖天符青龍咸池太陰天乙")

gtw = re.findall("..","地籥六賊五符天曹地符風伯雷公雨師風雲唐符國印天關")
cnumber = list("一二三四五六七八九")
nine_star = list("蓬芮沖輔禽心柱任英")
eight_door = list("休死傷杜中開驚生景")
eight_door2 = list("休死傷杜開驚生景")
eight_gua = list("坎坤震巽中乾兌艮離")
eight_gua2 = list("坎坤震巽乾兌艮離")
god_dict = {"陽":list("符蛇陰合勾雀地天"),"陰":list("符蛇陰合虎玄地天")}
zhi2gan = dict(zip(Zhi,list("癸己甲乙戊丙丁己庚辛戊壬")))


gans_code = dict(zip(Gan,range(0,11)))
gans_code2 = dict(zip(Gan,range(1,11)))
cnumber_code = dict(zip(cnumber,range(1,11)))
stars_code = dict(zip(cnumber, nine_star))
doors_code = dict(zip(cnumber, eight_door))
gongs_code = dict(zip(cnumber, eight_gua))
stars_gong_code = dict(zip(eight_gua, nine_star))

paiyinyang = {
        "陽":{
        "一":"九八七一二三四五六",
        "二":"一九八二三四五六七",
        "三":"二一九三四五六七八",
        "四":"三二一四五六七八九",
        "五":"四三二五六七八九一",
        "六":"五四三六七八九一二",
        "七":"六五四七八九一二三",
        "八":"七六五八九一二三四",
        "九":"八七六九一二三四五"},
        "陰":{
        "九":"一二三九八七六五四",
        "八":"九一二八七六五四三",
        "七":"八九一七六五四三二",
        "六":"七八九六五四三二一",
        "五":"六七八五四三二一九",
        "四":"五六七四三二一九八",
        "三":"四五六三二一九八七",
        "二":"三四五二一九八七六",
        "一":"二三四一九八七六五"}}

clockwise_eightgua = list("坎艮震巽離坤兌乾")
anti_clockwise_eightgua = list(reversed(clockwise_eightgua))
door_r = list("休生傷杜景死驚開")
star_r = list("蓬任沖輔英禽柱心")

liujiashun_dict = {tuple(jiazi()[0:10]):"甲子", tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申", tuple(jiazi()[30:40]):"甲午", tuple(jiazi()[40:50]):"甲辰", tuple(jiazi()[50:60]):"甲寅"}
liujiashun_dict2 = {tuple(jiazi()[0:10]):"甲子戊", tuple(jiazi()[10:20]):"甲戌己", tuple(jiazi()[20:30]):"甲申庚", tuple(jiazi()[30:40]):"甲午辛", tuple(jiazi()[40:50]):"甲辰壬", tuple(jiazi()[50:60]):"甲寅癸"}
door_code = {"陽遁":dict(zip(range(1,9), eight_door2)),"陰遁":dict(zip(range(1,9), list(reversed(eight_door2))))}


findyuen_dict = {tuple(jiazi()[0:5]): "上元", 
                tuple(jiazi()[15:20]):"上元", 
                tuple(jiazi()[30:35]):"上元", 
                tuple(jiazi()[45:50]):"上元", 
                tuple(jiazi()[5:10]): "中元",  
                tuple(jiazi()[20:25]):"中元", 
                tuple(jiazi()[35:40]):"中元", 
                tuple(jiazi()[50:55]):"中元", 
                tuple(jiazi()[10:15]):"下元", 
                tuple(jiazi()[25:30]):"下元" , 
                tuple(jiazi()[40:45]):"下元" , 
                tuple(jiazi()[55:60]):"下元" }

guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
shunlist = {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}
jieqi_all = new_list([stc[i:i+2] for i in range(0, len(stc), 2)], "冬至")
yingyang_dun = {tuple(jieqi_all[0:12]):"陽遁",tuple(jieqi_all[12:24]):"陰遁" }
yingyang_order = {"陽遁":list("戊己庚辛壬癸丁丙乙"),"陰遁":list("戊乙丙丁癸壬辛庚己")}
cnumber_order = list("一二三四五六七八九")
clockwise_cnum = list("一八三四九二七六")
cnum_dict = dict(zip(cnumber_order, range(1,9)))


# 采集压缩用
def zipSolarTermsList(inputList,charCountLen=2):
    tempList=abListMerge(inputList, type=-1)
    data=0
    num=0
    for i in tempList:
        data+=i << charCountLen*num
        num+=1
    return hex(data),len(tempList)

        
def twentyfourjieqi(year):
    day = getTheYearAllSolarTermsList(year)
    month = [ele for ele in [i for i in range(1,13)] for b in range(2)]
    new_date_list = []
    for i in range(0,23):
        new_date = str(year)+"/"+str(month[i])+"/"+str(day[i])   
        date_format = datetime.strptime(new_date , "%Y/%m/%d").date()
        new_date_list.append(date_format)
    return dict(zip(new_date_list,solarTermsNameList))
# 两个List合并对应元素相加或者相减，a[i]+b[i]:tpye=1 a[i]-b[i]:tpye=-1
def abListMerge(a, b=encryptionVectorList, type=1):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i]*type)
    return c

def unZipSolarTermsList(data,rangeEndNum=24,charCountLen=2):
    list2 = []
    for i in range(1,rangeEndNum+1):
        right=charCountLen*(rangeEndNum-i)
        if type(data).__name__=='str':
            data= int(data, 16)
        x=data >> right
        c=2**charCountLen
        list2=[(x % c)]+list2
    return abListMerge(list2)
    
def getTheYearAllSolarTermsList(year):
    return unZipSolarTermsList(solarTermsData[year-START_YEAR])

def find_shier_luck(gan):
    twelve_luck = re.findall('..',"長生沐浴冠帶臨冠帝旺") + list("衰病死墓絕胎養")
    twelve_luck_i = list("死病衰") + re.findall('..',"帝旺臨冠冠帶沐浴長生") + list("養胎絕墓")
    yang = dict(zip(Gan[0::2], [dict(zip(y, twelve_luck)) for y in [new_list(Zhi, i) for i in list("亥寅寅巳申")]]))
    ying = dict(zip(Gan[1::2], [dict(zip(y, twelve_luck_i)) for y in [new_list(Zhi, i) for i in list("亥寅寅巳申")]]))
    return {**yang, **ying}.get(gan)

