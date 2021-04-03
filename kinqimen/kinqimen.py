# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
from kinqimen.config import *
import sxtwl, re
import itertools

#%% 主程式
class Qimen:
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.p = {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時","旬首":self.shun(),"旬空":self.daykong_shikong(),"局日":self.qimen_ju_day(), "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "值符值使":self.zhifu_n_zhishi(), "天乙":self.tianyi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star()[0], "神":self.pan_god(), "馬星": {"天馬": self.moonhorse(),"丁馬":self.dinhorse(), "驛馬":self.hourhorse()}, "長生運": self.gong_chengsun()}
        self.g = self.gpan()
        self.overall = {"時家奇門": self.pan, "金函玉鏡": self.g}
                           
    #找節氣
    def find_jieqi(self):
        jieqi_list = twentyfourjieqi(self.year)
        s_date = list(jieqi_list.keys())
        date = datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day), '%Y-%m-%d').date()
        closest = sorted(s_date, key=lambda d: abs( date  - d))[0]
        test = {True:jieqi_list.get(s_date[s_date.index(closest) - 1]), False:jieqi_list.get(closest)}
        return test.get(closest>date)
    
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
        lunar = sxtwl.Lunar()
        cdate = lunar.getDayBySolar(self.year, self.month, self.day)
        yy_mm_dd = Gan[cdate.Lyear2.tg]+Zhi[cdate.Lyear2.dz],  Gan[cdate.Lmonth2.tg]+Zhi[cdate.Lmonth2.dz],  Gan[cdate.Lday2.tg]+Zhi[cdate.Lday2.dz]
        timegz = lunar.getShiGz(cdate.Lday2.tg, self.hour)
        new_hh = Gan[timegz.tg]+Zhi[timegz.dz]
        return yy_mm_dd[0], yy_mm_dd[1],  yy_mm_dd[2], new_hh
    
    #旬
    def shun(self):
        gangzhi = self.gangzhi()[2]
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
        fu_head = self.hourganghzi_zhifu()[2]
        fu_head_location = self.zhifu_n_zhishi().get("值符星宮")[1]
        earth_order = self.pan_earth()
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        try:
            gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
        except ValueError:
            gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], self.pan_earth()[0].get("乾"))
        if fu_head_location == "中":
            gong_reorder = new_list(rotate, "坤")
        else:
            gong_reorder = new_list(rotate,  fu_head_location)
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
        return {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時","旬首":self.shun(),"旬空":self.daykong_shikong(),"局日":self.qimen_ju_day(), "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "值符值使":self.zhifu_n_zhishi(), "天乙":self.tianyi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star()[0], "神":self.pan_god(), "馬星": {"天馬": self.moonhorse(),"丁馬":self.dinhorse(), "驛馬":self.hourhorse()}, "長生運": self.gong_chengsun()}
    
#%% 金函玉鏡 日家奇門       
    def gpan(self):
        find_shun = {tuple(jiazi()[0:10]):"甲子", tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申",  tuple(jiazi()[40:50]):"甲午",  tuple(jiazi()[50:60]):"甲寅"}
        dgz = self.gangzhi()[2]
        shun = multi_key_dict_get(find_shun, dgz)
        start_gong_d = {"冬至": "艮離坎坤震巽", "夏至":"坤離巽坤離兌"}
        yy_dun = {"冬至":"陽遁", "夏至":"陰遁"}
        start_jia = re.findall("..","甲子甲戌甲申甲午甲辰甲寅")
        start_gong = start_gong_d.get(multi_key_dict_get({tuple(jieqi_all[0:12]):"冬至", tuple(jieqi_all[13:24]):"夏至"}, self.find_jieqi()))
        yy = yy_dun.get(multi_key_dict_get({tuple(jieqi_all[0:12]):"冬至", tuple(jieqi_all[13:24]):"夏至"}, self.find_jieqi()))
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
        star = {"陰遁":dict(zip(new_list(eight_gua, dict(zip(new_list(jiazi(), shun)[0:10], new_list(list(reversed(eight_gua)), gong))).get(dgz)), golen_d)) ,"陽遁":dict(zip(new_list(eight_gua, dict(zip(new_list(jiazi(), shun)[0:10], new_list(eight_gua, gong))).get(dgz)), golen_d))}.get(yy)
        for i in eight_gua2:
            c = dict(zip(new_list(f.get(yy), i), door_r))
            g.append(c)
        door = multi_key_dict_get(dict(zip(b, g)), dgz)
        return {
                    "局": yy+dgz+"日",
                    "鶴神": self.crane_god().get(dgz),
                    "星": star,
                    "門": door,
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
            
        
#%% 支節
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
    print(Qimen(2021,4,2,17).pan())

