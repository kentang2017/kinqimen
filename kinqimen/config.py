# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 11:32:50 2020

@author: hooki
"""

from datetime import datetime
import re

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

START_YEAR = 1901
month_DAY_BIT = 12
month_NUM_BIT = 13
stc= '小寒大寒立春雨水驚蛰春分清明穀雨立夏小滿芒種夏至小暑大暑立秋處暑白露秋分寒露霜降立冬小雪大雪冬至'
solarTermsNameList=[stc[x * 2:(x + 1) * 2] for x in range(0, len(stc) // 2)]

jieqidun_code = {
("冬至", "驚蟄"): "一七四", 
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

# 1901-2100年二十节气最小公差数序列 向量压缩法
encryptionVectorList=[4, 19, 3, 18, 4, 19, 4, 19, 4, 20, 4, 20, 6, 22, 6, 22, 6, 22, 7, 22, 6, 21, 6, 21]
# 1901-2100年二十节气数据 每个元素的存储格式如下：
# 1-24
# 节气所在天（减去节气最小公约数）
# 1901-2100年香港天文台公布二十四节气按年存储16进制，1个16进制为4个2进制
solarTermsData=[
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, # 1901 ~ 1905
    0xaaaaaaaaaa6a, 0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0xaaabbabbafaa, 0x5aa665a65aab, 0x6aaaa6aa9a56, 0xaaaaaaaa9a5a, 0xaaabaabaaeaa,
    0x569665a65aaa, 0x5aa6a6a69a56, 0x6aaaaaaa9a5a, 0xaaabaabaaeaa, 0x569665a65aaa,
    0x5aa6a6a65a56, 0x6aaaaaaa9a5a, 0xaaabaabaaa6a, 0x569665a65aaa, 0x5aa6a6a65a56,
    0x6aaaa6aa9a5a, 0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a,
    0xaaaaaabaaa6a, 0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a,
    0x555665665aaa, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665665aaa,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0xaaaaaaaaaa6a, 0x555665655aaa, 0x569665a65a56,
    0x6aa6a6aa9a56, 0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x6aa6a6a65a56,
    0xaaaaaaaa9a5a, 0x5556556559aa, 0x569665a65a55, 0x5aa6a6a65a56, 0x6aaaa6aa9a5a,
    0x5556556555aa, 0x569665a65a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a,
    0x555665665a55, 0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555565556a, 0x555665665a55,
    0x5aa665a65a56, 0x6aaaa6aa9a5a, 0x55555555556a, 0x555665665a55, 0x5aa665a65a56,
    0x6aaaa6aa9a5a, 0x55555555556a, 0x555665655a55, 0x5aa665a65a56, 0x6aa6a6aa9a5a,
    0x55555555456a, 0x555655655a55, 0x5a9665a65a56, 0x6aa6a6a69a5a, 0x55555555456a,
    0x555655655a55, 0x569665a65a56, 0x6aa6a6a65a56, 0x55555155455a, 0x555655655955,
    0x569665a65a55, 0x5aa6a5a65a56, 0x15555155455a, 0x555555655555, 0x569665665a55,
    0x5aa665a65a56, 0x15555155455a, 0x555555655515, 0x555665665a55, 0x5aa665a65a56,
    0x15555155455a, 0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a,
    0x555555555515, 0x555665665a55, 0x5aa665a65a56, 0x15555155455a, 0x555555555515,
    0x555655655a55, 0x5aa665a65a56, 0x15515155455a, 0x555555554515, 0x555655655a55,
    0x5a9665a65a56, 0x15515151455a, 0x555551554515, 0x555655655a55, 0x569665a65a56,
    0x155151510556, 0x555551554505, 0x555655655955, 0x569665665a55, 0x155110510556,
    0x155551554505, 0x555555655555, 0x569665665a55, 0x55110510556, 0x155551554505,
    0x555555555515, 0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515,
    0x555665665a55, 0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55,
    0x55110510556, 0x155551554505, 0x555555555515, 0x555655655a55, 0x55110510556,
    0x155151514505, 0x555555554515, 0x555655655a55, 0x54110510556, 0x155151510505,
    0x555551554515, 0x555655655a55, 0x14110110556, 0x155110510501, 0x555551554505,
    0x555555655555, 0x14110110555, 0x155110510501, 0x555551554505, 0x555555555555,
    0x14110110555, 0x55110510501, 0x155551554505, 0x555555555555, 0x110110555,
    0x55110510501, 0x155551554505, 0x555555555515, 0x110110555, 0x55110510501,
    0x155551554505, 0x555555555515, 0x100100555, 0x55110510501, 0x155151514505,
    0x555555555515, 0x100100555, 0x54110510501, 0x155151514505, 0x555551554515,
    0x100100555, 0x54110510501, 0x155150510505, 0x555551554515, 0x100100555,
    0x14110110501, 0x155110510505, 0x555551554505, 0x100055, 0x14110110500,
    0x155110510501, 0x555551554505, 0x55, 0x14110110500, 0x55110510501,
    0x155551554505, 0x55, 0x110110500, 0x55110510501, 0x155551554505,
    0x15, 0x100110500, 0x55110510501, 0x155551554505,0x555555555515]

Gan = list("甲乙丙丁戊己庚辛壬癸")
rGan = list("癸壬辛庚己戊丁丙乙甲")
rhourgang_dict = dict(zip(rGan, list(range(1,11))))
hourgang_dict = dict(zip(Gan, list(range(1,11))))
Zhi = list("子丑寅卯辰巳午未申酉戌亥")
hidden_jia = {'甲子':'戊', '甲戌':'己','甲申':'庚','甲午':'辛','甲辰':'壬','甲寅':'癸' }
liushun = re.findall('..',"甲子甲戌甲申甲午甲辰甲寅")

cnumber = list("一二三四五六七八九")
nine_star = list("蓬芮沖輔禽心柱任英")
eight_door = list("休死傷杜中開驚生景")
eight_door2 = list("休死傷杜開驚生景")
eight_gua = list("坎坤震巽中乾兌艮離")
god_dict = {"陽":list("符蛇陰合勾雀地天"),"陰":list("符蛇陰合虎玄地天")}

gans_code = dict(zip(Gan,range(0,11)))
gans_code2 = dict(zip(Gan,range(1,11)))
cnumber_code = dict(zip(cnumber,range(1,11)))
stars_code = dict(zip(cnumber, nine_star))
doors_code = dict(zip(cnumber, eight_door))
gongs_code = dict(zip(cnumber, eight_gua))
stars_gong_code = dict(zip(eight_gua, nine_star))

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

clockwise_eightgua = list("坎艮震巽離坤兌乾")
anti_clockwise_eightgua = list(reversed(clockwise_eightgua))
door_r = list("休生傷杜景死驚開")
star_r = list("蓬任沖輔英禽柱心")

liujiashun_dict = {tuple(jiazi()[0:10]):"甲子", tuple(jiazi()[10:20]):"甲戌", tuple(jiazi()[20:30]):"甲申", tuple(jiazi()[30:40]):"甲午", tuple(jiazi()[40:50]):"甲辰", tuple(jiazi()[50:60]):"甲寅"}
liujiashun_dict2 = {tuple(jiazi()[0:10]):"甲子戊", tuple(jiazi()[10:20]):"甲戌己", tuple(jiazi()[20:30]):"甲申庚", tuple(jiazi()[30:40]):"甲午辛", tuple(jiazi()[40:50]):"甲辰壬", tuple(jiazi()[50:60]):"甲寅癸"}
door_code = {"陽遁":dict(zip(range(1,9), eight_door2)),"陰遁":dict(zip(range(1,9), list(reversed(eight_door2))))}

findyuen_dict = {tuple(jiazi()[0:5]): "上元", 
                tuple(jiazi()[15:20]):"上元", 
                tuple(jiazi()[30:35]):"上元", 
                tuple(jiazi()[45:50]):"上元", 
                tuple(jiazi()[5:10]): "中元",  
                tuple(jiazi()[20:25]):"中元", 
                tuple(jiazi()[35:40]):"中元", 
                tuple(jiazi()[50:55]):"中元", 
                tuple(jiazi()[10:15]):"下元", 
                tuple(jiazi()[25:30]):"下元" , 
                tuple(jiazi()[40:45]):"下元" , 
                tuple(jiazi()[55:60]):"下元" }

guxu = {'甲子':{'孤':'戌亥', '虛':'辰巳'}, '甲戌':{'孤':'申酉', '虛':'寅卯'},'甲申':{'孤':'午未', '虛':'子丑'},'甲午':{'孤':'辰巳', '虛':'戌亥'},'甲辰':{'孤':'寅卯', '虛':'申酉'},'甲寅':{'孤':'子丑', '虛':'午未'} }
shunlist = {0:"戊", 10:"己", 8:"庚", 6:"辛", 4:"壬", 2:"癸"}
jieqi_all = new_list([stc[i:i+2] for i in range(0, len(stc), 2)], "冬至")
yingyang_dun = {tuple(jieqi_all[0:12]):"陽遁",tuple(jieqi_all[12:24]):"陰遁" }
yingyang_order = {"陽遁":list("戊己庚辛壬癸丁丙乙"),"陰遁":list("戊乙丙丁癸壬辛庚己")}
cnumber_order = list("一二三四五六七八九")
clockwise_cnum = list("一八三四九二七六")
cnum_dict = dict(zip(cnumber_order, range(1,9)))

# 采集压缩用
def zipSolarTermsList(inputList,charCountLen=2):
    tempList=abListMerge(inputList, type=-1)
    data=0
    num=0
    for i in tempList:
        data+=i << charCountLen*num
        num+=1
    return hex(data),len(tempList)

        
def twentyfourjieqi(year):
    day = getTheYearAllSolarTermsList(year)
    month = [ele for ele in [i for i in range(1,13)] for b in range(2)]
    new_date_list = []
    for i in range(0,23):
        new_date = str(year)+"/"+str(month[i])+"/"+str(day[i])   
        date_format = datetime.strptime(new_date , "%Y/%m/%d").date()
        new_date_list.append(date_format)
    return dict(zip(new_date_list,solarTermsNameList))
# 两个List合并对应元素相加或者相减，a[i]+b[i]:tpye=1 a[i]-b[i]:tpye=-1
def abListMerge(a, b=encryptionVectorList, type=1):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i]*type)
    return c

def unZipSolarTermsList(data,rangeEndNum=24,charCountLen=2):
    list2 = []
    for i in range(1,rangeEndNum+1):
        right=charCountLen*(rangeEndNum-i)
        if type(data).__name__=='str':
            data= int(data, 16)
        x=data >> right
        c=2**charCountLen
        list2=[(x % c)]+list2
    return abListMerge(list2)
    
def getTheYearAllSolarTermsList(year):
    return unZipSolarTermsList(solarTermsData[year-START_YEAR])

qimen_shigan = {'乙乙': ['日奇伏吟', '凶', '不宜謁貴求名，只可安分守身。'],
 '乙丙': ['奇儀順遂', '吉', '吉星遷官進職，凶星夫妻離別。'],
 '乙丁': ['奇儀相佐', '吉', '文書事吉，百事皆可為。'],
 '乙戊': ['陰害陽門', '凶', '門逢凶迫，財破人傷。'],
 '乙己': ['日奇入墓', '平', '被土暗昧，門凶必凶，得三吉門為地遁。'],
 '乙庚': ['日奇被刑', '凶', '爭訟財產，夫妻懷私。'],
 '乙辛': ['青龍逃走', '凶', '奴僕拐帶，六畜皆傷。'],
 '乙壬': ['日奇入地', '凶', '尊卑悖亂，官訟是非。'],
 '乙癸': ['華蓋逢星', '平', '官遁跡修道，隱匿藏形，躲災避難為吉。'],
 '丙乙': ['日月並行', '吉', '公謀私為皆吉。'],
 '丙丙': ['月奇孛師', '凶', '文書逼迫，破耗遺失。'],
 '丙丁': ['月奇朱雀', '吉', '貴人文書吉利，常人平靜，得三吉門為天遁。'],
 '丙戊': ['飛鳥跌穴', '吉', '謀為百事洞澈。'],
 '丙己': ['太孛入刑', '凶', '囚人刑杖，文書不行，吉門得吉，凶門轉凶。'],
 '丙庚': ['熒入太白', '凶', '門戶破敗，盜賊耗失。'],
 '丙辛': ['日月相會', '吉', '謀事能成。'],
 '丙壬': ['火入天羅', '凶', '為客不利，是非頗多。'],
 '丙癸': ['華蓋孛師', '凶', '陰人害事，災禍頻生。'],
 '丁乙': ['玉女奇生', '吉', '貴人加官進爵，常人婚姻財喜。'],
 '丁丙': ['星隨月轉', '吉', '貴人越級高升，常人樂里生悲。'],
 '丁丁': ['奇入太陰', '吉', '文書即至，喜事遂心。'],
 '丁戊': ['青龍轉光', '吉', '官人升遷，常人威昌。'],
 '丁己': ['火入勾陳', '平', '奸私讎冤，事因女人。'],
 '丁庚': ['玉女刑殺', '平', '文書阻隔，行人必歸。'],
 '丁辛': ['玉女伏虎', '凶', '罪人釋囚，官人失位。'],
 '丁壬': ['五神互合', '吉', '貴人恩昭，訟獄公平。'],
 '丁癸': ['朱雀投江', '凶', '文書口舌俱消，音信沉溺。'],
 '戊乙': ['青龍和會', '凶', '門吉事吉，門凶事凶。'],
 '戊丙': ['青龍返首', '吉', '動作大吉，若逢迫、墓、擊、刑，吉事成凶。'],
 '戊丁': ['青龍耀明', '吉', '謁貴求名吉利，若值墓、迫，招是招非。'],
 '戊戊': ['青龍伏吟', '凶', '凡事閉塞，靜守為吉'],
 '戊己': ['貴人入獄', '中平', '公私皆不利。'],
 '戊庚': ['值符飛宮', '凶', '吉事不吉，凶事更凶。'],
 '戊辛': ['青龍折足', '凶', '吉門生助尚可謀為，若逢凶門，主招災、失財、有足疾。'],
 '戊壬': ['青龍破獄', '凶', '凡陰陽皆不吉利。'],
 '戊癸': ['青龍華蓋', '吉', '吉格者吉，招福，門凶多乖。'],
 '己乙': ['墓神不明', '凶', '地戶蓬星，宜遁跡隱形為利逸。'],
 '己丙': ['火孛地戶', '凶', '陽人冤枉相害，陰人必致淫污。'],
 '己丁': ['朱雀入墓', '凶', '文狀詞訟，先曲後直。'],
 '己戊': ['犬遇青龍', '平', '門吉謀望遂意，上人見喜，門凶枉勞心機'],
 '己己': ['地戶逢鬼', '凶', '病者必死，百事不遂。'],
 '己庚': ['刑格返名', '凶', '求名、詞訟先動者不利，陰星有謀害之情。'],
 '己辛': ['游魂入墓', '凶', '大人鬼魅，小人家先為祟。'],
 '己壬': ['地網高張', '凶', '狡童佚女，奸情殺傷。'],
 '己癸': ['地刑玄武', '凶', '男女疾病垂危，詞訟有囚獄之災。'],
 '庚乙': ['太白蓬星', '凶', '退吉進凶。'],
 '庚丙': ['太白入熒', '凶', '占賊必來，為客進利，為主破財。'],
 '庚丁': ['太白受刑', '凶', '因私暱起官司，門吉有救。'],
 '庚戊': ['天乙伏宮', '凶', '百事不可謀為凶。'],
 '庚己': ['太白大刑', '凶', '官司被重刑。'],
 '庚庚': ['太白同宮', '凶', '官災橫禍，兄弟雷攻。'],
 '庚辛': ['太白重鋒', '凶', '遠行車折馬死。'],
 '庚壬': ['太白退位', '凶', '遠行失迷道路，男女音信嗟呀。'],
 '庚癸': ['太白沖刑', '凶', '行人至官司止，生產母子俱傷，大凶。'],
 '辛乙': ['白虎猖狂', '凶', '人亡家敗，遠行多殃，尊長不喜，車船俱傷。'],
 '辛丙': ['干合孛師', '凶', '熒惑出現，占雨無，占晴旱，占事必因財致訟。'],
 '辛丁': ['獄神得奇', '吉', '經商獲倍利，因人逢赦宥。'],
 '辛戊': ['困龍被傷', '凶', '官司破敗，屈抑守分，妄動禍殃。'],
 '辛己': ['入獄自刑', '凶', '奴僕背主，訟訴難伸。'],
 '辛庚': ['白虎出力', '凶', '刀刃相接，主客相殘，遜讓退步，稍可強進，血濺衣衫。'],
 '辛辛': ['伏吟天庭', '凶', '公廢私就，訟獄自罹罪名。'],
 '辛壬': ['凶蛇入獄', '凶', '兩男爭女，訟獄不息，先動失理。'],
 '辛癸': ['天牢華蓋', '凶', '日月失明，誤入天網，動止乖張。'],
 '壬乙': ['小蛇得勢', '吉', '女子柔順，男人嗟呀，占孕生子，祿馬光華。'],
 '壬丙': ['水蛇入火', '凶', '官災刑禁絡繹不絕。'],
 '壬丁': ['干合蛇刑', '凶', '文書牽連，貴人匆匆，男凶女吉。'],
 '壬戊': ['小蛇化龍', '吉', '男人發達，女產嬰童。'],
 '壬己': ['凶蛇入獄', '凶', '大禍將至，順守斯吉，詞訟理曲。'],
 '壬庚': ['太白擒蛇', '凶', '刑獄公平，立剖。'],
 '壬辛': ['螣蛇相纏', '凶', '縱得吉門，亦不能安，若有謀望，被人欺瞞。'],
 '壬壬': ['蛇入地羅', '凶', '外人纏繞，內事索索，門吉星凶，庶免蹉跎。'],
 '壬癸': ['幼女奸淫', '凶', '家有醜聲，門星俱吉，反禍福隆。'],
 '癸乙': ['華蓋蓬星', '吉', '貴人祿位，常人平安。'],
 '癸丙': ['華蓋孛師', '吉', '貴賤逢之，上人見喜。'],
 '癸丁': ['螣蛇妖矯', '凶', '文書官司，火焚莫逃。'],
 '癸戊': ['天乙會合', '吉', '財喜婚姻，吉人贊助成合，若門凶迫制，反招官非。'],
 '癸己': ['華蓋地戶', '平', '男女占之，書信皆阻，躲災避難為吉。'],
 '癸庚': ['太白入網', '平', '以暴爭訟力平。'],
 '癸辛': ['網蓋天牢', '凶', '占訟占病，死罪莫逃。'],
 '癸壬': ['複見螣蛇', '平', '嫁娶重婚，後嫁無子，不保年華。'],
 '癸癸': ['天網四張', '凶', '行人失伴，病訟皆傷。']}
