# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
from config import *
import sxtwl


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

    def zhifu(self): 
        extra_value = jiaji_extra_plus_minus.get(multi_key_dict_get(liujiashun_dict , self.gangzhi()[3]))
        kok_num = cnum_dict.get(self.qimen_ju_name()[2]) 
        gan_num  = gan_dict.get(self.gangzhi()[3][0]) 
        hourgangzhihead = self.gangzhi()[3][0]
        if hourgangzhihead != "甲":
            zhifu = self.find_pan_earth()[1].get(self.gangzhi()[3][0])
        else:
            zhifu = self.find_pan_earth()[1].get(self.hourganghzi_zhifu()[2])
            if zhifu == "中":
                zhifu = self.hourganghzi_zhifu()[2]
        if self.qimen_ju_name()[0] == "陽":
            star = star_dict.get(gan_dict.get(self.gangzhi()[3][0]))    
        elif self.qimen_ju_name()[0] == "陰":
            if kok_num <= gan_num:
                star = star_dict.get(extra_value+ gan_dict.get(self.hourganghzi_zhifu()[2]) - kok_num + extra_value)
            elif self.gangzhi()[3][0] == "甲":
                star = star_dict.get(r_eight_gua_code.get(zhifu))
            elif self.gangzhi()[3][0] != "甲" and kok_num != 5:
                star = star_dict.get(gan_dict.get(self.gangzhi()[3][0])+extra_value)
            elif self.gangzhi()[3][0] != "甲" and kok_num == 5:
                star = star_dict.get(gan_dict.get(self.hourganghzi_zhifu()[2]) - kok_num + extra_value)
        return {"宮":zhifu, "星": star, "補數": extra_value}
    
    def zhishi(self):
        extra_value = jiaji_extra_plus_minus.get(multi_key_dict_get(liujiashun_dict , self.gangzhi()[3]))
        kok_num = cnum_dict.get(self.qimen_ju_name()[2]) 
        gan_num  = gan_dict.get(self.gangzhi()[3][0]) 
        if self.qimen_ju_name()[0] == "陽":
            zhishi_num = gan_num + extra_value + kok_num
            if zhishi_num == 10:
                zhishi_num = 1
            elif zhishi_num > 10:
                zhishi_num = zhishi_num - 9
                if zhishi_num == 10:
                    zhishi_num = 1
            elif gan_num == kok_num:
                zhishi_num = gan_dict.get(self.hourganghzi_zhifu()[2])  - kok_num
            elif self.gangzhi()[3][0] == "甲":
                zhishi_num = gan_dict.get(self.hourganghzi_zhifu()[2])
        elif self.qimen_ju_name()[0] == "陰":
            if gan_num > kok_num and gan_num < 10 and gan_num !=5:
                zhishi_num =  gan_dict.get(self.gangzhi()[3][0]) - r_gong_dict.get(self.zhifu().get("宮"))
                #zhishi_num = gan_dict.get(self.hourganghzi_zhifu()[2]) - gan_dict.get(self.gangzhi()[3][0])
                if zhishi_num == 0:
                    zhishi_num = gan_dict.get(self.gangzhi()[3][0]) + gan_dict.get(self.hourganghzi_zhifu()[2])
                elif zhishi_num < 0:
                    zhishi_num = r_gong_dict.get(self.zhifu().get("宮"))
            elif gan_num == 5:
                zhishi_num = 5
                zhishi_door =  door_code.get(self.qimen_ju_name()[0:2]).get(r_gong_dict.get(self.zhifu().get("宮")) - extra_value)
            elif gan_num == 10:
                zhishi_num = 5
            elif kok_num == 5:
                zhishi_num =  kok_num + gan_num 
         
        
        if self.gangzhi()[3][0] == "甲":
            zhishi_door = door_code.get(self.qimen_ju_name()[0:2]).get(kok_num + extra_value)
        elif self.gangzhi()[3][0] != "甲":
            if gan_num > kok_num and gan_num != 5:
                zhishi_door = door_code.get(self.qimen_ju_name()[0:2]).get(gan_num - kok_num)
            elif gan_num < kok_num and gan_num != 5:
                zhishi_door = door_code.get(self.qimen_ju_name()[0:2]).get(kok_num + extra_value)
            elif gan_num == kok_num and gan_num != 5:
                zhishi_door =  door_code.get(self.qimen_ju_name()[0:2]).get(gan_dict.get(self.hourganghzi_zhifu()[2]) - zhishi_num)
        return { "門":zhishi_door, "宮":gong_dict.get(zhishi_num)  }
        
    def find_pan_earth(self):
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
        hourgangzhihead = self.gangzhi()[3][0]
        fu_head_location = self.find_pan_earth()[1].get(self.hourganghzi_zhifu()[2])
        zhifu = self.zhifu()
        fu_head_order_next = new_list( yingyang_order.get(self.qimen_ju_name()[0:2]), fu_head)[1]
        if zhifu.get("宮") != "中":
            next_location = new_list(clockwise_eightgua, zhifu.get("宮"))
        else:
            next_location = new_list(clockwise_eightgua, new_list(clockwise_eightgua, "離")[1])
        earth_pan = new_list(self.find_pan_earth()[2], fu_head)
        result = dict(zip(next_location, earth_pan))
        r_result = dict(zip(earth_pan, next_location))
        return [result, r_result]
    
    def pan_door(self):
        if self.qimen_ju_name()[0] == "陽":
            starting_door = self.zhishi().get("門")
            starting_gong_order = new_list(eight_door2, starting_door)
        elif self.qimen_ju_name()[0] == "陰":
            starting_door = self.zhishi().get("門")
            starting_gong_order = new_list(list(reversed(eight_door2)), starting_door)
        return starting_gong_order
    
    def pan(self):
        return {"干支":self.gangzhi()[0]+"年"+self.gangzhi()[1]+"月"+self.gangzhi()[2]+"日"+self.gangzhi()[3]+"時", "局日":self.qimen_ju_day() , "排局":self.qimen_ju_name(), "節氣":self.find_jieqi(), "天盤":self.pan_sky(), "地盤":self.find_pan_earth()[0], "值符":self.zhifu(), "值使":self.zhishi()}

print( Qimen(2019, 11, 25, 0).pan())
        
#print( Qimen(2020, 5, 25, 21).zhifu())