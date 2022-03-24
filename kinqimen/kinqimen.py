# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
from kinqimen.config import *
import sxtwl, re
import itertools

class Qimen:
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.p = {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時","旬首":self.shun(self.gangzhi()[2]),"旬空":self.daykong_shikong(),"局日":self.qimen_ju_day(), "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "值符值使":self.zhifu_n_zhishi(), "天乙":self.tianyi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star()[0], "神":self.pan_god(), "馬星": {"天馬": self.moonhorse(),"丁馬":self.dinhorse(), "驛馬":self.hourhorse()}, "長生運": self.gong_chengsun()}
        self.g = self.gpan()
        self.overall = {"時家奇門": self.pan, "金函玉鏡": self.g}
                           
    #找節氣
    def find_jieqi(self):
        return jq(self.year, self.month, self.day, self.hour)
    
    #奇門排局
    def qimen_ju_name(self):
        find_yingyang = multi_key_dict_get(yingyang_dun, self.find_jieqi())
        findyuen = multi_key_dict_get(findyuen_dict, self.gangzhi()[2])
        jieqicode = multi_key_dict_get(jieqidun_code, self.find_jieqi())
        find_kok = {"上元":jieqicode[0], "中元":jieqicode[1], "下元":jieqicode[2]}
        return find_yingyang+find_kok.get(findyuen)+"局"+findyuen
    
    #三元
    def find_yuen(self):
        find_yingyang = multi_key_dict_get(yingyang_dun, self.find_jieqi())
        findyuen = multi_key_dict_get(findyuen_dict, self.gangzhi()[2])
        return findyuen
    
    #干支
    def gangzhi(self):
        if self.hour == 23:
            d = datetime.datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day)+"-"+str(self.hour)+":00:00", "%Y-%m-%d-%H:%M:%S") + datetime.timedelta(hours=1)
        else:
            d = datetime.datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day)+"-"+str(self.hour)+":00:00", "%Y-%m-%d-%H:%M:%S") 
        cdate = sxtwl.fromSolar(d.year, d.month, d.day)
        yTG = Gan[cdate.getYearGZ().tg] + Zhi[cdate.getYearGZ().dz]
        mTG = Gan[cdate.getMonthGZ().tg] + Zhi[cdate.getMonthGZ().dz]
        dTG  = Gan[cdate.getDayGZ().tg] + Zhi[cdate.getDayGZ().dz]
        hTG = Gan[cdate.getHourGZ(d.hour).tg] + Zhi[cdate.getHourGZ(d.hour).dz]
        return [yTG, mTG, dTG, hTG]
  #旬
    def shun(self, gz):
        gangzhi = gz
        gangzhi_gang = dict(zip(Gan, list(range(1,11))))
        gangzhi_zhi = dict(zip(Zhi, list(range(1,13))))
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
            find_d = multi_key_dict_get(ju_day_dict, day_gangzhi[0])
        except TypeError:
            find_d = multi_key_dict_get(ju_day_dict, day_gangzhi[1])
        return find_d
    
    #日空時空
    def daykong_shikong(self):
        return {"日空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, self.gangzhi()[2])).get("孤"), "時空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, self.gangzhi()[3])).get("孤")}

    #值符
    def hourganghzi_zhifu(self):
        return multi_key_dict_get(liujiashun_dict2, self.gangzhi()[3])
    
    #地盤
    def pan_earth(self):
        kok = self.qimen_ju_name()[2]
        kok_yingyang = self.qimen_ju_name()[0:2]
        cnum_to_gua = dict(zip(cnumber_order, eight_gua))
        new_gua = [cnum_to_gua.get(i) for i in new_list(cnumber_order, kok)]
        earth = dict(zip(new_gua, yingyang_order.get(kok_yingyang)))
        reverse_earth = dict(zip(yingyang_order.get(kok_yingyang), new_gua))
        cnumngua = dict(zip(new_list(cnumber_order, kok), yingyang_order.get(kok_yingyang)))
        clockwise_gan = [cnumngua.get(i) for i in  clockwise_cnum]
        return [earth, reverse_earth, clockwise_gan]
    
    #天盤
    def pan_sky(self):
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        earth = self.pan_earth()
        fu_head = self.hourganghzi_zhifu()[2]
        fu_location = earth[1].get(self.gangzhi()[3][0])
        fu_head_location = self.zhifu_n_zhishi().get("值符星宮")[1]
        fu_head_location2 = earth[1].get(fu_head)
        zhishi = self.zhifu_n_zhishi()["值使門宮"][1]
        zhifu_g = self.zhifu_n_zhishi()["值符星宮"][1]
        zhifu = self.zhifu_n_zhishi()["值符星宮"][0]
        if fu_head_location == "中":
            gong_reorder = new_list(rotate, "坤")
            try:
                gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
                gong_reorder = new_list(rotate,  fu_head_location)
                return dict(zip(gong_reorder, gan_reorder)), dict(zip(gan_reorder, gong_reorder)), gan_reorder
            except ValueError:
                try:    
                    return dict(zip(gong_reorder, gan_reorder)), [{'坤':fu_head}]       
                except UnboundLocalError:
                    return self.pan_earth()
        elif fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
            gong_reorder = new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:    
                start = dict(zip(cnumber_order2, gan_reorder)).get(self.qimen_ju_name()[2])
                rgan_reorder = new_list(gan_reorder , start)
                rgong_reorder = new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, rgan_reorder)), dict(zip(rgan_reorder, rgong_reorder)), gan_reorder
            elif fu_head in gan_reorder: 
                if fu_location == None:
                    return  self.pan_earth()
                elif fu_location != None:
                    rgan_reorder = new_list(gan_reorder , earth[0].get(fu_location))
                    rgong_reorder = new_list(gong_reorder , fu_location)
                    return [dict(zip(gong_reorder,gan_reorder)), {self.pan_star()[1].get("禽"):self.pan_earth()[0].get("中") } ]
        elif fu_head_location != "中" and zhifu == "禽" and fu_head_location2 == "中":
            gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], earth[0].get("坤"))
            gong_reorder = new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:    
                rgong_reorder = new_list(gong_reorder , fu_location)
                return dict(zip(rgong_reorder, gan_reorder)), dict(zip(gan_reorder, rgong_reorder))
            elif fu_head in gan_reorder: 
                rgan_reorder = new_list(gan_reorder , earth[0].get(fu_location))
                rgong_reorder = new_list(gong_reorder , fu_location)
                return [dict(zip(gong_reorder,gan_reorder)), {self.pan_star()[1].get("禽"):self.pan_earth()[0].get("中") } ]
            
    
    
    #八門
    def pan_door(self):
        starting_door = self.zhifu_n_zhishi().get("值使門宮")[0]
        starting_gong = self.zhifu_n_zhishi().get("值使門宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        door_reorder = {"陽":new_list(door_r, starting_door), "陰":new_list(list(reversed(door_r)), starting_door)}.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = new_list(rotate, "坤")
        else:
            gong_reorder = new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,door_reorder))
    
    #九星
    def pan_star(self):
        starting_star = self.zhifu_n_zhishi().get("值符星宮")[0].replace("芮", "禽")
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        star_reorder = {"陽":new_list(star_r, starting_star), "陰":new_list(list(reversed(star_r)), starting_star)}.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = new_list(rotate, "坤")
        else:
            gong_reorder = new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,star_reorder)), dict(zip(star_reorder, gong_reorder))
    
    #八神
    def pan_god(self):
        god_order = god_dict.get(self.qimen_ju_name()[0])
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        if starting_gong == "中":
            gong_reorder = new_list(rotate, "坤")
        else:
            gong_reorder = new_list(rotate, starting_gong)
        
        return dict(zip(gong_reorder,god_order))
    
    #排值符
    def zhifu_pai(self):
        yinyang = self.qimen_ju_name()[0]
        kook = self.qimen_ju_name()[2]
        pai = paiyinyang.get(yinyang).get(kook)
        return {"陰":dict(zip(liushun, [i+pai for i in new_list_r(cnumber, kook)[0:6]])), "陽":dict(zip(liushun, [i+pai for i in new_list(cnumber, kook)[0:6]]))}.get(yinyang)
   
    #排值使
    def zhishi_pai(self):
        yinyang = self.qimen_ju_name()[0]
        kook = self.qimen_ju_name()[2]
        yanglist = "".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))
        yinlist =  "".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))
        yangpai = dict(zip(liushun, [i+ yanglist[yanglist.index(i)+1:][0:11] for i in new_list(cnumber, kook)[0:6]]))
        yinpai = dict(zip(liushun, [i+ yinlist[yinlist.index(i)+1:][0:11] for i in new_list_r(cnumber, kook)[0:6]]))
        return {"陰":yinpai, "陽":yangpai}.get(yinyang)
    
    #找值符及值使
    def zhifu_n_zhishi(self):
        hgan = gans_code.get(self.gangzhi()[3][0])
        chour = multi_key_dict_get(liujiashun_dict, self.gangzhi()[3])
        star = dict(zip(list(self.zhifu_pai().keys()), [stars_code.get(i[0]) for i in list(self.zhifu_pai().values())])).get(chour)
        door = dict(zip(list(self.zhishi_pai().keys()), [doors_code.get(i[0]) for i in list(self.zhishi_pai().values())])).get(chour)
        if door == "中":
            door = "死"
        zhifu_gong = dict(zip(list(self.zhifu_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhifu_pai().values())])).get(chour)
        zhishi_gong = dict(zip(list(self.zhishi_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhishi_pai().values())])).get(chour)
        return {"值符星宮":[star,zhifu_gong], "值使門宮":[door,zhishi_gong]}
    
    #九宮長生十二神
    def gong_chengsun(self):
        find_twelve_luck = find_shier_luck(self.gangzhi()[2][0])
        find_twelve_luck_new = dict(zip([zhi2gan.get(i) for i in list(find_twelve_luck.keys())],list(find_twelve_luck.values())))
        sky_pan = self.pan_sky()[0]
        sky_pan_new = dict(zip(sky_pan.keys(),[{list(sky_pan.values())[y]: [find_twelve_luck_new.get(i) for i in sky_pan.values()][y]} for y in range(0,8)]))
        earth_pan = self.pan_earth()[0]
        earth_pan_new = earth_pan_new = dict(zip(earth_pan.keys(),[{list(earth_pan.values())[y]: [find_twelve_luck_new.get(i) for i in earth_pan.values()][y]} for y in range(0,9)]))
        return {"天盤":sky_pan_new, "地盤": earth_pan_new}
    
    def pan(self):
        return {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時","旬首":self.shun(self.gangzhi()[2]),"旬空":self.daykong_shikong(),"局日":self.qimen_ju_day(), "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "值符值使":self.zhifu_n_zhishi(), "天乙":self.tianyi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star()[0], "神":self.pan_god(), "馬星": {"天馬": self.moonhorse(),"丁馬":self.dinhorse(), "驛馬":self.hourhorse()}, "長生運": self.gong_chengsun()}
  
    def pan2(self):
        key = eight_gua
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
        start_jia = jiazi()[0::10]
        find_shun = dict(zip([tuple(new_list(jiazi(), i)[0:10]) for i in start_jia], start_jia))
        dgz = self.gangzhi()[2]
        shun = multi_key_dict_get(find_shun, dgz)
        start_gong_d = {"冬至": "艮離坎坤震巽", "夏至":"坤離巽坤離兌"}
        yy_dun = {"冬至":"陽遁", "夏至":"陰遁"}
        start_gong = start_gong_d.get(multi_key_dict_get({tuple(jieqi_all[0:12]):"冬至", tuple(jieqi_all[12:24]):"夏至"}, self.find_jieqi()))
        yy = yy_dun.get(multi_key_dict_get({tuple(jieqi_all[0:12]):"冬至", tuple(jieqi_all[12:24]):"夏至"}, self.find_jieqi()))
        gong = dict(zip(start_jia, start_gong)).get(shun)
        triple_list = list(map(lambda x: x + x + x, list(range(0,21))))
        b = []
        for i in range(0, len(triple_list)):
            try:
                a = tuple(jiazi()[triple_list[i]: triple_list[i+1]])
                b.append(a)
            except IndexError:
                pass

        g =[]
        f = {"陰遁":anti_clockwise_eightgua ,"陽遁":clockwise_eightgua}
        c_gong = new_list(eight_gua, gong)
        a_gong = new_list(list(reversed(eight_gua)), gong)
        close_ten_day = new_list(jiazi(), shun)[0:10]
        ying = dict(zip(new_list(eight_gua, {**dict(zip(close_ten_day, a_gong)), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), golen_d))
        yang = dict(zip(new_list(eight_gua, {**dict(zip(close_ten_day, c_gong)), **{close_ten_day[-1]:a_gong[0]}}.get(dgz)), golen_d))
        star = {"陰遁":ying ,"陽遁":yang}.get(yy)
        for i in eight_gua2:
            c = dict(zip(new_list(f.get(yy), i), door_r))
            g.append(c)
        e = itertools.cycle(g)
        door = multi_key_dict_get(dict(zip(b, e)), dgz)
        return {
                    "局": yy+dgz+"日",
                    "鶴神": self.crane_god().get(dgz),
                    "星": star,
                    "門": {**door, **{"中":""}},
                    "神": self.getgtw().get(dgz[0])
                    }
            
    def getgtw(self):
        newgtw_order = re.findall("..","地籥天關唐符風雲唐符風雲雷公風伯天曹五符")
        newgtw = [new_list(gtw, i) for i in newgtw_order]
        newgtw_list = [dict(zip(Zhi, i)) for i in newgtw]
        return dict(zip(Gan, newgtw_list))

    #鶴神 
    def crane_god(self):
        newjz = new_list(jiazi(), "庚申")
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
        e = ['''<td align="center">'''+i+ '''<br>'''+god.get(i)+'''</td>''' for i in Zhi]
        c = "<div><table><tr>"+e[0]+e[1]+e[2]+"</tr><tr>"+e[3]+e[4]+e[5]+"</tr><tr>"+e[6]+e[7]+e[8]+"</tr><tr>"+e[9]+e[10]+e[11]+"</tr></table></div>"
        return c
    

    #天乙
    def tianyi(self):
        try:
            star_location = stars_gong_code.get(self.zhifu_n_zhishi().get("值符星宮")[1])
        except IndexError:
            star_location = "禽"
        return star_location

    #丁馬
    def dinhorse(self):
        dinhorsedict =dict(zip(re.findall("..","甲子甲戌甲申甲午甲辰甲寅"), list("卯丑亥酉未巳")))
        liujiashun_dict = {tuple(jiazi()[0:10]):'甲子', tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申", tuple(jiazi()[30:40]):"甲午", tuple(jiazi()[40:50]):"甲辰",  tuple(jiazi()[50:60]):"甲寅"  }
        shun = multi_key_dict_get(liujiashun_dict, self.gangzhi()[2])
        return multi_key_dict_get(dinhorsedict, shun)
    
    #天馬
    def moonhorse(self):
        moonhorsedict = dict(zip([tuple(i) for i in re.findall("..","寅申卯酉辰戌巳亥午子丑未")], list("午申戌子寅辰")))
        return multi_key_dict_get(moonhorsedict, self.gangzhi()[2][1])
    
    #驛馬星
    def hourhorse(self):
        yima = dict(zip([tuple(i) for i in re.findall("...","申子辰寅午戌亥卯未巳酉丑")], list("寅申巳亥")))
        return multi_key_dict_get(yima, self.gangzhi()[3][1])
    
if __name__ == '__main__':
    print(Qimen(2005,1,19,23).pan())
