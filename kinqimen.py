# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
import re
import time
import itertools
import config
import datetime


class Qimen:
    def __init__(self, year, month, day, hour, minute):
        self.year, self.month, self.day, self.hour, self.minute = year, month, day, hour, minute

     #上中下元
    def year_yuen(self):
        w = [(i * 60) + 4 for i in range(22,100)]
        three_yuen = itertools.cycle([i+"元甲子" for i in list("上中下")])
        for i in w:
            if self.year < i:
                break
        yuen = dict(zip(w, three_yuen)).get(w[w.index(i)-1])
        return [yuen, w[w.index(i)-1]]
    #奇門局日
    def qimen_ju_day(self):
        ju_day_dict = {tuple(list("甲己")):"甲己日",  tuple(list("乙庚")):"乙庚日",  tuple(list("丙辛")):"丙辛日", tuple(list("丁壬")):"丁壬日", tuple(list("戊癸")):"戊癸日"}
        try:
            find_d = config.multi_key_dict_get(ju_day_dict, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2][0])
        except TypeError:
            find_d = config.multi_key_dict_get(ju_day_dict, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2][1])
        return find_d
    #有正授，有超神，有閏奇，有接氣
    def qimen_ju_day_zhirun(self):
        ju_day_dict = {tuple(["甲子", "甲午", "己卯", "己酉"]):"上元", tuple(["甲寅","甲申", "己巳", "己亥"]):"中元", tuple(["甲辰", "甲戌", "己丑", "己未"]):"下元"}
        Jieqi = config.jq(self.year, self.month, self.day, self.hour, self.minute)
        dgz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]
        if dgz in ["甲子", "甲午", "己卯", "己酉", "甲寅","甲申", "己巳", "己亥", "甲辰", "甲戌", "己丑", "己未"]:
            dgz_dist = "日干是符頭"
        else:
            dgz_dist = "日干非符頭"
        Jieqi_disance = config.jq_distance(self.year, self.month, self.day, self.hour, self.minute)[0].get(Jieqi)
        current = config.jq_distance(self.year, self.month, self.day, self.hour, self.minute)[1]
        difference = datetime.datetime.strptime(current, "%Y/%m/%d %H:%M:%S") >  datetime.datetime.strptime(Jieqi_disance, "%Y/%m/%d %H:%M:%S")
        difference1 = datetime.datetime.strptime(current, "%Y/%m/%d %H:%M:%S") - datetime.datetime.strptime(Jieqi_disance, "%Y/%m/%d %H:%M:%S")
        
        if dgz_dist == "日干是符頭" and difference == True:
            return "超神"
        if dgz_dist == "日干非符頭" and difference == True:
            return "接氣"
        if dgz_dist == "日干是符頭" and difference1 > 0:
            return  "正授"
        #return config.multi_key_dict_get(ju_day_dict, dict(zip(config.jiazi(),list(itertools.chain.from_iterable([[i]*5 for i in config.jiazi()[0::5]])))).get(dgz)), Jieqi, dgz, dgz_dist, difference, current,Jieqi_disance 
    
    #值符
    def hourganghzi_zhifu(self):
        return config.multi_key_dict_get(dict(zip(list(map(lambda x: tuple(x), list(map(lambda x: config.new_list(config.jiazi(), x)[0:10], config.jiazi()[0::10])))), list(map(lambda x: config.jiazi()[0::10][x] + config.tian_gan[4:10][x], list(range(0,6)))))), config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3])
    #分值符
    def hourganghzi_zhifu_minute(self):
        return config.multi_key_dict_get(dict(zip(list(map(lambda x: tuple(x), list(map(lambda x: config.new_list(config.jiazi(), x)[0:10], config.jiazi()[0::10])))), list(map(lambda x: config.jiazi()[0::10][x] + config.tian_gan[4:10][x], list(range(0,6)))))), config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[4])
    #地盤
    def pan_earth(self):
        return dict(zip(list(map(lambda x: dict(zip(config.cnumber, config.eight_gua)).get(x), config.new_list(config.cnumber, config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)[2]))), {"陽遁":list("戊己庚辛壬癸丁丙乙"),"陰遁":list("戊乙丙丁癸壬辛庚己")}.get(config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)[0:2])))
    #地盤
    def pan_earth_minute(self):
        return dict(zip(list(map(lambda x: dict(zip(config.cnumber, config.eight_gua)).get(x), config.new_list(config.cnumber, config.qimen_ju_name_ke(self.year, self.month, self.day, self.hour, self.minute)[2]))), {"陽遁":list("戊己庚辛壬癸丁丙乙"),"陰遁":list("戊乙丙丁癸壬辛庚己")}.get(config.qimen_ju_name_ke(self.year, self.month, self.day, self.hour, self.minute)[0:2])))
    
    #逆地盤
    def pan_earth_r(self):
        return dict(zip(list(self.pan_earth().values()), list(self.pan_earth().keys())))
    
    def pan_earth_min_r(self):
        return dict(zip(list(self.pan_earth_minute().values()), list(self.pan_earth_minute().keys())))
    
    #天盤
    def pan_sky(self):
        rotate = {"陽":config.clockwise_eightgua, "陰":list(reversed(config.clockwise_eightgua)) }.get(config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)[0])
        fu_head = self.hourganghzi_zhifu()[2]
        fu_location = self.pan_earth_r().get(config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][0])
        fu_head_location = config.zhifu_n_zhishi(self.year, self.month, self.day, self.hour, self.minute).get("值符星宮")[1]
        fu_head_location2 = self.pan_earth_r().get(fu_head)
        zhifu = config.zhifu_n_zhishi(self.year, self.month, self.day, self.hour, self.minute)["值符星宮"][0]
        #zhifu2 = config.zhifu_n_zhishi(self.year, self.month, self.day, self.hour, self.minute)
        if fu_head_location == "中":
            gong_reorder = config.new_list(rotate, "坤")
            try:
                gan_reorder, gong_reorder= config.new_list(list(map(lambda x: self.pan_earth().get(x), list(rotate))), fu_head),  config.new_list(rotate,  fu_head_location)
                return dict(zip(gong_reorder, gan_reorder))
            except ValueError:
                return dict(zip(list(reversed(gong_reorder)), config.new_list(list(map(lambda x: self.pan_earth().get(x), list(reversed(rotate)))), self.pan_earth().get("坤")) ))
        if fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            gan_reorder = config.new_list(list(map(lambda x:self.pan_earth().get(x), list(rotate))), fu_head)
            gong_reorder = config.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:
                start = dict(zip(config.cnumber, gan_reorder)).get(config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)[2])
                rgan_reorder = config.new_list(gan_reorder , start)
                rgong_reorder = config.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, rgan_reorder)), dict(zip(rgan_reorder, rgong_reorder))
            if fu_head in gan_reorder:
                if fu_location == None:
                    return  self.pan_earth()
                elif fu_location != None:
                    return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth().get("中") } }
        if fu_head_location != "中" and zhifu == "禽" and fu_head_location2 == "中":
            gan_reorder = config.new_list(list(map(lambda x: self.pan_earth().get(x), list(rotate))), self.pan_earth().get("坤"))
            gong_reorder = config.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:
                rgong_reorder = config.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, gan_reorder))
            if fu_head in gan_reorder:
                return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth()[0].get("中") } }
            
    #天盤分
    def pan_sky_minute(self):
        rotate = {"陽":config.clockwise_eightgua, "陰":list(reversed(config.clockwise_eightgua)) }.get(config.qimen_ju_name_ke(self.year, self.month, self.day, self.hour, self.minute)[0])
        fu_head = self.hourganghzi_zhifu_minute()[2]
        fu_location = self.pan_earth_min_r().get(config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[4][0])
        fu_head_location = config.zhifu_n_zhishi_ke(self.year, self.month, self.day, self.hour, self.minute).get("值符星宮")[1]
        fu_head_location2 = self.pan_earth_min_r().get(fu_head)
        zhifu = config.zhifu_n_zhishi_ke(self.year, self.month, self.day, self.hour, self.minute)["值符星宮"][0]
        #zhifu2 = config.zhifu_n_zhishi_ke(self.year, self.month, self.day, self.hour, self.minute)
        if fu_head_location == "中":
            gong_reorder = config.new_list(rotate, "坤")
            try:
                gan_reorder, gong_reorder= config.new_list(list(map(lambda x: self.pan_earth().get(x), list(rotate))), fu_head),  config.new_list(rotate,  fu_head_location)
                return dict(zip(gong_reorder, gan_reorder))
            except ValueError:
                return dict(zip(list(reversed(gong_reorder)), config.new_list(list(map(lambda x: self.pan_earth().get(x), list(reversed(rotate)))), self.pan_earth().get("坤")) ))
        if fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            gan_reorder = config.new_list(list(map(lambda x:self.pan_earth_minute().get(x), list(rotate))), fu_head)
            gong_reorder = config.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:
                start = dict(zip(config.cnumber, gan_reorder)).get(config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)[2])
                rgan_reorder = config.new_list(gan_reorder , start)
                rgong_reorder = config.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, rgan_reorder)), dict(zip(rgan_reorder, rgong_reorder))
            if fu_head in gan_reorder:
                if fu_location == None:
                    return  self.pan_earth_minute()
                elif fu_location != None:
                    return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth_minute().get("中") } }
        if fu_head_location != "中" and zhifu == "禽" and fu_head_location2 == "中":
            gan_reorder = config.new_list(list(map(lambda x: self.pan_earth_minute().get(x), list(rotate))), self.pan_earth_minute().get("坤"))
            gong_reorder = config.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:
                rgong_reorder = config.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, gan_reorder))
            if fu_head in gan_reorder:
                return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth_minute()[0].get("中") } }
    #九宮長生十二神
    def gong_chengsun(self):
        sky = self.pan_sky()
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        find_twelve_luck = config.find_shier_luck(gz[2][0])
        di_zhi_mapping = dict(zip(config.di_zhi, list("癸己甲乙戊丙丁己庚辛戊壬")))
        find_twelve_luck_new = {di_zhi_mapping.get(k): v for k, v in find_twelve_luck.items()}
        try:
            sky_pan = sky[0]
            sky_pan_new = {k: {v: find_twelve_luck_new.get(k)} for k, v in sky_pan.items()}
        except KeyError:
             sky_pan = sky
             sky_pan_new = dict(zip(list(sky_pan.keys()), list(map(lambda i:{i:find_twelve_luck_new.get(i)}, list(sky_pan.values())))))
        earth_pan = self.pan_earth()
        earth_pan_new = {k: {v: find_twelve_luck_new.get(v)} for k, v in earth_pan.items()}
        return {"天盤": sky_pan_new, "地盤": earth_pan_new}
    
    def gong_chengsun_minute(self):
        sky = self.pan_sky_minute()
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        find_twelve_luck = config.find_shier_luck(gz[3][0])
        di_zhi_mapping = dict(zip(config.di_zhi, list("癸己甲乙戊丙丁己庚辛戊壬")))
        find_twelve_luck_new = {di_zhi_mapping.get(k): v for k, v in find_twelve_luck.items()}
        try:
            sky_pan = sky[0]
            sky_pan_new = {k: {v: find_twelve_luck_new.get(k)} for k, v in sky_pan.items()}
        except KeyError:
             sky_pan = sky
             sky_pan_new = dict(zip(list(sky_pan.keys()), list(map(lambda i:{i:find_twelve_luck_new.get(i)}, list(sky_pan.values())))))
        earth_pan = self.pan_earth()
        earth_pan_new = {k: {v: find_twelve_luck_new.get(v)} for k, v in earth_pan.items()}
        return {"天盤": sky_pan_new, "地盤": earth_pan_new}


    def pan(self):
        # Calculate gangzhi once and store the result for reuse
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        gzd = "{}年{}月{}日{}時".format(gz[0], gz[1], gz[2], gz[3], gz[4])
        shunhead = config.shun(gz[2])
        shunkong = config.daykong_shikong(self.year, self.month, self.day, self.hour, self.minute)
        paiju = config.qimen_ju_name(self.year, self.month, self.day, self.hour, self.minute)
        j_q = config.jq(self.year, self.month, self.day, self.hour, self.minute)
        zfzs = config.zhifu_n_zhishi(self.year, self.month, self.day, self.hour, self.minute)
        pan_star_result = config.pan_star(self.year, self.month, self.day, self.hour, self.minute)
        star = pan_star_result[0]
        door = config.pan_door(self.year, self.month, self.day, self.hour, self.minute)
        god = config.pan_god(self.year, self.month, self.day, self.hour, self.minute)
        return {
            "干支": gzd,
            "旬首": shunhead,
            "旬空": shunkong,
            "局日": self.qimen_ju_day(),
            "排局": paiju,
            "節氣": j_q,
            "值符值使": zfzs,
            "天乙": self.tianyi(),
            "天盤": self.pan_sky(),
            "地盤": self.pan_earth(),
            "門": door,
            "星": star,
            "神": god,
            "馬星": {
                "天馬": self.moonhorse(),
                "丁馬": self.dinhorse(),
                "驛馬": self.hourhorse()
            },
            "長生運": self.gong_chengsun()
        }
    
    def pan_minute(self):
        # Calculate gangzhi once and store the result for reuse
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        gzd = "{}年{}月{}日{}時{}分".format(gz[0], gz[1], gz[2], gz[3], gz[4])
        shunhead = config.shun(gz[3])
        shunkong = config.hourkong_minutekong(self.year, self.month, self.day, self.hour, self.minute)
        paiju = config.qimen_ju_name_ke(self.year, self.month, self.day, self.hour, self.minute)
        j_q = config.jq(self.year, self.month, self.day, self.hour, self.minute)
        zfzs = config.zhifu_n_zhishi_ke(self.year, self.month, self.day, self.hour, self.minute)
        pan_star_result = config.pan_star_minute(self.year, self.month, self.day, self.hour, self.minute)
        star = pan_star_result[0]
        door = config.pan_door_minute(self.year, self.month, self.day, self.hour, self.minute)
        god = config.pan_god_minute(self.year, self.month, self.day, self.hour, self.minute)
        return {
            "干支": gzd,
            "旬首": shunhead,
            "旬空": shunkong,
            "局日": self.qimen_ju_day(),
            "排局": paiju,
            "節氣": j_q,
            "值符值使": zfzs,
            "天乙": self.tianyi(),
            "天盤": self.pan_sky_minute(),
            "地盤": self.pan_earth_minute(),
            "門": door,
            "星": star,
            "神": god,
            "馬星": {
                "天馬": self.moonhorse(),
                "丁馬": self.dinhorse(),
                "驛馬": self.hourhorse()
            },
            "長生運": self.gong_chengsun_minute()
        }
        
        
    def pan_html(self):
        god, door, star, sky, earth = self.pan_god(), self.pan_door(), self.pan_star()[0],  self.pan_sky(), self.pan_earth()
        a = ''' <div class="container"><table style="width:100%"><tr>'''+"".join(['''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''' for i in list("巽離坤")])+"</tr>"
        b = ['''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''' for i in list("震兌")]
        c = '''<tr>'''+b[0]+ '''<td><br><br></td>'''+b[1]+'''</tr>'''
        d = "<tr>"+"".join(list(map(lambda i: '''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''',list("艮坎乾"))))+"</tr></table></div>"
        return a+c+d

    def ypan(self):
        kok = {"上元甲子":"陰一局", "中元甲子":"陰四局", "下元甲子":"陰七局"}.get(self.year_yuen()[0])
        #start = {"上元甲子":"坎", "中元甲子":"巽", "下元甲子":"兌"}.get(self.year_yuen()[0])
        return kok

    def gpan(self):
        start_jia = config.jiazi()[0::10]
        dgz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]
        shun = config.multi_key_dict_get(dict(zip([tuple(config.new_list(config.jiazi(), i)[0:10]) for i in start_jia], start_jia)), dgz)
        yy = {"冬至":"陽遁", "夏至":"陰遁"}.get(config.multi_key_dict_get({tuple(config.jieqi_name[0:12]):"冬至", tuple(config.jieqi_name[12:24]):"夏至"}, config.jq(self.year, self.month, self.day, self.hour, self.minute)))
        gong = dict(zip(start_jia, {"冬至": "艮離坎坤震巽", "夏至":"坤離巽坤離兌"}.get(config.multi_key_dict_get({tuple(config.jieqi_name[0:12]):"冬至", tuple(config.jieqi_name[12:24]):"夏至"}, config.jq(self.year, self.month, self.day,self.hour, self.minute))))).get(shun)
        triple_list = list(map(lambda x: x + x + x, list(range(0,21))))
        b = []
        for i in range(0, len(triple_list)):
            try:
                a = tuple(config.jiazi()[triple_list[i]: triple_list[i+1]])
                b.append(a)
            except IndexError:
                pass
        g =[]
        close_ten_day = config.new_list(config.jiazi(), shun)[0:10]
        a_gong = config.new_list(list(reversed(config.eight_gua)), gong)
        ying = dict(zip(config.new_list(config.eight_gua, {**dict(zip(close_ten_day, config.new_list(list(reversed(config.eight_gua)), gong))), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), config.golen_d))
        yang = dict(zip(config.new_list(config.eight_gua, {**dict(zip(close_ten_day, config.new_list(config.eight_gua, gong))), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), config.golen_d))
        for i in list("坎坤震巽乾兌艮離"):
            c = dict(zip(config.new_list({"陰遁":list(reversed(config.clockwise_eightgua)) ,"陽遁":config.clockwise_eightgua}.get(yy), i), config.door_r))
            g.append(c)
        return {
                    "局": yy+dgz+"日",
                    "鶴神": self.crane_god().get(dgz),
                    "星": {"陰遁":ying ,"陽遁":yang}.get(yy),
                    "門": {**config.multi_key_dict_get(dict(zip(b, itertools.cycle(g))), dgz), **{"中":""}},
                    "神": config.getgtw().get(dgz[0])
                    }
    #鶴神
    def crane_god(self):
        newc_list = list(map(lambda i:[list("巽離坤兌乾坎天艮震")[i][:5]]*[6,5,6,5,6,5,16,6,5][i],list(range(0,8))))
        return dict(zip(config.new_list(config.jiazi(), "庚申"), newc_list))

    def gpan_html(self):
        door = self.gpan().get("門")
        star = self.gpan().get("星")
        a = ''' <div class="container"><table style="width:100%"><tr>'''+"".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("巽離坤")])+"</tr>"
        b = "".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("震中兌")])
        d = "<tr>"+"".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("艮坎乾")])+"</tr></table></div>"
        return a+b+d

    def five_html(self):
        e = ['''<td align="center">'''+i+ '''<br>'''+self.pan_god().get(i)+'''</td>''' for i in config.di_zhi]
        c = "<div><table><tr>"+e[0]+e[1]+e[2]+"</tr><tr>"+e[3]+e[4]+e[5]+"</tr><tr>"+e[6]+e[7]+e[8]+"</tr><tr>"+e[9]+e[10]+e[11]+"</tr></table></div>"
        return c
    #天乙
    def tianyi(self):
        try:
            star_location = dict(zip(config.eight_gua, list("蓬芮沖輔禽心柱任英"))).get(config.zhifu_n_zhishi(self.year, self.month, self.day, self.hour, self.minute).get("值符星宮")[1])
        except IndexError:
            star_location = "禽"
        return star_location
    #丁馬
    def dinhorse(self):
        return config.multi_key_dict_get(dict(zip(re.findall("..","甲子甲戌甲申甲午甲辰甲寅"), list("卯丑亥酉未巳"))), config.multi_key_dict_get(config.liujiashun_dict(), config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]))
    #天馬
    def moonhorse(self):
        return config.multi_key_dict_get(dict(zip(list(map(lambda i:tuple(i), re.findall("..","寅申卯酉辰戌巳亥午子丑未"))), list("午申戌子寅辰"))), config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2][1])
    #驛馬星
    def hourhorse(self):
        return config.multi_key_dict_get(dict(zip(list(map(lambda i:tuple(i), re.findall("...","申子辰寅午戌亥卯未巳酉丑"))), list("寅申巳亥"))), config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])

    def overall(self):
        return { "金函玉鏡(日家奇門)": self.gpan(), "時家奇門": self.pan(), "刻家奇門":self.pan_minute()}
    
    

if __name__ == '__main__':
    tic = time.perf_counter()
    #print(Qimen(2023,11,27,10,4).pan())
    #print(Qimen(2024,1,16,0,0).pan_minute())
    print(Qimen(2024,7,22,22,28).qimen_ju_day_zhirun())
    print(Qimen(2024,7,24,11,56).qimen_ju_day_zhirun())
    #print(config.qimen_ju_name_ke(2023,6,22,18,17))
    #print(config.jq(2023,6,22,18,17))
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")
