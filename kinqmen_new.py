# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:05:37 2019

@author: ken tang
@email: kinyeah@gmail.com
"""

from qimen_dict import *
import sxtwl

class Qimen():
    def __init__(self, year, month, day, hour, jieqi):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.jieqi = jieqi
    
    def gangzhi(self):
        lunar = sxtwl.Lunar()
        cdate = lunar.getDayBySolar(self.year, self.month, self.day)
        yy_mm_dd = Gan[cdate.Lyear2.tg]+Zhi[cdate.Lyear2.dz],  Gan[cdate.Lmonth2.tg]+Zhi[cdate.Lmonth2.dz],  Gan[cdate.Lday2.tg]+Zhi[cdate.Lday2.dz]
        timegz = lunar.getShiGz(cdate.Lday2.tg, self.hour)
        new_hh = Gan[timegz.tg]+Zhi[timegz.dz]
        return yy_mm_dd[0], yy_mm_dd[1],  yy_mm_dd[2], new_hh
    
    def lunar_date(self):
        lunar = sxtwl.Lunar()  #实例化日历库
        day = lunar.getDayBySolar(self.year, self.month, self.day)
        if day.Lleap:
            ld =  "潤"+ ymc[day.Lmc]+"月"+rmc[day.Ldi]+"日"
        else:
            ld = ymc[day.Lmc]+"月"+ rmc[day.Ldi]+"日"
        return ld

    def jiazi(self):
        tiangan = '甲乙丙丁戊己庚辛壬癸'
        dizhi = '子丑寅卯辰巳午未申酉戌亥'
        jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
        return jiazi

    def check_lunar_month(self):
        lunar = sxtwl.Lunar()
        lunar_date = lunar.getDayByLunar(self.year, self.month, self.day)
        ymc = [u"十一月", u"十二月", u"一月", u"二月", u"三月", u"四月", u"五月", u"六月", u"七月", u"八月", u"九月", u"十月"]
        return str(ymc[lunar_date.Lmc])

    def weekday(self):
        dayNumber = calendar.weekday(self.year, self.month, self.day) 
        days =["Mon", "Tue", "Wed", "Thu", 
                             "Fri", "Sat", "Sun"] 
        return days[dayNumber]

    def shun(self):
        gangzhi = self.gangzhi()[3]
        shunlist = {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}
        gangzhi_gang = dict(zip(Gan, list(range(1,11))))
        gangzhi_zhi = dict(zip(Zhi, list(range(1,13))))
        gang = gangzhi_gang.get(gangzhi[0])
        zhi = gangzhi_zhi.get(gangzhi[1])
        shun_value =  zhi - gang
        if shun_value < 0:
            shun_value = shun_value+12
        return shunlist.get(shun_value)
    
    def qimen_ju_day(self):
        ju_day_dict = {"甲":"甲己日", "己":"甲己日", "乙":"乙庚日", "庚":"乙庚日", "丙":"丙辛日", "辛":"丙辛日","丁":"丁壬日", "壬":"丁壬日", "戊":"戊癸日", "癸":"戊癸日"}
        ju_day = ju_day_dict.get(self.gangzhi()[2][0])
        return ju_day
    
    def daykong_shikong(self):
        daygangzhi = self.gangzhi()[2]
        hourgangzhi = self.gangzhi()[3]
        liujiashun_dict = {tuple(self.jiazi()[0:10]):'甲子', tuple(self.jiazi()[10:20]):"甲戌", tuple(self.jiazi()[20:30]):"甲申", tuple(self.jiazi()[30:40]):"甲午", tuple(self.jiazi()[40:50]):"甲辰",  tuple(self.jiazi()[50:60]):"甲寅"  }
        guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
        return {"日空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, daygangzhi)).get("孤"), "時空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, hourgangzhi)).get("孤")}

    def qimen_ju_name(self):
        daygangzhi = self.gangzhi()[2]
        #find_yuen_dict = {("甲子","乙丑","丙寅","丁卯","戊辰","己卯","庚辰","辛巳","壬午","癸未", "甲午","乙未","丙申","丁酉","戊戌","己酉","庚戌","辛亥","壬子","癸丑"): "上元", ("己巳","庚午","辛未","壬申","癸酉", "甲申","乙酉","丙戌","丁亥","戊子","己亥","庚子","辛丑","壬寅","癸卯", "甲寅","乙卯","丙辰","丁巳","戊午"): "中元", ("甲戌","乙亥","丙子","丁丑","戊寅","己丑","庚寅","辛卯","壬辰","癸巳","甲辰","乙巳","丙午","丁未","戊申","己未","庚申","辛酉","壬戌","癸亥"):  "下元"}
        find_yuen_dict = {tuple(self.jiazi()[0:20]): "上元", tuple(self.jiazi()[20:40]): "中元", tuple(self.jiazi()[40:60]): "下元"}
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
        findju = jieqi_panju.get(self.jieqi).get(find_yuen)
        return findju
    
    def zhifu_zhishi(self):
        gangzhi = self.gangzhi()
        hourgangzhi = gangzhi[3]
        qimen_ju = self.qimen_ju_name()
        shun1 = self.shun()
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
        if gong_dict.get(zhifu_lokgong) == "中" and star_dict.get(zhifu_zhishi_num) !="禽":
            result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[new_list(eight_door2, eight_door2[zhifu_zhishi_num+1])[0], zhishigong ]}]
        elif gong_dict.get(zhifu_lokgong) != "中" and star_dict.get(zhifu_zhishi_num) !="禽":
            result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[door_dict.get(zhifu_zhishi_num), zhishigong ]}]
        elif gong_dict.get(zhifu_lokgong) != "中" and star_dict.get(zhifu_zhishi_num) =="禽":
            result = [{"值符":[star_dict.get(zhifu_zhishi_num), zhifugong, shun(hourgangzhi)], "直使":[door_dict2.get(7), zhishigong ]}]
        return [result, zhifu_zhishi_num, zhifu_lokgong]
        

    def result(self):
        qimen_ju = self.qimen_ju_name()
        zhifu_zhishi1 = self.zhifu_zhishi()
        gangzhi = self.gangzhi()
        hourgangzhi = gangzhi[3]
        daygangzhi = gangzhi[2]
        zhifu_lokgong_o = self.zhifu_zhishi()[0][0].get("值符")[0]
        zhifu_lokgong_g = self.zhifu_zhishi()[0][0].get("值符")[1]
        zhishi_lokgong_o = self.zhifu_zhishi()[0][0].get("直使")[0]
        zhishi_lokgong_g = self.zhifu_zhishi()[0][0].get("直使")[1]
    
        if zhifu_lokgong_o == "禽":
            zhifu_lokgong_o = "芮"
        
        if qimen_ju[0] == "陽":
            if zhishi_lokgong_g != "中" and zhifu_lokgong_g != "中":
                god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g),eight_gods_yinyang.get("陽遁")))
            elif zhishi_lokgong_g == "中" and zhifu_lokgong_g == "中":
                god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), eight_gua[1]), eight_gods_yinyang.get("陽遁")))
            elif zhishi_lokgong_g == "中" and zhifu_lokgong_g != "中":
                god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), zhifu_lokgong_g),eight_gods_yinyang.get("陽遁")))
            elif zhishi_lokgong_g != "中" and zhifu_lokgong_g == "中":
                god_new_dict = dict(zip(new_list(list("兌乾坎艮震巽離坤"), eight_gua2[-5]),eight_gods_yinyang.get("陽遁")))
    
            yang_dun_lei = dict(zip(list("一二三四五六七八九"), list("乙丙丁癸壬辛庚己戊")))
            lei_gong = yang_dun_lei.get(qimen_ju[2])
            earth_pan = dict(zip(new_list_r(eight_gua, "離"), new_list(list("戊己庚辛壬癸丁丙乙"), lei_gong)))
          
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
            door_new_dict = dict(zip(new_list(eight_gua2,eight_gua[1]), new_list(eight_door2, zhishi_lokgong_o)))
            star_new_dict = dict(zip(new_list(eight_gua2,eight_gua2[-5]), new_list(eight_star2, zhifu_lokgong_o)))
            try:
                sky_pan = dict(zip(new_list(list("坎艮震巽離坤兌乾"),  eight_gua2[5]),  new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi))))
                sky_pan2 =  dict(zip(new_list([earth_pan.get(i) for i in list("坎艮震巽離坤兌乾")], shun(hourgangzhi)), new_list(list("坎艮震巽離坤兌乾"), eight_gua3[eight_gua3.index(zhifu_lokgong_g)-3]) ))    
            except ValueError:
                a = list("戊己庚辛癸丁丙乙")
                sky_pan = dict(zip(new_list(list("坎坤震巽乾兌艮離"), "坎"),  a))
                sky_pan2 = sky_pan
                
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
            d1 = list(d[eight_gua.index(zhishi_lokgong_g)].values())[0]
        
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
        return {"排局": [qimen_ju, self.jieqi, daygangzhi+"日", hourgangzhi+"時"], "空亡": self.daykong_shikong() , "值符":zhifu_zhishi1[0][0]["值符"], "直使":zhifu_zhishi1[0][0]["直使"], "天乙":tianyi, "天地盤":{ "地盤":earth_pan, "天盤":sky_pan}, "八星":star_new_dict, "八門":door_new_dict, "八神":god_new_dict}, d, d1


        


print(Qimen(2020,5,23, 17, "小滿").result())
