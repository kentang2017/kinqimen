# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:32:50 2020

@author: hooki
"""


from ephem import *
import math, datetime, re

def jiazi():
    tiangan = '甲乙丙丁戊己庚辛壬癸'
    dizhi = '子丑寅卯辰巳午未申酉戌亥'
    jiazi = [tiangan[x % len(tiangan)] + dizhi[x % len(dizhi)] for x in range(60)]
    return jiazi

def new_list_r(olist, o):
    zhihead_code = olist.index(o)
    res1 = []
    for i in range(len(olist)):
        res1.append( olist[zhihead_code % len(olist)])
        zhihead_code = zhihead_code - 1
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


jieqi=re.findall('..', '春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至小寒大寒立春雨水驚蟄')

def ecliptic_lon(jd_utc):
    s=Sun(jd_utc)
    equ=Equatorial(s.ra,s.dec,epoch=jd_utc)
    e=Ecliptic(equ)
    return e.lon

def sta(jd):
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)
    return n

def iteration(jd,sta):
    s1=sta(jd)
    s0=s1
    dt=1.0
    while True:
        jd+=dt
        s=sta(jd)
        if s0!=s:
            s0=s
            dt=-dt/2
        if abs(dt)<0.0000001 and s!=s1:
            break
    return jd

def fjqs(year, month, day, hour):
    jd=Date( str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2)+" "+str(hour).zfill(2)+":00:00.00")
    ct = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S")
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1
    c = []
    for i in range(1):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        b = [jieqi[n], datetime.datetime.strptime(str(d[0])+"-"+str(d[1])+"-"+str(d[2])+"-"+str(d[3])+":00:00", "%Y-%m-%d-%H:%M:%S")]
        c.append(b)
    return c[0]


def jq(year, month, day, hour):
    jd=Date( str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2)+" "+str(hour).zfill(2)+":00:00.00")
    ct = datetime.datetime.strptime(str(year)+"-"+str(month)+"-"+str(day)+"-"+str(hour)+":00:00", "%Y-%m-%d-%H:%M:%S")
    p = ct - datetime.timedelta(days=7)
    pp = ct - datetime.timedelta(days=21)
    bf = fjqs(p.year, p.month, p.day, p.hour)
    bbf = fjqs(pp.year, pp.month, pp.day, pp.hour)
    t1 = bf[1]
    t2 = bbf[1]
    if ct < t1:
        return bbf[0]
    else:
        return bf[0]

Gan = list("甲乙丙丁戊己庚辛壬癸")
Zhi = list("子丑寅卯辰巳午未申酉戌亥")

def find_jq_date(year, month, day, hour, jq):
    jd=Date( str(year)+"/"+str(month).zfill(2)+"/"+str(day).zfill(2)+" "+str(hour).zfill(2)+":00:00.00")
    e=ecliptic_lon(jd)
    n=int(e*180.0/math.pi/15)+1
    dzlist = []
    for i in range(24):
        if n>=24:
            n-=24
        jd=iteration(jd,sta)
        d=Date(jd+1/3).tuple()
        d1=Date(jd+1/3)
        b = {jieqi[n]: datetime.datetime(d[0], d[1], d[2],d[3], d[4], int(d[5]))}
        n+=1
        dzlist.append(b)
    return list(dzlist[[list(i.keys())[0] for i in dzlist].index(jq)].values())[0]

#print(find_jq_date(2022, 3, 18, 11, "冬至"))
