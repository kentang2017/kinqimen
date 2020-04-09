# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:05:37 2019

@author: ken tang
@email: kinyeah@gmail.com
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

def jiazi():
    tiangan = '甲乙丙丁戊己庚辛壬癸'
    dizhi = '子丑寅卯辰巳午未申酉戌亥'
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi

def daykong_shikong(daygangzhi,hourgangzhi):
    liujiashun_dict = {tuple(jiazi()[0:10]):'甲子', tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申", tuple(jiazi()[30:40]):"甲午", tuple(jiazi()[40:50]):"甲辰",  tuple(jiazi()[50:60]):"甲寅"  }
    guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
    return {"日空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, daygangzhi)).get("孤"), "時空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, hourgangzhi)).get("孤")}

def qimen_ju_day(daygangzhi):
    ju_day_dict = {"甲":"甲己日", "己":"甲己日", "乙":"乙庚日", "庚":"乙庚日", "丙":"丙辛日", "辛":"丙辛日","丁":"丁壬日", "壬":"丁壬日", "戊":"戊癸日", "癸":"戊癸日"}
    ju_day = ju_day_dict.get(daygangzhi[0])
    return ju_day

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

def qimen_ju_name(jieqi, daygangzhi):
    find_yuen_dict = {("甲子","乙丑","丙寅","丁卯","戊辰","己卯","庚辰","辛巳","壬午","癸未", "甲午","乙未","丙申","丁酉","戊戌","己酉","庚戌","辛亥","壬子","癸丑"): "上元", ("己巳","庚午","辛未","壬申","癸酉", "甲申","乙酉","丙戌","丁亥","戊子","己亥","庚子","辛丑","壬寅","癸卯", "甲寅","乙卯","丙辰","丁巳","戊午"): "中元", ("甲戌","乙亥","丙子","丁丑","戊寅","己丑","庚寅","辛卯","壬辰","癸巳","甲辰","乙巳","丙午","丁未","戊申","己未","庚申","辛酉","壬戌","癸亥"):  "下元"}
    jieqi_panju = {
    "立春":{"上元":"陰遁八局",  "中元":"陰遁五局", "下元":"陰遁二局"},
    "立冬":{"上元":"陰遁六局",  "中元":"陰遁九局", "下元":"陰遁三局"},
    "立秋":{"上元":"陰遁二局",  "中元":"陰遁五局", "下元":"陰遁八局"},
    "芒種":{"上元":"陰遁六局",  "中元":"陰遁三局", "下元":"陰遁九局"},
    "小寒":{"上元":"陽遁二局",  "中元":"陽遁八局", "下元":"陽遁五局"},
    "大暑":{"上元":"陰遁七局",  "中元":"陰遁一局", "下元":"陰遁四局"},
    "大寒":{"上元":"陽遁三局",  "中元":"陽遁九局", "下元":"陽遁六局"},
    "處暑":{"上元":"陰遁一局",  "中元":"陰遁四局", "下元":"陰遁七局"},
    "秋分":{"上元":"陰遁七局",  "中元":"陰遁一局", "下元":"陰遁四局"},
    "小滿":{"上元":"陽遁五局",  "中元":"陽遁二局", "下元":"陽遁八局"},
    "大雪":{"上元":"陰遁四局",  "中元":"陰遁七局", "下元":"陰遁一局"},
    "驚蟄":{"上元":"陽遁一局",  "中元":"陽遁七局", "下元":"陽遁四局"},
    "春分":{"上元":"陽遁三局",  "中元":"陽遁九局", "下元":"陽遁六局"},
    "穀雨":{"上元":"陽遁五局",  "中元":"陽遁二局", "下元":"陽遁八局"},
    "寒露":{"上元":"陰遁六局",  "中元":"陰遁九局", "下元":"陰遁三局"},
    "冬至":{"上元":"陽遁一局",  "中元":"陽遁七局", "下元":"陽遁四局"},
    "立夏":{"上元":"陽遁四局",  "中元":"陽遁一局", "下元":"陽遁七局"},
    "夏至":{"上元":"陰遁九局",  "中元":"陰遁三局", "下元":"陰遁六局"},
    "白露":{"上元":"陰遁九局",  "中元":"陰遁三局", "下元":"陰遁六局"},
    "霜降":{"上元":"陰遁五局",  "中元":"陰遁八局", "下元":"陰遁二局"},
    "雨水":{"上元":"陽遁九局",  "中元":"陽遁六局", "下元":"陽遁三局"},
    "小暑":{"上元":"陰遁八局",  "中元":"陰遁二局", "下元":"陰遁五局"},
    "清明":{"上元":"陽遁四局",  "中元":"陽遁一局", "下元":"陽遁七局"},
    "小雪":{"上元":"陰遁五局",  "中元":"陰遁八局", "下元":"陰遁二局"}}
    find_yuen = multi_key_dict_get(find_yuen_dict, daygangzhi)
    findju = jieqi_panju.get(jieqi).get(find_yuen)
    return findju

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


def zhifu_zhishi(jieqi, daygangzhi, hourgangzhi):
    qimen_ju = qimen_ju_name(jieqi, daygangzhi)
    shun1 = shun(hourgangzhi)
    kok_num_dict = dict(zip(list("一二三四五六七八九"), list(range(1,10))))
    shun_num_dict = dict(zip(list("戊己庚辛壬癸"), list(range(1,7))))
    sanqiliuyi_dict = {"乙":9, "戊":1, "己":2, "庚":3, "辛":4, "壬":5, "癸":6, "丙":8, "丁":7}
    sanqiliuyi_dict2 = {"乙":9, "戊":6, "己":5, "庚":4, "辛":3, "壬":2, "癸":1, "丙":8, "丁":7}
    shun_num = shun_num_dict.get(shun1)
    kok_num = kok_num_dict.get(qimen_ju[2])
   
    if qimen_ju[0] == "陽":
        zhifu_zhishi_num = kok_num + shun_num -1
        if zhifu_zhishi_num > 9 :
            zhifu_zhishi_num = zhifu_zhishi_num - 9
        if zhifu_zhishi_num < 0:
            zhifu_zhishi_num = zhifu_zhishi_num + 9
        
        if hourgangzhi[0] == "甲":
            hourgang_num = 1
            new_hour_code = hidden_jia.get(hourgangzhi)
            hourgangzhi_code =  multi_key_dict_get(sanqiliuyi_dict, new_hour_code)
        elif hourgangzhi[0] != "甲":
            hourgang_num = hourgang_dict.get(hourgangzhi[0])
            hourgangzhi_code =  multi_key_dict_get(sanqiliuyi_dict, hourgangzhi[0])
        
        if hourgangzhi[0] == "甲":
            zhifu_lokgong = zhifu_zhishi_num + hourgang_num  - 1
        elif hourgangzhi[0] != "甲":
            zhifu_lokgong = hourgangzhi_code  + kok_num - 1
            if zhifu_lokgong > 9:
                zhifu_lokgong = zhifu_lokgong -9
            elif zhifu_lokgong < 0:
                zhifu_lokgong = zhifu_lokgong +9
        
        zhishi_lokgong = zhifu_zhishi_num + hourgang_num - 1
        if zhishi_lokgong > 9:
            zhishi_lokgong = zhishi_lokgong-9
        elif zhishi_lokgong < 0:
            zhishi_lokgong = zhishi_lokgong+9
        hourgangzhi_code_zs =  multi_key_dict_get(sanqiliuyi_dict, hourgangzhi[0])

    
    elif qimen_ju[0] == "陰":
        zhifu_zhishi_num = 1 + kok_num - shun_num
        if zhifu_zhishi_num > 9 :
            zhifu_zhishi_num = zhifu_zhishi_num - 9
        if zhifu_zhishi_num < 0 :
            zhifu_zhishi_num = zhifu_zhishi_num + 9
        
        if hourgangzhi[0] == "甲":
            hourgang_num = 1
            new_hour_code = hidden_jia.get(hourgangzhi)
            hourgangzhi_code_zs =  multi_key_dict_get(sanqiliuyi_dict2, new_hour_code)
            zhifu_lokgong = zhifu_zhishi_num + hourgang_num - 1
            zhishi_lokgong = zhifu_zhishi_num + hourgang_num - 1
             
        elif hourgangzhi[0] != "甲":
            new_hour_code = hourgang_dict.get(hourgangzhi[0])
            hourgang_num =  multi_key_dict_get(sanqiliuyi_dict2, hourgangzhi[0])
            hourgangzhi_code_zs =  multi_key_dict_get(sanqiliuyi_dict2, hourgangzhi[0]) 
            zhifu_lokgong = zhifu_zhishi_num + hourgangzhi_code_zs  - 3
            zhishi_lokgong = zhifu_zhishi_num + hourgangzhi_code_zs - 1
        
        if zhifu_lokgong > 9:
            zhifu_lokgong = zhifu_lokgong -9
        elif zhifu_lokgong <= 0:
            zhifu_lokgong = zhifu_lokgong +9
        
        
        if zhishi_lokgong > 9:
            zhishi_lokgong = zhishi_lokgong-9
        elif zhishi_lokgong <= 0:
            zhishi_lokgong = zhishi_lokgong+9
        
    zhifugong = gong_dict.get(zhifu_lokgong)
    zhishigong = gong_dict.get(zhishi_lokgong)
    if gong_dict.get(zhifu_lokgong) == "中":
        try:
            result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[new_list(eight_door2, eight_door2[zhifu_zhishi_num+1])[0], zhishigong ]}]
        except IndexError:
            result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[door_dict.get(zhifu_zhishi_num), zhishigong ]}]
    elif gong_dict.get(zhifu_lokgong) != "中":
        result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[door_dict.get(zhifu_zhishi_num), zhishigong ]}]
    return result

def qimen(jieqi, daygangzhi, hourgangzhi):
    qimen_ju = qimen_ju_name(jieqi, daygangzhi)
    zhifu_zhishi1 = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)
    zhifu_lokgong_o = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)[0].get("值符")[0]
    zhifu_lokgong_g = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)[0].get("值符")[1]
    zhifu_sky_pan_head = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)[0].get("值符")[2]
    zhishi_lokgong_o = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)[0].get("直使")[0]
    zhishi_lokgong_g = zhifu_zhishi(jieqi, daygangzhi, hourgangzhi)[0].get("直使")[1]
    if zhifu_lokgong_o == "禽":
        zhifu_lokgong_o = "芮"
    
    
    if qimen_ju[0] == "陽":
        if zhishi_lokgong_g != "中" and zhifu_lokgong_g != "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g),eight_gods_yinyang.get("陽遁")))
        elif zhishi_lokgong_g == "中" and zhifu_lokgong_g == "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), eight_gua3[5]),eight_gods_yinyang.get("陽遁")))
        elif zhishi_lokgong_g == "中" and zhifu_lokgong_g != "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g),eight_gods_yinyang.get("陽遁")))
        elif zhishi_lokgong_g != "中" and zhifu_lokgong_g == "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), eight_gua2[-5]),eight_gods_yinyang.get("陽遁")))

        yang_dun_lei = dict(zip(list("一二三四五六七八九"), list("乙丙丁癸壬辛庚己戊")))
        lei_gong = yang_dun_lei.get(qimen_ju[2])
        earth_pan = dict(zip(new_list_r(eight_gua, "離"), new_list(list("戊己庚辛壬癸丁丙乙"), lei_gong)))
        earth_pan2 = dict(zip(new_list(list("戊乙丙丁癸壬辛庚己"), lei_gong),  new_list_r(eight_gua, "離")))
        find_earth_gan_end = earth_pan2.get(zhifu_sky_pan_head)
        
    elif qimen_ju[0] == "陰":
        if zhishi_lokgong_g != "中" and zhifu_lokgong_g != "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g) ,eight_gods_yinyang.get("陰遁")))
        elif zhishi_lokgong_g == "中" and zhifu_lokgong_g == "中":
            god_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[-5]) ,eight_gods_yinyang.get("陰遁")))
        elif zhishi_lokgong_g == "中" and zhifu_lokgong_g != "中":
            god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g) ,eight_gods_yinyang.get("陰遁")))
        elif zhishi_lokgong_g != "中" and zhifu_lokgong_g == "中":
            god_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[-5]) ,eight_gods_yinyang.get("陰遁")))
            
        yin_dun_lei = dict(zip(list("一二三四五六七八九"), list("己庚辛壬癸丁丙乙戊")))
        lei_gong = yin_dun_lei.get(qimen_ju[2])
        earth_pan = dict(zip(new_list_r(eight_gua, "離"), new_list(list("戊乙丙丁癸壬辛庚己"), lei_gong)))
        earth_pan2 = dict(zip(new_list(list("戊乙丙丁癸壬辛庚己"), lei_gong),  new_list_r(eight_gua, "離")))

        find_earth_gan_end = earth_pan2.get(zhifu_sky_pan_head)

    earth_pan_list = list(earth_pan.values())
    del earth_pan_list[5]

    if zhishi_lokgong_g != "中" and zhifu_lokgong_g != "中":
        door_new_dict = dict(zip(new_list(eight_gua2,zhishi_lokgong_g), new_list(eight_door2, zhishi_lokgong_o)))
        star_new_dict = dict(zip(new_list(eight_gua2,zhifu_lokgong_g), new_list(eight_star2, zhifu_lokgong_o)))
        try: 
            sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g),  new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi))))
            sky_pan2 =  dict(zip(new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi)), new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g) ))    
        except ValueError:
            a = list("戊乙丙丁癸壬辛庚己")
            sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g),  new_list(a, a[eight_gua4.get(zhifu_lokgong_g)])))
            sky_pan2 = dict(zip(new_list(a, a[eight_gua4.get(zhifu_lokgong_g)]), new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g)))
            
    elif zhishi_lokgong_g == "中" and zhifu_lokgong_g == "中":
        door_new_dict = dict(zip(new_list(eight_gua2,eight_gua[3]), new_list(eight_door2, zhishi_lokgong_o)))
        star_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[-5]), new_list(eight_star2, zhifu_lokgong_o)))
        sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"),  eight_gua2[-5]),  new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi))))
        sky_pan2 =  dict(zip(new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi)), new_list(list("坎艮震巽離坤兌乾"), eight_gua3[eight_gua3.index(zhifu_lokgong_g)-3]) ))    

    elif zhifu_lokgong_g != "中" and zhishi_lokgong_g == "中":
        door_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[eight_gua2.index(zhifu_lokgong_g)]), new_list(eight_door2, eight_door2[4])))
        star_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[eight_gua2.index(zhifu_lokgong_g)]), new_list(eight_star, eight_star2[5])))
        sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g),  new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi))))
        sky_pan2 =  dict(zip(new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi)), new_list(list("坎艮震巽離坤兌乾"), zhifu_lokgong_g) ))    
    
    elif zhifu_lokgong_g == "中" and zhishi_lokgong_g != "中":
        door_new_dict = dict(zip(new_list(eight_gua2,eight_gua[1]), new_list(eight_door2, zhishi_lokgong_o)))
        star_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[-5]), new_list(eight_star2, zhifu_lokgong_o)))
        sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"),  eight_gua2[-5]),  new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi))))
        sky_pan2 =  dict(zip(new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi)), new_list(list("坎艮震巽離坤兌乾"), eight_gua3[eight_gua3.index(zhifu_lokgong_g)-3]) ))    

    
    if hourgangzhi[0] != "甲":
        yi = hourgangzhi[0]
    elif hourgangzhi[0] == "甲":
        yi = hidden_jia.get(hourgangzhi)
        
    d = []
    for i in eight_gua2:
        a = {i: {"天":sky_pan.get(i), "地":earth_pan.get(i), "星":star_new_dict.get(i), "門":door_new_dict.get(i), "神":god_new_dict.get(i)}}
        d.append(a)
        
    try:
        d1 = list(d[eight_gua2.index(zhifu_lokgong_g)].values())[0]
    except ValueError:
        d1 = list(d[eight_gua2.index(zhishi_lokgong_g)].values())[0]
    
    if sky_pan2.get(yi) != None:
        tianyi = [sky_pan.get(sky_pan2.get(yi)),sky_pan2.get(yi), door_new_dict.get(sky_pan2.get(yi)), god_new_dict.get(sky_pan2.get(yi)), star_new_dict.get(sky_pan2.get(yi))]
    elif sky_pan2.get(yi) != None and d1.get("天") == d1.get("地"):
        tianyi = [d1.get("天"),zhifu_lokgong_g,d1.get("門"), d1.get("神"), d1.get("星")]  
    elif sky_pan2.get(yi) == None:
        yi = earth_pan.get(zhifu_zhishi1[0]["值符"][1])
        if sky_pan2.get(yi) == None:
            yi2 = Gan[-1]
            tianyi = [yi, sky_pan2.get(yi2),door_new_dict.get(sky_pan2.get(yi2)), god_new_dict.get(sky_pan2.get(yi2)), star_new_dict.get(sky_pan2.get(yi2))]  
        elif sky_pan2.get(yi) != None:
            tianyi = [yi, sky_pan2.get(yi),door_new_dict.get(sky_pan2.get(yi)), god_new_dict.get(sky_pan2.get(yi)), star_new_dict.get(sky_pan2.get(yi))]  
    return {"排局": [qimen_ju, jieqi, daygangzhi+"日", hourgangzhi+"時"], "空亡":daykong_shikong(daygangzhi,hourgangzhi) , "值符":zhifu_zhishi1[0]["值符"], "直使":zhifu_zhishi1[0]["直使"], "天乙":tianyi, "天地盤":{ "地盤":earth_pan, "天盤":sky_pan}, "八星":star_new_dict, "八門":door_new_dict, "八神":god_new_dict}, d, d1

#print(qimen("大暑", "庚午", "甲申"))
#print(qimen("穀雨", "甲午", "乙亥"))
#print(qimen("夏至", "戊戌", "乙卯"))
#print(shun( "辛未"))