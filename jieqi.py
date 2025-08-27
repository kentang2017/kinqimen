# -*- coding: utf-8 -*-
"""
Created on Wed Aug 27 08:25:17 2025

@author: hooki
"""

import datetime
import  sxtwl

jqmc = ['小寒', '大寒', '立春', '雨水', '驚蟄', '春分', '清明', '穀雨', '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']


#%% 節氣計算
def get_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the current solar term (jieqi) for the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Check if the given date has a solar term
    if day.hasJieQi():
        jq_index = day.getJieQi()
        jd = day.getJieQiJD()
        t = sxtwl.JD2DD(jd)
        return {
            "年": t.Y,
            "月": t.M,
            "日": t.D,
            "時": int(t.h),
            "分": round(t.m),
            "節氣": jqmc[jq_index-1],
            "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
        }
    else:
        # If no solar term on this day, find the previous solar term
        current_day = day
        while True:
            current_day = current_day.before(1)
            if current_day.hasJieQi():
                jq_index = current_day.getJieQi()
                jd = current_day.getJieQiJD()
                t = sxtwl.JD2DD(jd)
                return {
                    "年": t.Y,
                    "月": t.M,
                    "日": t.D,
                    "時": int(t.h),
                    "分": round(t.m),
                    "節氣": jqmc[jq_index-1],
                    "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
                }
            
def get_before_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the next solar term (jieqi) after the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Start searching from the next day
    current_day = day.before(15)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y,
                "月": t.M,
                "日": t.D,
                "時": int(t.h),
                "分": round(t.m),
                "節氣": jqmc[jq_index-1],
                "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.before(1)

def get_next_jieqi_start_date(year, month, day, hour, minute):
    """
    Get the start date and time of the next solar term (jieqi) after the given date and time.
    Returns a dictionary with year, month, day, hour, minute, and the name of the solar term.
    """
    # Initialize the day object with the given date
    day = sxtwl.fromSolar(year, month, day)
    
    # Start searching from the next day
    current_day = day.after(1)
    while True:
        if current_day.hasJieQi():
            jq_index = current_day.getJieQi()
            jd = current_day.getJieQiJD()
            t = sxtwl.JD2DD(jd)
            return {
                "年": t.Y,
                "月": t.M,
                "日": t.D,
                "時": int(t.h),
                "分": round(t.m),
                "節氣": jqmc[jq_index-1],
                "時間":datetime.datetime(t.Y, t.M, t.D, int(t.h), round(t.m))
            }
        current_day = current_day.after(1)


def jq(year, month, day, hour, minute):
    """
    Get the current solar term (jieqi) for the given date and time.
    Returns the name of the solar term as a string.
    """
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
        
        if not (isinstance(jq_start_datetime, datetime.datetime) and isinstance(next_jq_start_datetime, datetime.datetime)):
            raise ValueError(f"Jieqi times are not datetime objects: {jq_start_datetime}, {next_jq_start_datetime}")
        
        # Check if current_datetime is within the current jieqi period
        if jq_start_datetime <= current_datetime < next_jq_start_datetime:
            return jq_name
        # If before the current jieqi start, get the previous jieqi
        elif current_datetime < jq_start_datetime:
            prev_jq_start_dict = get_before_jieqi_start_date(year, month, day, hour, minute)
            if not (isinstance(prev_jq_start_dict, dict) and "節氣" in prev_jq_start_dict):
                raise ValueError(f"Invalid previous jieqi dictionary format for {year}-{month}-{day}")
            return prev_jq_start_dict["節氣"]
        else:
            raise ValueError(f"Current datetime {current_datetime} not within any valid jieqi period")
    except Exception as e:
        raise ValueError(f"Error in jq for {year}-{month}-{day} {hour}:{minute}: {str(e)}")
        

if __name__ == '__main__':
    year = 2025
    month = 1
    day = 15
    hour = 17
    minute = 36
    #print(liujiashun_dict())
    #print(qimen_ju_name_zhirun_raw(year, month, day, hour, minute))
    print(f"{year}-{month}-{day} {hour}:{minute}")
    #print( get_jieqi_start_date(year, month, day, hour, minute))
    #print( get_next_jieqi_start_date(year, month, day, hour, minute))
    #print( get_before_jieqi_start_date(year, month, day, hour, minute))
    print(jq(year, month, day, hour, minute))
        