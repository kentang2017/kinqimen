import urllib
import streamlit as st
import pendulum as pdlm
from io import StringIO
import datetime
from contextlib import contextmanager, redirect_stdout
import kinqimen
from kinliuren import kinliuren
import config

BASE_URL_KINLIUREN = 'https://raw.githubusercontent.com/kentang2017/kinliuren/master/'

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write
        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret
        stdout.write = new_write
        yield

def get_file_content_as_string(base_url, path):
    url = base_url + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

def display_pan(qtext, lunar_month, gz, num, eg, e_to_s, e_to_g):
    qd = [qtext.get("地盤").get(i) for i in eg]
    qt = [qtext.get("天盤").get(i) for i in eg]
    god = [qtext.get("神").get(i) for i in eg]
    door = [qtext.get("門").get(i) for i in eg]
    star = [qtext.get("星").get(i) for i in eg]
    md = qtext.get("地盤").get("中")

    st.write(f"{'時家奇門' if num == 1 else '刻家奇門'} | {qtext.get('排盤方式')}")
    st.write(f"{y}年{m}月{d}日{h}時\n")
    st.write(f"{qtext.get('干支')} |\n{qtext.get('排局')} | 節氣︰{j_q} |\n值符星宮︰天{qtext.get('值符值使').get('值符星宮')[0]}宮 | 值使門宮︰{qtext.get('值符值使').get('值使門宮')[0]}門{qtext.get('值符值使').get('值使門宮')[1]}宮\n")
    
    layout = [
        ["巳", "午", "未", "申"],
        ["辰", "酉"],
        ["卯", "戌"],
        ["寅", "丑", "子", "亥"]
    ]
    
    for row in layout:
        st.write(f"＼ {' | '.join([f'{e_to_s[i]}{e_to_g[i]}' for i in row])} ／")
        st.write(" │ ".join([f"{god[i]} {door[i]} {qt[i]} {star[i]} {qd[i]}" for i in row if i in eg]))
    
    expander = st.expander("原始碼")
    expander.write(str(qtext))

st.set_page_config(layout="wide", page_title="堅奇門 - 奇門遁甲排盘")
pan, example, guji, log, links = st.tabs(['🧮排盤', '📜案例', '📚古籍', '🆕更新', '🔗連結'])

with st.sidebar:
    pp_date = st.date_input("日期", pdlm.now(tz='Asia/Shanghai').date())
    pp_time = st.time_input("時間", pdlm.now(tz='Asia/Shanghai').time())
    option = st.selectbox('起盤方式', ('時家奇門', '刻家奇門'))
    option2 = st.selectbox('排盤', ('置閏', '拆補'))
    num = dict(zip(['時家奇門', '刻家奇門'], [1, 2])).get(option)
    pai = dict(zip(['拆補', '置閏'], [1, 2])).get(option2)
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y, m, d, h, minute = int(p[0]), int(p[1]), int(p[2]), int(pp[0]), int(pp[1])
    manual = st.button('手動盤')
    instant = st.button('即時盤')

with links:
    st.header('連結')
    st.markdown(get_file_content_as_string(BASE_URL_KINLIUREN, "update.md"), unsafe_allow_html=True)

with log:
    st.header('更新')
    st.markdown(get_file_content_as_string(BASE_URL_KINLIUREN, "log.md"))

with pan:
    st.header('堅奇門')
    output4 = st.empty()
    with st_capture(output4.code):
        try:
            if manual or instant:
                if instant:
                    now = datetime.datetime.now()
                    y, m, d, h, minute = now.year, now.month, now.day, now.hour, now.minute
                
                gz = config.gangzhi(y, m, d, h, minute)
                j_q = config.jq(y, m, d, h, minute)
                eg = list("巽離坤震兌艮坎乾")
                lunar_month = dict(zip(range(1, 13), config.cmonth)).get(config.lunar_date_d(y, m, d).get("月"))

                if num == 1:
                    qtext = kinqimen.Qimen(y, m, d, h, minute).pan(pai)
                    lr = kinliuren.Liuren(qtext.get("節氣"), lunar_month, gz[2], gz[3]).result(0)
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                elif num == 2:
                    qtext = kinqimen.Qimen(y, m, d, h, minute).pan_minute(pai)
                    lr = kinliuren.Liuren(qtext.get("節氣"), lunar_month, gz[3], gz[4]).result(0)
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                
                display_pan(qtext, lunar_month, gz, num, eg, e_to_s, e_to_g)
        except ValueError:
            st.empty()
