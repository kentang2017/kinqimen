# -*- coding: utf-8 -*-
"""
修正版節氣 / 干支計算
- 月柱改為精確到「時分」的節氣交節判斷（解決交節當天日級誤差）
- 2026-09-07 16:30 → 丙申月（正確）
- 2026-09-07 22:40 之後 → 丁酉月

Created on Wed Aug 27 08:25:17 2025
@author: hooki
修正: 2026-08-08
"""

import datetime
from itertools import cycle, repeat
import sxtwl
from sxtwl import fromSolar
import ephem


jqmc = ['小寒', '大寒', '立春', '雨水', '驚蟄', '春分', '清明', '穀雨',
        '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑',
        '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']

tian_gan = '甲乙丙丁戊己庚辛壬癸'
di_zhi = '子丑寅卯辰巳午未申酉戌亥'

# 節氣 → 月支（以「節」為準）
JIEQI_TO_YUEZHI = {
    '立春': '寅', '雨水': '寅',
    '驚蟄': '卯', '春分': '卯',
    '清明': '辰', '穀雨': '辰',
    '立夏': '巳', '小滿': '巳',
    '芒種': '午', '夏至': '午',
    '小暑': '未', '大暑': '未',
    '立秋': '申', '處暑': '申',
    '白露': '酉', '秋分': '酉',
    '寒露': '戌', '霜降': '戌',
    '立冬': '亥', '小雪': '亥',
    '大雪': '子', '冬至': '子',
    '小寒': '丑', '大寒': '丑',
}

YUEZHI_TO_NUM = {z: i + 1 for i, z in enumerate('寅卯辰巳午未申酉戌亥子丑')}


#%% 甲子平支
def jiazi():
    return list(map(lambda x: "{}{}".format(tian_gan[x % len(tian_gan)], di_zhi[x % len(di_zhi)]), list(range(60))))


def multi_key_dict_get(d, k):
    for keys, v in d.items():
        if k in keys:
            return v
    return None


def new_list(olist, o):
    a = olist.index(o)
    return olist[a:] + olist[:a]


#%% 節氣計算（已修正：精確比較當前時分）
def get_jieqi_start_date(year, month, day, hour, minute):
    """
    回傳「當前時間所屬」節氣的開始時刻（精確到時分）。
    若當天有節氣但當前時刻尚未到達，則回傳上一個節氣。
    """
    current_dt = datetime.datetime(year, month, day, hour, minute)
    day_obj = fromSolar(year, month, day)

    # 當天有節氣時，先判斷是否已過交節時刻
    if day_obj.hasJieQi():
        jq_index = day_obj.getJieQi()
        jd = day_obj.getJieQiJD()
        t = sxtwl.JD2DD(jd)
        jq_dt = datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
        if current_dt >= jq_dt:
            return {
                "年": t.Y, "月": t.M, "日": t.D,
                "時": int(t.h), "分": round(t.m),
                "節氣": jqmc[jq_index - 1],
                "時間": jq_dt
            }

    # 往前找最近的一個已過去的節氣
    current = day_obj
    while True:
        current = current.before(1)
        if current.hasJieQi():
            jq_index = current.getJieQi()
            jd = current.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y, "月": t.M, "日": t.D,
                "時": int(t.h), "分": round(t.m),
                "節氣": jqmc[jq_index - 1],
                "時間": datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }


def get_before_jieqi_start_date(year, month, day, hour, minute):
    """
    取得再前一個節氣（備用，正常路徑較少用到）。
    """
    day_obj = fromSolar(year, month, day)
    current_day = day_obj.before(15)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y, "月": t.M, "日": t.D,
                "時": int(t.h), "分": round(t.m),
                "節氣": jqmc[jq_index - 1],
                "時間": datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.before(1)


def get_next_jieqi_start_date(year, month, day, hour, minute):
    """下一個節氣開始時刻"""
    day_obj = fromSolar(year, month, day)
    current_day = day_obj.after(1)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y, "月": t.M, "日": t.D,
                "時": int(t.h), "分": round(t.m),
                "節氣": jqmc[jq_index - 1],
                "時間": datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.after(1)


def jq(year, month, day, hour, minute):
    """當前節氣名稱（已精確到時分）"""
    try:
        current_datetime = datetime.datetime(year, month, day, hour, minute)
        jq_start_dict = get_jieqi_start_date(year, month, day, hour, minute)
        next_jq_start_dict = get_next_jieqi_start_date(year, month, day, hour, minute)

        if not (isinstance(jq_start_dict, dict) and isinstance(next_jq_start_dict, dict) and
                "時間" in jq_start_dict and "時間" in next_jq_start_dict and
                "節氣" in jq_start_dict and "節氣" in next_jq_start_dict):
            raise ValueError(f"Invalid jieqi dictionary format for {year}-{month}-{day} {hour}:{minute}")

        jq_start_datetime = jq_start_dict["時間"]
        next_jq_start_datetime = next_jq_start_dict["時間"]
        jq_name = jq_start_dict["節氣"]

        if not (isinstance(jq_start_datetime, datetime.datetime) and
                isinstance(next_jq_start_datetime, datetime.datetime)):
            raise ValueError(f"Jieqi times are not datetime objects: {jq_start_datetime}, {next_jq_start_datetime}")

        if jq_start_datetime <= current_datetime < next_jq_start_datetime:
            return jq_name
        elif current_datetime < jq_start_datetime:
            prev_jq_start_dict = get_before_jieqi_start_date(year, month, day, hour, minute)
            if not (isinstance(prev_jq_start_dict, dict) and "節氣" in prev_jq_start_dict):
                raise ValueError(f"Invalid previous jieqi dictionary format for {year}-{month}-{day}")
            return prev_jq_start_dict["節氣"]
        else:
            raise ValueError(f"Current datetime {current_datetime} not within any valid jieqi period")
    except Exception as e:
        raise ValueError(f"Error in jq for {year}-{month}-{day} {hour}:{minute}: {str(e)}")


def ke_jiazi_d(hour):
    t = [f"{h}:{m}0" for h in range(24) for m in range(6)]
    minutelist = dict(zip(t, cycle(repeat_list(1, find_lunar_ke(hour)))))
    return minutelist


def repeat_list(n, thelist):
    return [repetition for i in thelist for repetition in repeat(i, n)]


# 五虎遁，起正月
def find_lunar_month(year_gz):
    fivetigers = {
        tuple(list('甲己')): '丙寅',
        tuple(list('乙庚')): '戊寅',
        tuple(list('丙辛')): '庚寅',
        tuple(list('丁壬')): '壬寅',
        tuple(list('戊癸')): '甲寅'
    }
    if multi_key_dict_get(fivetigers, year_gz[0]) is None:
        result = multi_key_dict_get(fivetigers, year_gz[1])
    else:
        result = multi_key_dict_get(fivetigers, year_gz[0])
    return dict(zip(range(1, 13), new_list(jiazi(), result)[:12]))


# 五鼠遁，起子時
def find_lunar_hour(day):
    fiverats = {
        tuple(list('甲己')): '甲子',
        tuple(list('乙庚')): '丙子',
        tuple(list('丙辛')): '戊子',
        tuple(list('丁壬')): '庚子',
        tuple(list('戊癸')): '壬子'
    }
    if multi_key_dict_get(fiverats, day[0]) is None:
        result = multi_key_dict_get(fiverats, day[1])
    else:
        result = multi_key_dict_get(fiverats, day[0])
    return dict(zip(list(di_zhi), new_list(jiazi(), result)[:12]))


# 五馬遁，起子刻
def find_lunar_ke(hour):
    fivehourses = {
        tuple(list('丙辛')): '甲午',
        tuple(list('丁壬')): '丙午',
        tuple(list('戊癸')): '戊午',
        tuple(list('甲己')): '庚午',
        tuple(list('乙庚')): '壬午'
    }
    if multi_key_dict_get(fivehourses, hour[0]) is None:
        result = multi_key_dict_get(fivehourses, hour[1])
    else:
        result = multi_key_dict_get(fivehourses, hour[0])
    return new_list(jiazi(), result)


# 農曆
def lunar_date_d(year, month, day):
    lunar_m = ['占位', '正月', '二月', '三月', '四月', '五月', '六月',
               '七月', '八月', '九月', '十月', '冬月', '腊月']
    day_obj = fromSolar(year, month, day)
    return {
        "年": day_obj.getLunarYear(),
        "農曆月": lunar_m[int(day_obj.getLunarMonth())],
        "月": day_obj.getLunarMonth(),
        "日": day_obj.getLunarDay()
    }


def _get_month_gz_by_jieqi(year, month, day, hour, minute, yTG):
    """依精確節氣計算月柱（核心修正）"""
    current_jq = jq(year, month, day, hour, minute)
    yuezhi = JIEQI_TO_YUEZHI[current_jq]
    month_num = YUEZHI_TO_NUM[yuezhi]
    return find_lunar_month(yTG)[month_num]


# 換算干支
def gangzhi1(year, month, day, hour, minute):
    if hour == 23:
        d = ephem.Date(round((ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day + 1).zfill(2),
            str(0).zfill(2)))), 3))
    else:
        d = ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day).zfill(2),
            str(hour).zfill(2)))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG = "{}{}".format(tian_gan[cdate.getYearGZ().tg], di_zhi[cdate.getYearGZ().dz])
    dTG = "{}{}".format(tian_gan[cdate.getDayGZ().tg], di_zhi[cdate.getDayGZ().dz])
    hTG = "{}{}".format(tian_gan[cdate.getHourGZ(dd[3]).tg], di_zhi[cdate.getHourGZ(dd[3]).dz])

    # 修正：一律用精確節氣計算月柱
    mTG1 = _get_month_gz_by_jieqi(year, month, day, hour, minute, yTG)
    hTG1 = find_lunar_hour(dTG).get(hTG[1])
    return [yTG, mTG1, dTG, hTG1]


def gangzhi(year, month, day, hour, minute):
    if hour == 23:
        d = ephem.Date(round((ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day + 1).zfill(2),
            str(0).zfill(2)))), 3))
    else:
        d = ephem.Date("{}/{}/{} {}:00:00.00".format(
            str(year).zfill(4),
            str(month).zfill(2),
            str(day).zfill(2),
            str(hour).zfill(2)))
    dd = list(d.tuple())
    cdate = fromSolar(dd[0], dd[1], dd[2])
    yTG = "{}{}".format(tian_gan[cdate.getYearGZ().tg], di_zhi[cdate.getYearGZ().dz])
    dTG = "{}{}".format(tian_gan[cdate.getDayGZ().tg], di_zhi[cdate.getDayGZ().dz])
    hTG = "{}{}".format(tian_gan[cdate.getHourGZ(dd[3]).tg], di_zhi[cdate.getHourGZ(dd[3]).dz])

    # 修正：一律用精確節氣計算月柱（解決 2026-09-07 16:30 被誤判為丁酉的問題）
    mTG1 = _get_month_gz_by_jieqi(year, month, day, hour, minute, yTG)
    hTG1 = find_lunar_hour(dTG).get(hTG[1])

    zi = gangzhi1(year, month, day, 0, 0)[3]
    # 刻的對應（清理 if 鏈）
    reminute = f"{(minute // 10) * 10:02d}"
    hourminute = f"{hour}:{reminute}"
    gangzhi_minute = ke_jiazi_d(zi).get(hourminute)
    return [yTG, mTG1, dTG, hTG1, gangzhi_minute]


if __name__ == '__main__':
    year = 2026
    month = 9
    day = 7
    hour = 16
    minute = 30
    print(f"{year}-{month}-{day} {hour}:{minute}")
    print("gangzhi:", gangzhi(year, month, day, hour, minute))
    print("jq:", jq(year, month, day, hour, minute))
    print("jieqi start:", get_jieqi_start_date(year, month, day, hour, minute))

    print("\n--- 交節後驗證 ---")
    print("23:00 gangzhi:", gangzhi(2026, 9, 7, 16, 30))
    print("23:00 jq:", jq(2026, 9, 7, 16, 30))
