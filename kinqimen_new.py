# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
from config import *
import sxtwl
import itertools


class Qimen:
    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
                                 
    def find_jieqi(self):
        jieqi_list = twentyfourjieqi(self.year)
        s_date = list(jieqi_list.keys())
        date = datetime.strptime(str(self.year)+"-"+str(self.month)+"-"+str(self.day), '%Y-%m-%d').date()
        closest = sorted(s_date, key=lambda d: abs( date  - d))[0]
        test = {True:jieqi_list.get(s_date[s_date.index(closest) - 1]), False:jieqi_list.get(closest)}
        return test.get(closest>date)
    
    def qimen_ju_name(self):
        find_yingyang = multi_key_dict_get(yingyang_dun, self.find_jieqi())
        findyuen = multi_key_dict_get(findyuen_dict, self.gangzhi()[2])
        jieqicode = multi_key_dict_get(jieqidun_code, self.find_jieqi())
        find_kok = {"上元":jieqicode[0], "中元":jieqicode[1], "下元":jieqicode[2]}
        return find_yingyang+find_kok.get(findyuen)+"局"+findyuen
    
    def find_yuen(self):
        find_yingyang = multi_key_dict_get(yingyang_dun, self.find_jieqi())
        findyuen = multi_key_dict_get(findyuen_dict, self.gangzhi()[2])
        return findyuen
    
    def gangzhi(self):
        lunar = sxtwl.Lunar()
        cdate = lunar.getDayBySolar(self.year, self.month, self.day)
        yy_mm_dd = Gan[cdate.Lyear2.tg]+Zhi[cdate.Lyear2.dz],  Gan[cdate.Lmonth2.tg]+Zhi[cdate.Lmonth2.dz],  Gan[cdate.Lday2.tg]+Zhi[cdate.Lday2.dz]
        timegz = lunar.getShiGz(cdate.Lday2.tg, self.hour)
        new_hh = Gan[timegz.tg]+Zhi[timegz.dz]
        return yy_mm_dd[0], yy_mm_dd[1],  yy_mm_dd[2], new_hh
    
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
    
    def qimen_ju_day(self):
        day_gangzhi = self.gangzhi()[2]
        ju_day_dict = {tuple(list("甲己")):"甲己日",  tuple(list("乙庚")):"乙庚日",  tuple(list("丙辛")):"丙辛日", tuple(list("丁壬")):"丁壬日", tuple(list("戊癸")):"戊癸日"}
        try:
            find_d = multi_key_dict_get(ju_day_dict, day_gangzhi[0])
        except TypeError:
            find_d = multi_key_dict_get(ju_day_dict, day_gangzhi[1])
        return find_d
    
    def daykong_shikong(self):
        return {"日空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, self.gangzhi()[2])).get("孤"), "時空":multi_key_dict_get(guxu, multi_key_dict_get(liujiashun_dict, self.gangzhi()[3])).get("孤")}

    def hourganghzi_zhifu(self):
        return multi_key_dict_get(liujiashun_dict2, self.gangzhi()[3])

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
    
    def pan_sky(self):
        fu_head = self.hourganghzi_zhifu()[2]
        fu_head_location = self.zhifu_n_zhishi().get("值符星宮")[1]
        earth_order = self.pan_earth()
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        gan_reorder = new_list([self.pan_earth()[0].get(i) for i in list(rotate)], fu_head)
        gong_reorder = new_list(rotate, fu_head_location)
        return dict(zip(gong_reorder,gan_reorder))
    
    def pan_door(self):
        starting_door = self.zhifu_n_zhishi().get("值使門宮")[0]
        starting_gong = self.zhifu_n_zhishi().get("值使門宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        door_reorder = {"陽":new_list(door_r, starting_door), "陰":new_list(list(reversed(door_r)), starting_door)}.get(self.qimen_ju_name()[0])
        gong_reorder = new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,door_reorder))
    
    def pan_star(self):
        starting_star = self.zhifu_n_zhishi().get("值符星宮")[0]
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        star_reorder = {"陽":new_list(star_r, starting_star), "陰":new_list(list(reversed(star_r)), starting_star)}.get(self.qimen_ju_name()[0])
        gong_reorder = new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,star_reorder))
    
    def pan_god(self):
        god_order = god_dict.get(self.qimen_ju_name()[0])
        starting_gong = self.zhifu_n_zhishi().get("值符星宮")[1]
        rotate = {"陽":clockwise_eightgua, "陰":anti_clockwise_eightgua }.get(self.qimen_ju_name()[0])
        gong_reorder = new_list(rotate, starting_gong)
        return dict(zip(gong_reorder,god_order))
    
    def pan(self):
        return {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時", "局日":self.qimen_ju_day() , "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "天盤":self.pan_sky(), "地盤":self.pan_earth()[0], "門":self.pan_door(),"星":self.pan_star(), "神":self.pan_god() ,"值符值使":self.zhifu_n_zhishi()}

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
        return {"陰":dict(zip(liushun, [i+pai for i in new_list_r(cnumber, kook)[0:6]])), "陽":dict(zip(liushun, [i+pai for i in new_list(cnumber, kook)[0:6]]))}.get(yinyang)
   
    def zhishi_pai(self):
        yinyang = self.qimen_ju_name()[0]
        kook = self.qimen_ju_name()[2]
        yanglist = "".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))+"".join(new_list(cnumber, kook))
        yinlist =  "".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))+"".join(new_list_r(cnumber, kook))
        yangpai = dict(zip(liushun, [i+ yanglist[yanglist.index(i)+1:][0:11] for i in new_list(cnumber, kook)[0:6]]))
        yinpai = dict(zip(liushun, [i+ yinlist[yinlist.index(i)-1:][0:11] for i in new_list_r(cnumber, kook)[0:6]]))
        return {"陰":yinpai, "陽":yangpai}.get(yinyang)
    
    def zhifu_n_zhishi(self):
        hgan = gans_code.get(self.gangzhi()[3][0])
        chour = multi_key_dict_get(liujiashun_dict, self.gangzhi()[3])
        star = dict(zip(list(self.zhifu_pai().keys()), [stars_code.get(i[0]) for i in list(self.zhifu_pai().values())])).get(chour)
        door = dict(zip(list(self.zhishi_pai().keys()), [doors_code.get(i[0]) for i in list(self.zhishi_pai().values())])).get(chour)
        zhifu_gong = dict(zip(list(self.zhifu_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhifu_pai().values())])).get(chour)
        zhishi_gong = dict(zip(list(self.zhishi_pai().keys()), [gongs_code.get(i[hgan]) for i in list(self.zhishi_pai().values())])).get(chour)
        return {"值符星宮":[star,zhifu_gong], "值使門宮":[door,zhishi_gong]}

print( Qimen(2020,5,31, 2).pan())

