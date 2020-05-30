# -*- coding: utf-8 -*-
"""
Created on Sun May 10 15:44:51 2020

@author: hooki
"""


Gan = list("甲乙丙丁戊己庚辛壬癸")
Zhi = list("子丑寅卯辰巳午未申酉戌亥")
eight_door = list("休死傷杜中開驚生景")
eight_star = list("蓬芮沖輔禽心柱任英")
eight_star2 = list("蓬任沖輔英芮柱心")
eight_gua2 = list("震巽離坤兌乾坎艮")
eight_door2 = list("開休生傷杜景死驚")
eight_gua4 = {"坎":1, "坤":2, "震":3, "巽":4, "中":5, "乾":6, "兌":7, "艮":8,"離":9}
eight_gua = list("坎坤震巽中乾兌艮離")
eight_gua3 = list("坎坤震巽中乾兌艮離")
eight_gods_yinyang = {"陽遁":list("符蛇陰合勾朱地天"), "陰遁":list("符天地玄白合陰蛇")}

hourgang_dict = dict(zip(Gan, list(range(1,11))))
gong_dict = dict(zip(list(range(1,10)), eight_gua))
door_dict = dict(zip(list(range(1,10)), eight_door))
door_dict2 = dict(zip(list(range(1,9)), eight_door2))
star_dict = dict(zip(list(range(1,10)), eight_star))
hidden_jia = {'甲子':'戊', '甲戌':'己','甲申':'庚','甲午':'辛','甲辰':'壬','甲寅':'癸' }



def new_list_r(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code + 1
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

def shun(gangzhi):
    shunlist = {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}
    gangzhi_gang = dict(zip(Gan, list(range(1,11))))
    gangzhi_zhi = dict(zip(Zhi, list(range(1,13))))
    gang = gangzhi_gang.get(gangzhi[0])
    zhi = gangzhi_zhi.get(gangzhi[1])
    shun_value =  zhi - gang
    if shun_value < 0:
        shun_value = shun_value+12
    return shunlist.get(shun_value)

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

print(star_dict.get(5))