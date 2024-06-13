# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:49:35 2020
@author: kentang
"""
import re
import time
import itertools
import config
from bidict import bidict
from datetime import datetime, timedelta

def test_qimen(start_datetime, end_datetime):
    # Ensure end_datetime is greater than start_datetime
    if end_datetime <= start_datetime:
        raise ValueError("End datetime must be greater than start datetime")
    # Initialize current_datetime to start_datetime
    current_datetime = start_datetime
    # Loop through each hour from start_datetime to end_datetime
    while current_datetime <= end_datetime:
        year = current_datetime.year
        month = current_datetime.month
        day = current_datetime.day
        hour = current_datetime.hour
        minute = current_datetime.minute  # Keep it 0 for each hour
        try:
            p = Qimen(year, month, day, hour, minute).pan(2)
            print(f"Successfully executed for {current_datetime}")
        except Exception as e:
            print(f"Error at {current_datetime}: {e}")
        # Move to the next hour
        current_datetime += timedelta(hours=1)

class Qimen:
    """奇門函數"""
    def __init__(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def year_yuen(self):
        """搵上中下元"""
        yuen_list = [(i * 60) + 4 for i in range(22,100)]
        three_yuen = itertools.cycle([i+"元甲子" for i in list("上中下")])
        for yuen in yuen_list:
            if self.year < yuen:
                break
            yuen1 = dict(zip(yuen_list, three_yuen)).get(yuen_list[yuen_list.index(yuen)-1])
            return [yuen1, yuen_list[yuen_list.index(yuen)-1]]
        return None

    def qimen_ju_day(self):
        """奇門局日"""
        ju_day_dict = {tuple(list("甲己")):"甲己日",
                       tuple(list("乙庚")):"乙庚日",
                       tuple(list("丙辛")):"丙辛日",
                       tuple(list("丁壬")):"丁壬日",
                       tuple(list("戊癸")):"戊癸日"}
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        try:
            find_d = config.multi_key_dict_get(ju_day_dict, gz[2][0])
        except TypeError:
            find_d = config.multi_key_dict_get(ju_day_dict, gz[2][1])
        return find_d
    #值符
    def hourganghzi_zhifu(self):
        """時干支值符"""
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        jz = config.jiazi()
        a = list(map(lambda x:config.new_list(jz, x)[0:10],jz[0::10]))
        b = list(map(lambda x:jz[0::10][x]+config.tian_gan[4:10][x],list(range(0,6))))
        d = dict(zip(list(map(lambda x: tuple(x),a)),b))
        return config.multi_key_dict_get(d, gz[3])
    #分值符
    def hourganghzi_zhifu_minute(self):
        """刻家奇門值符"""
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        jz = config.jiazi()
        a = list(map(lambda x: tuple(x),list(map(lambda x:config.new_list(jz, x)[0:10],jz[0::10]))))
        b = list(map(lambda x: jz[0::10][x] + config.tian_gan[4:10][x],list(range(0,6))))
        return config.multi_key_dict_get(dict(zip(a,b)), gz[4])
    #地盤
    def pan_earth(self, option):
        """時家奇門地盤設置, option 1:拆補 2:置閏"""
        chaibu = config.qimen_ju_name_chaibu(self.year,
                                             self.month,
                                             self.day,
                                             self.hour,
                                             self.minute)
        zhirun = config.qimen_ju_name_zhirun(self.year,
                                             self.month,
                                             self.day,
                                             self.hour,
                                             self.minute)
        qmju = {1:chaibu,2:zhirun}.get(option)
        return dict(zip(list(map(lambda x: dict(zip(config.cnumber, config.eight_gua)).get(x),
                         config.new_list(config.cnumber, qmju[2]))),
                        {"陽遁":list("戊己庚辛壬癸丁丙乙"),
                         "陰遁":list("戊乙丙丁癸壬辛庚己")}.get(qmju[0:2])))
    #地盤
    def pan_earth_minute(self):
        """刻家奇門地盤設置"""
        ke = config.qimen_ju_name_ke(self.year,
                                     self.month,
                                     self.day,
                                     self.hour,
                                     self.minute)
        return dict(zip(list(map(lambda x: dict(zip(config.cnumber, config.eight_gua)).get(x),
                        config.new_list(config.cnumber, ke[2]))),
                        {"陽遁":list("戊己庚辛壬癸丁丙乙"),
                         "陰遁":list("戊乙丙丁癸壬辛庚己")}.get(ke[0:2])))
    #逆地盤
    def pan_earth_r(self, option):
        """時家奇門地盤(逆)設置, option 1:拆補 2:置閏"""
        pan_earth_v = list(self.pan_earth(option).values())
        pan_earth_k = list(self.pan_earth(option).keys())
        return dict(zip(pan_earth_v, pan_earth_k))

    def pan_earth_min_r(self):
        """刻家奇門地盤(逆)設置"""
        pan_earth_v = list(self.pan_earth_minute().values())
        pan_earth_k = list(self.pan_earth_minute().keys())
        return dict(zip(pan_earth_v, pan_earth_k))
    #天盤
    def pan_sky(self, option):
        qmju = {
            1: config.qimen_ju_name_chaibu,
            2: config.qimen_ju_name_zhirun
        }.get(option)(self.year,
                      self.month,
                      self.day,
                      self.hour,
                      self.minute)
        rotate = {
            "陽": config.clockwise_eightgua,
            "陰": list(reversed(config.clockwise_eightgua))
        }.get(qmju[0])
        zhifu_n_zhishi = config.zhifu_n_zhishi(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            option)
        fu_head = self.hourganghzi_zhifu()[2]
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        fu_location = self.pan_earth_r(option).get(gz[3][0])
        fu_head_location = zhifu_n_zhishi.get("值符星宮")[1]
        fu_head_location2 = self.pan_earth_r(option).get(fu_head)
        gan_head = zhifu_n_zhishi.get("值符天干")[1]
        zhifu = zhifu_n_zhishi["值符星宮"][0]
        earth = self.pan_earth(option)
        gong_reorder = config.new_list(rotate, "坤")
        if fu_head_location == "中":
            try:
                a = list(map(earth.get, rotate))
                gan_reorder = config.new_list(a, fu_head)
                gong_reorder = config.new_list(rotate, fu_head_location)
                return dict(zip(gong_reorder, gan_reorder))
            except ValueError:
                if config.pan_god(self.year,
                                  self.month,
                                  self.day,
                                  self.hour,
                                  self.minute,
                                  option).get("坤") != "符":
                    a = list(map(earth.get, rotate))
                    return dict(zip(gong_reorder, config.new_list(a, self.pan_earth(option).get("坤"))))
                if earth.get("坤") == gan_head:
                    a = list(map(earth.get, rotate))
                    return dict(zip(gong_reorder, config.new_list(a, list(reversed(a))[0])))
                else:
                    try:
                        return dict(zip(gong_reorder, config.new_list(a, gan_head)))
                    except ValueError:
                        return dict(zip(gong_reorder, config.new_list(a, self.pan_earth(option).get("坤"))))

        if fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            newlist = list(map(earth.get, rotate))
            gan_reorder = config.new_list(newlist, fu_head)
            gong_reorder = config.new_list(rotate, fu_head_location)
            if fu_head not in gan_reorder:
                start = dict(zip(config.cnumber, gan_reorder)).get(qmju[2])
                rgan_reorder = config.new_list(gan_reorder, start)
                rgong_reorder = config.new_list(gong_reorder, fu_location)
                aa = dict(zip(rgong_reorder, rgan_reorder))
                bb = dict(zip(rgan_reorder, rgong_reorder))
                return aa, bb
            if fu_head in gan_reorder:
                if fu_location is None:
                    return self.pan_earth(option)
                return {**dict(zip(gong_reorder, gan_reorder)),
                        **{"中": self.pan_earth(option).get("中")}}
        if fu_head_location != "中" and zhifu == "禽" and fu_head_location2 == "中":
            gg = list(map(earth.get, rotate))
            gan_reorder = config.new_list(gg, self.pan_earth(option).get("坤"))
            gong_reorder = config.new_list(rotate, fu_head_location)
            if fu_head not in gan_reorder:
                rgong_reorder = config.new_list(gong_reorder, fu_location)
                return dict(zip(rgong_reorder, gan_reorder))
            return {**dict(zip(gong_reorder, gan_reorder)),
                    **{"中": self.pan_earth(option)[0].get("中")}}
    
    #天盤分
    def pan_sky_minute(self, option):
        """刻家奇門天盤設置, option 1:拆補 2:置閏"""
        rotate = {"陽":config.clockwise_eightgua,"陰":
                  list(reversed(config.clockwise_eightgua))}.get(
                      config.qimen_ju_name_ke(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute)[0])
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        fu_head = self.hourganghzi_zhifu_minute()[2]
        fu_location = self.pan_earth_min_r().get(gz[4][0])
        fu_head_location = config.zhifu_n_zhishi_ke(self.year,
                                                    self.month,
                                                    self.day,
                                                    self.hour,
                                                    self.minute,
                                                    option).get("值符星宮")[1]
        fu_head_location2 = self.pan_earth_min_r().get(fu_head)
        zhifu = config.zhifu_n_zhishi_ke(self.year,
                                         self.month,
                                         self.day,
                                         self.hour,
                                         self.minute,
                                         option)["值符星宮"][0]
        if fu_head_location == "中":
            gong_reorder = config.new_list(rotate, "坤")
            try:
                g = list(map(lambda x: self.pan_earth(option).get(x), list(rotate)))
                gan_reorder = config.new_list(g, fu_head)
                gong_reorder = config.new_list(rotate, fu_head_location)
                return dict(zip(gong_reorder, gan_reorder))
            except ValueError:
                aaa = list(map(lambda x: self.pan_earth(option).get(x), list(reversed(rotate))))
                aaa_bbb = config.new_list(aaa, self.pan_earth(option).get("坤"))
                return dict(zip(list(reversed(gong_reorder)), aaa_bbb))
        if fu_head_location != "中" and zhifu != "禽" and fu_head_location2 != "中":
            rotate_list = list(map(lambda x:self.pan_earth_minute().get(x), list(rotate)))
            gan_reorder = config.new_list(rotate_list, fu_head)
            gong_reorder = config.new_list(rotate, fu_head_location)
            if fu_head not in gan_reorder:
                start = dict(zip(config.cnumber, gan_reorder)).get(
                    config.qimen_ju_name(self.year,
                                         self.month,
                                         self.day,
                                         self.hour,
                                         self.minute)[2])
                rgan_reorder = config.new_list(gan_reorder , start)
                rgong_reorder = config.new_list(gong_reorder , fu_location)
                a_value = dict(zip(rgong_reorder, rgan_reorder))
                b_value = dict(zip(rgan_reorder, rgong_reorder))
                return a_value, b_value
            if fu_head in gan_reorder:
                if fu_location == None:
                    return  self.pan_earth_minute()
                elif fu_location != None:
                    return {**dict(zip(gong_reorder,gan_reorder)),
                            **{"中":self.pan_earth_minute().get("中")}}
        if fu_head_location !="中" and zhifu =="禽" and fu_head_location2 =="中":
            earth_rotate = list(map(lambda x: self.pan_earth_minute().get(x), list(rotate)))
            gan_reorder = config.new_list(earth_rotate, self.pan_earth_minute().get("坤"))
            gong_reorder = config.new_list(rotate,  fu_head_location)
            if fu_head not in gan_reorder:
                rgong_reorder = config.new_list(gong_reorder, fu_location)
                return dict(zip(rgong_reorder, gan_reorder))
            if fu_head in gan_reorder:
                return {**dict(zip(gong_reorder,gan_reorder)),
                        **{"中":self.pan_earth_minute()[0].get("中")}}
        else:
            g = list(map(lambda x: self.pan_earth(option).get(x), list(rotate)))
            gan_reorder = config.new_list(g, fu_head)
            gong_reorder = config.new_list(rotate, fu_head_location)
            return dict(zip(gong_reorder,gan_reorder))
    #九宮長生十二神
    def gong_chengsun(self, option):
        sky = self.pan_sky(option)
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        find_twelve_luck = config.find_shier_luck(gz[2][0])
        di_zhi_mapping = dict(zip(config.di_zhi, list("癸己甲乙戊丙丁己庚辛戊壬")))
        find_twelve_luck_new = {di_zhi_mapping.get(k): v for k, v in find_twelve_luck.items()}
        try:
            sky_pan = sky[0]
            sky_pan_new = {k: {v: find_twelve_luck_new.get(k)} for k, v in sky_pan.items()}
        except KeyError:
            sky_pan = sky
            c = list(map(lambda i:{i:find_twelve_luck_new.get(i)}, list(sky_pan.values())))
            sky_pan_new = dict(zip(list(sky_pan.keys()), c))
        earth_pan = self.pan_earth(option)
        earth_pan_new = {k: {v: find_twelve_luck_new.get(v)} for k, v in earth_pan.items()}
        return {"天盤": sky_pan_new, "地盤": earth_pan_new}

    def gong_chengsun_minute(self, option):
        sky = self.pan_sky_minute(option)
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        find_twelve_luck = config.find_shier_luck(gz[3][0])
        di_zhi_mapping = dict(zip(config.di_zhi, list("癸己甲乙戊丙丁己庚辛戊壬")))
        find_twelve_luck_new = {di_zhi_mapping.get(k): v for k, v in find_twelve_luck.items()}
        try:
            sky_pan = sky[0]
            sky_pan_new = {k: {v: find_twelve_luck_new.get(k)} for k, v in sky_pan.items()}
        except KeyError:
            sky_pan = sky
            b = list(map(lambda i:{i:find_twelve_luck_new.get(i)}, list(sky_pan.values())))
            sky_pan_new = dict(zip(list(sky_pan.keys()), b))
        earth_pan = self.pan_earth(option)
        earth_pan_new = {k: {v: find_twelve_luck_new.get(v)} for k, v in earth_pan.items()}
        return {"天盤": sky_pan_new, "地盤": earth_pan_new}

    def pan(self, option):#1拆補 #2置閏
        """時家奇門起盤綜合, option 1:拆補 2:置閏"""
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        gzd = "{}年{}月{}日{}時".format(gz[0], gz[1], gz[2], gz[3])
        qmju = {1:config.qimen_ju_name_chaibu(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute),
                2:config.qimen_ju_name_zhirun(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute)}.get(option)
        shunhead = config.shun(gz[2])
        shunkong = config.daykong_shikong(self.year,
                                          self.month,
                                          self.day,
                                          self.hour,
                                          self.minute)
        paiju = qmju
        j_q = config.jq(self.year,
                        self.month,
                        self.day,
                        self.hour,
                        self.minute)
        zfzs = config.zhifu_n_zhishi(self.year,
                                     self.month,
                                     self.day,
                                     self.hour,
                                     self.minute,
                                     option)
        pan_star_result = config.pan_star(self.year,
                                          self.month,
                                          self.day,
                                          self.hour,
                                          self.minute,
                                          option)
        star = pan_star_result[0]
        door = config.pan_door(self.year,
                               self.month,
                               self.day,
                               self.hour,
                               self.minute,
                               option)
        god = config.pan_god(self.year,
                             self.month,
                             self.day,
                             self.hour,
                             self.minute,
                             option)
        return {
            "排盤方式":{1:"拆補", 2:"置閏"}.get(option),
            "干支": gzd,
            "旬首": shunhead,
            "旬空": shunkong,
            "局日": self.qimen_ju_day(),
            "排局": paiju,
            "節氣": j_q,
            "值符值使": zfzs,
            "天乙": self.tianyi(option),
            "天盤": self.pan_sky(option),
            "地盤": self.pan_earth(option),
            "門": door,
            "星": star,
            "神": god,
            "馬星": {
                "天馬": self.moonhorse(),
                "丁馬": self.dinhorse(),
                "驛馬": self.hourhorse()
            },
            "長生運": self.gong_chengsun(option)}

    def pan_minute(self, option):
        """刻家奇門起盤綜合, option 1:拆補 2:置閏"""
        gz = config.gangzhi(self.year,
                            self.month,
                            self.day,
                            self.hour,
                            self.minute)
        gzd = "{}年{}月{}日{}時{}分".format(gz[0], gz[1], gz[2], gz[3], gz[4])
        qmju = config.qimen_ju_name_ke(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute)
        shunhead = config.shun(gz[3])
        shunkong = config.hourkong_minutekong(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute)
        paiju = qmju
        j_q = config.jq(self.year,
                        self.month,
                        self.day,
                        self.hour,
                        self.minute)
        zfzs = config.zhifu_n_zhishi_ke(self.year,
                                        self.month,
                                        self.day,
                                        self.hour,
                                        self.minute,
                                        option)
        pan_star_result = config.pan_star_minute(self.year,
                                                 self.month,
                                                 self.day,
                                                 self.hour,
                                                 self.minute,
                                                 option)
        star = pan_star_result[0]
        door = config.pan_door_minute(self.year,
                                      self.month,
                                      self.day,
                                      self.hour,
                                      self.minute,
                                      option)
        god = config.pan_god_minute(self.year,
                                    self.month,
                                    self.day,
                                    self.hour,
                                    self.minute,
                                    option)
        return {
            "排盤方式":{1:"拆補", 2:"置閏"}.get(option),
            "干支": gzd,
            "旬首": shunhead,
            "旬空": shunkong,
            "局日": self.qimen_ju_day(),
            "排局": paiju,
            "節氣": j_q,
            "值符值使": zfzs,
            "天乙": self.tianyi(option),
            "天盤": self.pan_sky_minute(option),
            "地盤": self.pan_earth_minute(),
            "門": door,
            "星": star,
            "神": god,
            "馬星": {
                "天馬": self.moonhorse(),
                "丁馬": self.dinhorse(),
                "驛馬": self.hourhorse()
            },
            "長生運": self.gong_chengsun_minute(option)}

    def pan_html(self, option):
        """時家奇門html, option 1:拆補 2:置閏"""
        god = config.pan_god(self.year,
                             self.month,
                             self.day,
                             self.hour,
                             self.minute,
                             option)
        door = config.pan_door(self.year,
                               self.month,
                               self.day,
                               self.hour,
                               self.minute,
                               option)
        star = config.pan_star(self.year,
                               self.month,
                               self.day,
                               self.hour,
                               self.minute,
                               option)[0]
        sky = self.pan_sky(option)
        earth = self.pan_earth(option)
        a = ''' <div class="container"><table style="width:100%"><tr>''' + \
            "".join(['''<td align="center">''' +
                     sky.get(i) +
                     god.get(i) +
                     door.get(i) +
                     "<br>" +
                     earth.get(i) +
                     star.get(i) +
                     i + '''</td>''' for i in list("巽離坤")]) + "</tr>"
        b = ['''<td align="center">''' +
             sky.get(i) +
             god.get(i) +
             door.get(i) +
             "<br>" +
             earth.get(i) +
             star.get(i) +
             i + '''</td>''' for i in list("震兌")]
        c = '''<tr>''' + b[0] + '''<td><br><br></td>''' + b[1] + '''</tr>'''
        d = "<tr>" + \
            "".join(['''<td align="center">''' +
                     sky.get(i) +
                     god.get(i) +
                     door.get(i) +
                     "<br>" +
                     earth.get(i) +
                     star.get(i) +
                     i + '''</td>''' for i in list("艮坎乾")]) + "</tr></table></div>"
        return a + "".join(b) + c + d

    def ypan(self):
        kok = {"上元甲子":"陰一局",
               "中元甲子":"陰四局",
               "下元甲子":"陰七局"}.get(self.year_yuen()[0])
        return kok

    def gpan(self):
        j_q = config.jq(self.year,
                        self.month,
                        self.day,
                        self.hour,
                        self.minute)
        start_jia = config.jiazi()[0::10]
        dgz = config.gangzhi(self.year,
                             self.month,
                             self.day,
                             self.hour,
                             self.minute)[2]
        dd = [tuple(config.new_list(config.jiazi(), i)[0:10]) for i in start_jia]
        shun = config.multi_key_dict_get(dict(zip(dd, start_jia)), dgz)
        yy = {"冬至":"陽遁", "夏至":"陰遁"}.get(config.multi_key_dict_get(
            {tuple(config.jieqi_name[0:12]):"冬至",
             tuple(config.jieqi_name[12:24]):"夏至"},j_q))
        dh_doors = {"冬至": "艮離坎坤震巽", "夏至":"坤離巽坤離兌"}
        gong = dict(zip(start_jia, dh_doors.get(config.multi_key_dict_get(
            {tuple(config.jieqi_name[0:12]):"冬至",
             tuple(config.jieqi_name[12:24]):"夏至"}, j_q
            )))).get(shun)
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
        r_gua = list(reversed(config.eight_gua))
        new_dict = {**dict(zip(close_ten_day,config.new_list(r_gua, gong))),
                    **{close_ten_day[-1]:a_gong[0]}}
        new_dict_r = {**dict(zip(close_ten_day, config.new_list(config.eight_gua, gong))),
                    **{close_ten_day[-1]:a_gong[0]}}
        ying = dict(zip(config.new_list(config.eight_gua,new_dict.get(dgz)), config.golen_d))
        yang = dict(zip(config.new_list(config.eight_gua,new_dict_r.get(dgz)), config.golen_d))
        for i in list("坎坤震巽乾兌艮離"):
            yy_gua = {"陰遁":list(reversed(config.clockwise_eightgua)),
                      "陽遁":config.clockwise_eightgua}
            c = dict(zip(config.new_list(yy_gua.get(yy), i), config.door_r))
            g.append(c)
        ddd = config.multi_key_dict_get(dict(zip(b, itertools.cycle(g))), dgz)
        return {"局": yy+dgz+"日",
                "鶴神": self.crane_god().get(dgz),
                "星": {"陰遁":ying ,"陽遁":yang}.get(yy),
                "門": {**ddd, 
                      **{"中":""}},
                "神": config.getgtw().get(dgz[0])}
    #鶴神
    def crane_god(self):
        d = list("巽離坤兌乾坎天艮震")
        dd = [6,5,6,5,6,5,16,6,5]
        newc_list = list(map(lambda i:[d[i][:5]]*dd[i],list(range(0,8))))
        return dict(zip(config.new_list(config.jiazi(), "庚申"), newc_list))

    def gpan_html(self):
        gpan_data = self.gpan()
        door = gpan_data.get("門")
        star = gpan_data.get("星")
        html_output = '''<div class="container"><table style="width:100%"><tr>'''
        html_output += ''.join([
            f'''<td align="center">{star[i]}<br>{door[i]}{i}</td>''' for i in "巽離坤"
        ])
        html_output += "</tr><tr>"
        html_output += ''.join([
            f'''<td align="center">{star[i]}<br>{door[i]}{i}</td>''' for i in "震中兌"
        ])
        html_output += "</tr><tr>"
        html_output += ''.join([
            f'''<td align="center">{star[i]}<br>{door[i]}{i}</td>''' for i in "艮坎乾"
        ])
        html_output += "</tr></table></div>"
        return html_output
    #天乙
    def tianyi(self, option):
        zhifu_n_zhishi= config.zhifu_n_zhishi(self.year,
                                              self.month,
                                              self.day,
                                              self.hour,
                                              self.minute,
                                              option)
        zhifu_dict = dict(zip(config.eight_gua, list("蓬芮沖輔禽心柱任英")))
        try:
            star_location = zhifu_dict.get(zhifu_n_zhishi.get("值符星宮")[1])
        except IndexError:
            star_location = "禽"
        return star_location
    #丁馬
    def dinhorse(self):
        gz = config.gangzhi(self.year,
                                 self.month,
                                 self.day,
                                 self.hour,
                                 self.minute)
        tg = re.findall("..","甲子甲戌甲申甲午甲辰甲寅")
        new_dict = dict(zip(tg, list("卯丑亥酉未巳")))
        new = config.multi_key_dict_get(config.liujiashun_dict(), gz[2])
        return config.multi_key_dict_get(new_dict, new)
    #天馬
    def moonhorse(self):
        Gangzhi = config.gangzhi(self.year,
                                 self.month,
                                 self.day,
                                 self.hour,
                                 self.minute)
        tg = re.findall("..","寅申卯酉辰戌巳亥午子丑未")
        new = list(map(lambda i:tuple(i), tg))
        new_dict = dict(zip(new, list("午申戌子寅辰")))
        return config.multi_key_dict_get(new_dict, Gangzhi[2][1])
    #驛馬星
    def hourhorse(self):
        Gangzhi = config.gangzhi(self.year,
                                 self.month,
                                 self.day,
                                 self.hour,
                                 self.minute)
        tg = re.findall("...","申子辰寅午戌亥卯未巳酉丑")
        new = list(map(lambda i:tuple(i), tg))
        new_dict = dict(zip(new, list("寅申巳亥")))
        return config.multi_key_dict_get(new_dict, Gangzhi[3][1])
    
    def green_dragon(self, option):
        sky = self.pan_sky(option)
        earth = self.pan_earth(option)
        zhishi = config.zhifu_n_zhishi(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            option).get("值符天干")[1]
        try:
            zhishi_gong = bidict(earth).inverse[zhishi]
            sky_gong = bidict(sky).inverse["戊"]
            earth_gong = bidict(earth).inverse["丙"]
            if earth_gong == sky_gong:
                return {"青龍返首": sky_gong}
            if zhishi_gong == earth_gong:
                return {"青龍返首": earth_gong}
            else:
                return {"青龍返首": "沒有"}
        except KeyError:
            return {"青龍返首": "沒有"}
            
    def fly_bird(self, option):
        sky = self.pan_sky(option)
        earth = self.pan_earth(option)
        zhishi = config.zhifu_n_zhishi(
            self.year,
            self.month,
            self.day,
            self.hour,
            self.minute,
            option).get("值符天干")[1]
        try:
            zhishi_gong = bidict(earth).inverse[zhishi]
            earth_gong = bidict(earth).inverse["戊"]
            sky_gong = bidict(sky).inverse["丙"]        
            if earth_gong == sky_gong:
                return {"飛鳥跌穴": sky_gong}
            if sky_gong == zhishi_gong:
                return {"飛鳥跌穴": sky_gong}
            else:
                return {"飛鳥跌穴": "沒有"}
        except KeyError:
            return {"飛鳥跌穴": "沒有"}
        
    def jade_girl(self, option):
        earth = self.pan_earth(option)
        try:
            earth_gong = bidict(earth).inverse["丁"]
            zhishi = config.zhifu_n_zhishi(
                self.year,
                self.month,
                self.day,
                self.hour,
                self.minute,
                option).get('值使門宮')[1]
            if zhishi == earth_gong:
                return {"玉女守門": zhishi}
            else:
                return {"玉女守門": "沒有"}
        except KeyError:
            return {"玉女守門": "沒有"}
        
    def overall(self, option):
        """整體奇門起盤綜合, option 1:拆補 2:置閏"""
        return {"金函玉鏡(日家奇門)": self.gpan(),
                "時家奇門": self.pan(option),
                "刻家奇門":self.pan_minute(option)}
    


if __name__ == '__main__':
    tic = time.perf_counter()
    #start_datetime = datetime(2024, 5, 1, 0, 0)
    #end_datetime = datetime(2024, 5, 30, 23, 0)  # Adjust as needed
    #print(test_qimen(start_datetime, end_datetime))
    try:
        for y in range(0,23):
            for i in range(1,32):
                qtext2 = Qimen(2024,7,i,y,0).green_dragon(2)
                print(qtext2)
    except KeyError:
        print([2024,7,i,y,0])
    #qtext1 = Qimen(2024,6,6,16,37).pan_earth(2)
   
    #q = list("巽離坤震兌艮坎乾")
    #a = [qtext.get("天盤").get(i) for i in q]
    #print(qtext1)
    #print(qtext2)
    #print(Qimen(2024,2,2,4,15).pan_earth(2))
    #print(Qimen(2024,2,2,4,15).pan_earth(2))
    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")
