# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
import sxtwl, re, time
import itertools
import math, datetime, re, ephem

class Qimen:
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.jieqi = re.findall('..', '春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水驚蟄')
        self.findyuen_dict = dict(zip(list(map(lambda x:tuple(x), [self.new_list(self.jiazi(), i)[0:5] for i in self.jiazi()[0::5]])), ["上元","中元","下元"]*4))
        self.liujiashun_dict = dict(zip(list(map(lambda x: tuple(x), [self.new_list(self.jiazi(), i)[0:10] for i in self.jiazi()[0::10]])), self.jiazi()[0::10]))
        self.jieqi_all = self.new_list(self.jieqi, "冬至")
        self.yingyang_dun = {tuple(self.jieqi_all[0:12]):"陽遁",tuple(self.jieqi_all[12:24]):"陰遁" }
        self.cnumber = list("一二三四五六七八九")
        self.door_r = list("休生傷杜景死驚開")
        self.eight_gua = list("坎坤震巽中乾兌艮離")
        self.clockwise_eightgua = list("坎艮震巽離坤兌乾")
        self.Gan = list("甲乙丙丁戊己庚辛壬癸")
        self.Zhi = list("子丑寅卯辰巳午未申酉戌亥")
    
    def jiazi(self):
        tiangan = '甲乙丙丁戊己庚辛壬癸'
        dizhi = '子丑寅卯辰巳午未申酉戌亥'
        jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
        return jiazi
    
    def new_list_r(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append( olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code - 1
        return res1
    
    def new_list(self, olist, o):
        zhihead_code = olist.index(o)
        res1 = []
        for i in range(len(olist)):
            res1.append( olist[zhihead_code % len(olist)])
            zhihead_code = zhihead_code + 1
        return res1
    
    def multi_key_dict_get(self, d, k):
        for keys, v in d.items():
            if k in keys:
                return v
        return None
        
    def find_shier_luck(self, gan):
        twelve_luck = re.findall('..',"長生沐浴冠帶臨冠帝旺") + list("衰病死墓絕胎養")
        twelve_luck_i = list("死病衰") + re.findall('..',"帝旺臨冠冠帶沐浴長生") + list("養胎絕墓")
        yang = dict(zip(self.Gan[0::2], [dict(zip(y, twelve_luck)) for y in [self.new_list(self.Zhi, i) for i in list("亥寅寅巳申")]]))
        ying = dict(zip(self.Gan[1::2], [dict(zip(y, twelve_luck_i)) for y in [self.new_list(self.Zhi, i) for i in list("亥寅寅巳申")]]))
        return {**yang, **ying}.get(gan)
        
    def ecliptic_lon(self, jd_utc):
        s = ephem.Sun(jd_utc)
        equ = ephem.Equatorial(s.ra,s.dec,epoch=jd_utc)
        e= ephem.Ecliptic(equ)
        return e.lon
    
    def sta(self, jd):
        e=self.ecliptic_lon(jd)
        n=int(e*180.0/math.pi/15)
        return n
    
    def iteration(self, jd):
        s1=self.sta(jd)
        s0=s1
        dt=1.0
        while True:
            jd+=dt
            s=self.sta(jd)
            if s0!=s:
                s0=s
                dt=-dt/2
            if abs(dt)<0.0000001 and s!=s1:
                break
        return jd
    
    def fjqs(self, year, month, day, hour):
        jd = ephem.Date( str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2)+" "+str(hour).zfill(2)+":00:00.00")
        ct = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S")
        e=self.ecliptic_lon(jd)
        n=int(e*180.0/math.pi/15)+1
        c = []
        for i in range(1):
            if n>=24:
                n-=24
            jd = self.iteration(jd)
            d = ephem.Date(jd+1/3).tuple()
            b = [self.jieqi[n], datetime.datetime.strptime(str(d[0])+"-"+str(d[1])+"-"+str(d[2])+"-"+str(d[3])+":00:00", "%Y-%m-%d-%H:%M:%S")]
            c.append(b)
        return c[0]
    
    def jq(self, year, month, day, hour):
        jd= ephem.Date( str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2)+" "+str(hour).zfill(2)+":00:00.00")
        ct = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S")
        p = ct - datetime.timedelta(days=7)
        pp = ct - datetime.timedelta(days=21)
        bf = self.fjqs(p.year, p.month, p.day, p.hour)
        bbf = self.fjqs(pp.year, pp.month, pp.day, pp.hour)
        t1 = bf[1]
        t2 = bbf[1]
        if ct < t1:
            return bbf[0]
        else:
            return bf[0]

    #找節氣
    def find_jieqi(self):
        return self.jq(self.year, self.month, self.day, self.hour)
    
    #奇門排局
    def qimen_ju_name(self):
        find_yingyang = self.multi_key_dict_get(self.yingyang_dun, self.find_jieqi())
        findyuen = self.multi_key_dict_get(self.findyuen_dict, self.gangzhi()[2])
        jieqidun_code = {("冬至", "驚蟄"): "一七四", 
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
        jieqicode = self.multi_key_dict_get(jieqidun_code, self.find_jieqi())
        find_kok = {"上元":jieqicode[0], "中元":jieqicode[1], "下元":jieqicode[2]}
        return find_yingyang+find_kok.get(findyuen)+"局"+findyuen
    
    #三元
    def find_yuen(self):
        find_yingyang = multi_key_dict_get(self.yingyang_dun, self.find_jieqi())
        findyuen = multi_key_dict_get(self.findyuen_dict, self.gangzhi()[2])
        return findyuen
    
    #干支
    def gangzhi(self):
        if self.hour == 23:
            d = datetime.datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day)+"-"+str(self.hour)+":00:00", "%Y-%m-%d-%H:%M:%S") + datetime.timedelta(hours=1)
        else:
            d = datetime.datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day)+"-"+str(self.hour)+":00:00", "%Y-%m-%d-%H:%M:%S") 
        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        yTG = self.Gan[cdate.getYearGZ().tg] + self.Zhi[cdate.getYearGZ().dz]
        mTG = self.Gan[cdate.getMonthGZ().tg] + self.Zhi[cdate.getMonthGZ().dz]
        dTG  = self.Gan[cdate.getDayGZ().tg] + self.Zhi[cdate.getDayGZ().dz]
        hTG = self.Gan[cdate.getHourGZ(d.hour).tg] + self.Zhi[cdate.getHourGZ(d.hour).dz]
        return [yTG, mTG, dTG, hTG]
    #旬
    def shun(self, gz):
        shunlist = {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}
        gangzhi = gz
        gangzhi_gang = dict(zip(self.Gan, list(range(1,11))))
        gangzhi_zhi = dict(zip(self.Zhi, list(range(1,13))))
        gang = gangzhi_gang.get(gangzhi[0])
        zhi = gangzhi_zhi.get(gangzhi[1])
        shun_value =  zhi - gang
        if shun_value < 0:
            shun_value = shun_value+12
        return shunlist.get(shun_value)
    
    #奇門局日
    def qimen_ju_day(self):
        day_gangzhi = self.gangzhi()[2]
        ju_day_dict = {tuple(list("甲己")):"甲己日",  tuple(list("乙庚")):"乙庚日",  tuple(list("丙辛")):"丙辛日", tuple(list("丁壬")):"丁壬日", tuple(list("戊癸")):"戊癸日"}
        try:
            find_d = self.multi_key_dict_get(ju_day_dict, day_gangzhi[0])
        except TypeError:
            find_d = self.multi_key_dict_get(ju_day_dict, day_gangzhi[1])
        return find_d
    
    #日空時空
    def daykong_shikong(self):
        guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
        return {"日空":self.multi_key_dict_get(guxu, self.multi_key_dict_get(self.liujiashun_dict, self.gangzhi()[2])).get("孤"), "時空":self.multi_key_dict_get(guxu, self.multi_key_dict_get(self.liujiashun_dict, self.gangzhi()[3])).get("孤")}
    
    #值符
    def hourganghzi_zhifu(self):
        liujiashun_dict2 = dict(zip(list(map(lambda x: tuple(x), [self.new_list(self.jiazi(), i)[0:10] for i in self.jiazi()[0::10]])), [self.jiazi()[0::10][i] + self.Gan[4:10][i]  for i in range(0,5)]))
        return self.multi_key_dict_get(liujiashun_dict2, self.gangzhi()[3])
    
    #地盤
    def pan_earth(self):
        kok = self.qimen_ju_name()[2]
        yingyang_order = {"陽遁":list("戊己庚辛壬癸丁丙乙"),"陰遁":list("戊乙丙丁癸壬辛庚己")}
        kok_yingyang = self.qimen_ju_name()[0:2]
        cnum_to_gua = dict(zip(self.cnumber, self.eight_gua))
        new_gua = [cnum_to_gua.get(i) for i in self.new_list(self.cnumber, kok)]
        earth = dict(zip(new_gua, yingyang_order.get(kok_yingyang)))
        reverse_earth = dict(zip(yingyang_order.get(kok_yingyang), new_gua))
        cnumngua = dict(zip(self.new_list(self.cnumber, kok), yingyang_order.get(kok_yingyang)))
        clockwise_gan = [cnumngua.get(i) for i in  list("一八三四九二七六")]
        return [earth, reverse_earth, clockwise_gan]
    
    #天盤
    def pan_sky(self):
        rotate = {"陽":self.clockwise_eightgua, "陰":list(reversed(self.clockwise_eightgua)) }.get(self.qimen_ju_name()[0])
        earth = self.pan_earth()
        fu_head = self.hourganghzi_zhifu()[2]
        fu_location = earth[1].get(self.gangzhi()[3][0])
        fu_head_location = self.zhifu_n_zhishi().get("值符星宮")[1]
        fu_head_location2 = earth[1].get(fu_head)
        zhishi = self.zhifu_n_zhishi()["值使門宮"][1]
        zhifu_g = self.zhifu_n_zhishi()["值符星宮"][1]
        zhifu = self.zhifu_n_zhishi()["值符星宮"][0]
        if fu_head_location == "中":
            gong_reorder = self.new_list(rotate, "坤")
            try:
                gan_reorder = self.new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
                gong_reorder = self.new_list(rotate,  fu_head_location)
                return dict(zip(gong_reorder, gan_reorder))
            except ValueError:
                try:    
                    return dict(zip(gong_reorder, gan_reorder)), [{'坤':fu_head}]       
                except UnboundLocalError:
                    return self.pan_earth()
        elif fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            gan_reorder = self.new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
            gong_reorder = self.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:    
                start = dict(zip(self.cnumber, gan_reorder)).get(self.qimen_ju_name()[2])
                rgan_reorder = self.new_list(gan_reorder , start)
                rgong_reorder = self.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, rgan_reorder)), dict(zip(rgan_reorder, rgong_reorder))
            elif fu_head in gan_reorder: 
                if fu_location == None:
                    return  self.pan_earth()
                elif fu_location != None:
                    rgan_reorder = self.new_list(gan_reorder , earth[0].get(fu_location))
                    rgong_reorder = self.new_list(gong_reorder , fu_location)
                    return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth()[0].get("中") } }
        elif fu_head_location != "中" and zhifu == "禽" and fu_head_location2 == "中":
            gan_reorder = self.new_list([self.pan_earth()[0].get(i) for i in list(rotate)], earth[0].get("坤"))
            gong_reorder = self.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:    
                rgong_reorder = self.new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, gan_reorder)), dict(zip(gan_reorder, rgong_reorder))
            elif fu_head in gan_reorder: 
                rgan_reorder = self.new_list(gan_reorder , earth[0].get(fu_location))
                rgong_reorder = self.new_list(gong_reorder , fu_location)
                return {**dict(zip(gong_reorder,gan_reorder)),**{"中":self.pan_earth()[0].get("中") } }
            
    #八門
    def pan_door(self):
        starting_door = self.zhifu_n_zhishi().get("值使門宮")[0]
        starting_gong = self.zhifu_n_zhishi().get("值使門宮")[1]
        rotate = {"陽":self.clockwise_eightgua, "陰":list(reversed(self.clockwise_eightgua))}.get(self.qimen_ju_name()[0])
        door_reorder = {"陽":self.new_list(self.door_r, starting_door), "陰":self.new_list(list(reversed(self.door_r)), starting_door)}.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = self.new_list(rotate, "坤")
        else:
            gong_reorder = self.new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,door_reorder))
    
    #九星
    def pan_star(self):
        star_r = list("蓬任沖輔英禽柱心")
        starting_star = self.zhifu_n_zhishi().get("值符星宮")[0].replace("芮", "禽")
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":self.clockwise_eightgua, "陰":list(reversed(self.clockwise_eightgua))}.get(self.qimen_ju_name()[0])
        star_reorder = {"陽":self.new_list(star_r, starting_star), "陰":self.new_list(list(reversed(star_r)), starting_star)}.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = self.new_list(rotate, "坤")
        else:
            gong_reorder = self.new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,star_reorder)), dict(zip(star_reorder, gong_reorder))
    
    #八神
    def pan_god(self):
        god_dict = {"陽":list("符蛇陰合勾雀地天"),"陰":list("符蛇陰合虎玄地天")}
        god_order = god_dict.get(self.qimen_ju_name()[0])
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":self.clockwise_eightgua, "陰":list(reversed(self.clockwise_eightgua)) }.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = self.new_list(rotate, "坤")
        else:
            gong_reorder = self.new_list(rotate, starting_gong)
        
        return dict(zip(gong_reorder,god_order))
    
    #排值符
    def zhifu_pai(self):
        yinyang = self.qimen_ju_name()[0]
        kook = self.qimen_ju_name()[2]
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
        pai = paiyinyang.get(yinyang).get(kook)
        return {"陰":dict(zip(self.jiazi()[0::10], [i+pai for i in self.new_list_r(self.cnumber, kook)[0:6]])), "陽":dict(zip(self.jiazi()[0::10], [i+pai for i in self.new_list(self.cnumber, kook)[0:6]]))}.get(yinyang)
   
    #排值使
    def zhishi_pai(self):
        yinyang = self.qimen_ju_name()[0]
        kook = self.qimen_ju_name()[2]
        yanglist = "".join(self.new_list(self.cnumber, kook))+"".join(self.new_list(self.cnumber, kook))+"".join(self.new_list(self.cnumber, kook))
        yinlist =  "".join(self.new_list_r(self.cnumber, kook))+"".join(self.new_list_r(self.cnumber, kook))+"".join(self.new_list_r(self.cnumber, kook))
        yangpai = dict(zip(self.jiazi()[0::10], [i+ yanglist[yanglist.index(i)+1:][0:11] for i in self.new_list(self.cnumber, kook)[0:6]]))
        yinpai = dict(zip(self.jiazi()[0::10], [i+ yinlist[yinlist.index(i)+1:][0:11] for i in self.new_list_r(self.cnumber, kook)[0:6]]))
        return {"陰":yinpai, "陽":yangpai}.get(yinyang)
    
    #找值符及值使
    def zhifu_n_zhishi(self):
        stars_code = dict(zip(self.cnumber, list("蓬芮沖輔禽心柱任英")))
        doors_code = dict(zip(self.cnumber, list("休死傷杜中開驚生景")))
        gongs_code = dict(zip(self.cnumber, self.eight_gua))
        gans_code = dict(zip(self.Gan,range(0,11)))
        hgan = gans_code.get(self.gangzhi()[3][0])
        chour = self.multi_key_dict_get(self.liujiashun_dict, self.gangzhi()[3])
        star = dict(zip(list(self.zhifu_pai().keys()), [stars_code.get(i[0]) for i in list(self.zhifu_pai().values())])).get(chour)
        door = dict(zip(list(self.zhishi_pai().keys()), [doors_code.get(i[0]) for i in list(self.zhishi_pai().values())])).get(chour)
        if door == "中":
            door = "死"
        zhifu_gong = dict(zip(list(self.zhifu_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhifu_pai().values())])).get(chour)
        zhishi_gong = dict(zip(list(self.zhishi_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhishi_pai().values())])).get(chour)
        return {"值符星宮":[star,zhifu_gong], "值使門宮":[door,zhishi_gong]}
    
    #九宮長生十二神
    def gong_chengsun(self):
        find_twelve_luck = self.find_shier_luck(self.gangzhi()[2][0])
        zhi2gan = dict(zip(self.Zhi,list("癸己甲乙戊丙丁己庚辛戊壬")))
        find_twelve_luck_new = dict(zip([zhi2gan.get(i) for i in list(find_twelve_luck.keys())],list(find_twelve_luck.values())))
        sky_pan = self.pan_sky()
        sky_pan_new = dict(zip(sky_pan.keys(),[{list(sky_pan.values())[y]: [find_twelve_luck_new.get(i) for i in sky_pan.values()][y]} for y in range(0,8)]))
        earth_pan = self.pan_earth()[0]
        earth_pan_new = earth_pan_new = dict(zip(earth_pan.keys(),[{list(earth_pan.values())[y]: [find_twelve_luck_new.get(i) for i in earth_pan.values()][y]} for y in range(0,9)]))
        return {"天盤":sky_pan_new, "地盤": earth_pan_new}
    
    def pan(self):
        return {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時","旬首":self.shun(self.gangzhi()[2]),"旬空":self.daykong_shikong(),"局日":self.qimen_ju_day(), "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "值符值使":self.zhifu_n_zhishi(), "天乙":self.tianyi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star()[0], "神":self.pan_god(), "馬星": {"天馬": self.moonhorse(),"丁馬":self.dinhorse(), "驛馬":self.hourhorse()}, "長生運": self.gong_chengsun()}
  
    def pan2(self):
        key = self.eight_gua
        sky = self.pan_sky()[0]
        earth = self.pan_earth()[0]
        star = self.pan_star()[0]
        door = self.pan_door()
        god = self.pan_god()
        return [[sky.get(i), earth.get(i), i,  door.get(i), star.get(i)] for i in key]
  
  
    def pan_html(self):
        god = self.pan_god()
        door = self.pan_door()
        star = self.pan_star()[0]
        sky = self.pan_sky()[0]
        earth = self.pan_earth()[0]
        a = ''' <div class="container"><table style="width:100%"><tr>'''+"".join(['''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''' for i in list("巽離坤")])+"</tr>"
        b = ['''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''' for i in list("震兌")]
        c = '''<tr>'''+b[0]+ '''<td><br><br></td>'''+b[1]+'''</tr>'''
        d = "<tr>"+"".join(['''<td align="center">'''+sky.get(i)+god.get(i)+door.get(i) +"<br>"+ earth.get(i)+star.get(i)+ i+'''</td>''' for i in list("艮坎乾")])+"</tr></table></div>"
        return a+c+d
   
    def gpan(self):
        start_jia = self.jiazi()[0::10]
        find_shun = dict(zip([tuple(self.new_list(self.jiazi(), i)[0:10]) for i in start_jia], start_jia))
        dgz = self.gangzhi()[2]
        shun = self.multi_key_dict_get(find_shun, dgz)
        start_gong_d = {"冬至": "艮離坎坤震巽", "夏至":"坤離巽坤離兌"}
        yy_dun = {"冬至":"陽遁", "夏至":"陰遁"}
        start_gong = start_gong_d.get(self.multi_key_dict_get({tuple(self.jieqi_all[0:12]):"冬至", tuple(self.jieqi_all[12:24]):"夏至"}, self.find_jieqi()))
        yy = yy_dun.get(self.multi_key_dict_get({tuple(self.jieqi_all[0:12]):"冬至", tuple(self.jieqi_all[12:24]):"夏至"}, self.find_jieqi()))
        gong = dict(zip(start_jia, start_gong)).get(shun)
        triple_list = list(map(lambda x: x + x + x, list(range(0,21))))
        b = []
        for i in range(0, len(triple_list)):
            try:
                a = tuple(self.jiazi()[triple_list[i]: triple_list[i+1]])
                b.append(a)
            except IndexError:
                pass

        g =[]
        f = {"陰遁":list(reversed(self.clockwise_eightgua)) ,"陽遁":self.clockwise_eightgua}
        c_gong = self.new_list(self.eight_gua, gong)
        a_gong = self.new_list(list(reversed(self.eight_gua)), gong)
        close_ten_day = self.new_list(self.jiazi(), shun)[0:10]
        golen_d = re.findall("..","太乙攝提軒轅招搖天符青龍咸池太陰天乙")
        ying = dict(zip(self.new_list(self.eight_gua, {**dict(zip(close_ten_day, a_gong)), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), golen_d))
        yang = dict(zip(self.new_list(self.eight_gua, {**dict(zip(close_ten_day, c_gong)), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), golen_d))
        star = {"陰遁":ying ,"陽遁":yang}.get(yy)
        for i in list("坎坤震巽乾兌艮離"):
            c = dict(zip(self.new_list(f.get(yy), i), self.door_r))
            g.append(c)
        e = itertools.cycle(g)
        door = self.multi_key_dict_get(dict(zip(b, e)), dgz)
        return {
                    "局": yy+dgz+"日",
                    "鶴神": self.crane_god().get(dgz),
                    "星": star,
                    "門": {**door, **{"中":""}},
                    "神": self.getgtw().get(dgz[0])
                    }
            
    def getgtw(self):
        newgtw_order = re.findall("..","地籥天關唐符風雲唐符風雲雷公風伯天曹五符")
        gtw = re.findall("..","地籥六賊五符天曹地符風伯雷公雨師風雲唐符國印天關")
        newgtw = [self.new_list(gtw, i) for i in newgtw_order]
        newgtw_list = [dict(zip(self.Zhi, i)) for i in newgtw]
        return dict(zip(self.Gan, newgtw_list))

    #鶴神 
    def crane_god(self):
        newjz = self.new_list(self.jiazi(), "庚申")
        crane_nums = [6,5,6,5,6,5,16,6,5]
        crane_list = list("巽離坤兌乾坎天艮震")
        newc_list = []
        for i in range(0,8):
            newc = [crane_list[i][:5]]*crane_nums[i]
            newc_list.extend(newc)
        return dict(zip(newjz, newc_list))
            
    def gpan_html(self):
        god = self.gpan().get("神")
        door = self.gpan().get("門")
        star = self.gpan().get("星")
        a = ''' <div class="container"><table style="width:100%"><tr>'''+"".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("巽離坤")])+"</tr>"
        b = "".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("震中兌")])
        d = "<tr>"+"".join(['''<td align="center">'''+star.get(i) +"<br>"+ door.get(i)+ i+'''</td>''' for i in list("艮坎乾")])+"</tr></table></div>"
        return a+b+d
    
    def five_html(self):
        e = ['''<td align="center">'''+i+ '''<br>'''+god.get(i)+'''</td>''' for i in self.Zhi]
        c = "<div><table><tr>"+e[0]+e[1]+e[2]+"</tr><tr>"+e[3]+e[4]+e[5]+"</tr><tr>"+e[6]+e[7]+e[8]+"</tr><tr>"+e[9]+e[10]+e[11]+"</tr></table></div>"
        return c
    

    #天乙
    def tianyi(self):
        stars_gong_code = dict(zip(self.eight_gua, list("蓬芮沖輔禽心柱任英")))
        try:
            star_location = stars_gong_code.get(self.zhifu_n_zhishi().get("值符星宮")[1])
        except IndexError:
            star_location = "禽"
        return star_location

    #丁馬
    def dinhorse(self):
        dinhorsedict =dict(zip(re.findall("..","甲子甲戌甲申甲午甲辰甲寅"), list("卯丑亥酉未巳")))
        shun = self.multi_key_dict_get(self.liujiashun_dict, self.gangzhi()[2])
        return self.multi_key_dict_get(dinhorsedict, shun)
    
    #天馬
    def moonhorse(self):
        moonhorsedict = dict(zip([tuple(i) for i in re.findall("..","寅申卯酉辰戌巳亥午子丑未")], list("午申戌子寅辰")))
        return self.multi_key_dict_get(moonhorsedict, self.gangzhi()[2][1])
    
    #驛馬星
    def hourhorse(self):
        yima = dict(zip([tuple(i) for i in re.findall("...","申子辰寅午戌亥卯未巳酉丑")], list("寅申巳亥")))
        return self.multi_key_dict_get(yima, self.gangzhi()[3][1])
    
    def overall(self):
        return {"時家奇門": self.pan(), "金函玉鏡": self.gpan()}

if __name__ == '__main__':
    tic = time.perf_counter()
    print(Qimen(2015,7,20,10).pan())
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")