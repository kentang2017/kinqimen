import urllib
import streamlit as st
import pendulum as pdlm
from io import StringIO
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
        
def get_file_content_as_string(path):
    url = 'https://raw.githubusercontent.com/kentang2017/kinqimen/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

def get_file_content_as_string1(path):
    url = 'https://raw.githubusercontent.com/kentang2017/kinliuren/master/' + path
    response = urllib.request.urlopen(url)
    return response.read().decode("utf-8")

st.set_page_config(layout="wide",page_title="堅奇門 - 奇門遁甲排盘")
pan,example,guji,log,links = st.tabs([' 🧮排盤 ', ' 📜案例 ', ' 📚古籍 ',' 🆕更新 ',' 🔗連結 ' ])
with st.sidebar:
    pp_date=st.date_input("日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time=st.time_input("時間",pdlm.now(tz='Asia/Shanghai').time())
    option = st.selectbox( '起盤方式', ( ' 時家奇門 ', ' 刻家奇門 '))
    option2 = st.selectbox( '排盤', (' 拆補 ',' 置閏 '))
    num = dict(zip([' 時家奇門 ', ' 刻家奇門 '],[1,2])).get(option)
    pai = dict(zip([' 拆補 ',' 置閏 '],[1,2])).get(option2)
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    h = int(pp[0])
    mintue = int(pp[1])
    manual = st.button('手動盤')
    instant = st.button('即時盤')
   
with links:
    st.header('連結')
    st.markdown(get_file_content_as_string1("update.md", unsafe_allow_html=True)

with log:
    st.header('更新')
    st.markdown(get_file_content_as_string1("log.md"))

with pan:
    st.header('堅奇門')
    output4 = st.empty()
    with st_capture(output4.code):
        try:
            if manual:
                gz = config.gangzhi(y,m,d,h,mintue)
                j_q =  config.jq(y, m, d, h, mintue)
                eg = list("巽離坤震兌艮坎乾")
                lunar_month = dict(zip(range(1,13), config.cmonth)).get(config.lunar_date_d(y,m,d).get("月"))
                if num == 1:
                    qtext = kinqimen.Qimen(y,m,d,h,mintue).pan(pai)
                    lr = kinliuren.Liuren( qtext.get("節氣"),lunar_month, gz[2], gz[3]).result(0)
                    qd = [qtext.get("地盤").get(i) for i in eg]
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                    qt = [qtext['天盤'].get(i) for i in eg]
                    god = [qtext.get("神").get(i) for i in eg]
                    door = [qtext.get("門").get(i) for i in eg]
                    star = [qtext.get("星").get(i) for i in eg]
                    md = qtext.get("地盤").get("中")
                    print("時家奇門 | {}".format(qtext.get("排盤方式")))
                    print("{}年{}月{}日{}時\n".format(y,m,d,h))
                    print("{} |\n{} | 節氣︰{} |\n值符天干︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"),  j_q, qtext.get("值符值使").get("值符天干")[0]+qtext.get("值符值使").get("值符天干")[1],  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
                    print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                    print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                    print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                    print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                    print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                    print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                    print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                    print(" 　├───────────┼───────────┼───────────┤")
                    print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                    print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                    print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                    expander = st.expander("原始碼")
                    expander.write(str(qtext))
                if num == 2:
                    qtext = kinqimen.Qimen(y,m,d,h,mintue).pan_minute(pai)
                    lr = kinliuren.Liuren( qtext.get("節氣"),lunar_month, gz[3], gz[4]).result(0)
                    qd = [qtext.get("地盤").get(i) for i in eg]
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                    qt = [qtext.get("天盤").get(i) for i in eg]
                    god = [qtext.get("神").get(i) for i in eg]
                    door = [qtext.get("門").get(i) for i in eg]
                    star = [qtext.get("星").get(i) for i in eg]
                    md = qtext.get("地盤").get("中")
                    print("刻家奇門 | {}".format(qtext.get("排盤方式")))
                    print("{}年{}月{}日{}時\n".format(y,m,d,h))
                    print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"),  j_q,  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
                    print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                    print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                    print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                    print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                    print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                    print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                    print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                    print(" 　├───────────┼───────────┼───────────┤")
                    print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                    print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                    print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                    expander = st.expander("原始碼")
                    expander.write(str(qtext))
                else:
                    output4 = st.empty()
        except ValueError:
            st.empty()
            if instant:
                output4 = st.empty()
                now = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong'))
                y = now.year
                m = now.month
                d = now.day
                h = now.hour
                mintue = now.minute
                gz = config.gangzhi(y,m,d,h,mintue)
                j_q =  config.jq(y, m, d, h, mintue)
                eg = list("巽離坤震兌艮坎乾")
                lunar_month = dict(zip(range(1,13), config.cmonth)).get(config.lunar_date_d(y,m,d).get("月"))
                if num == 1:
                    qtext = kinqimen.Qimen(y,m,d,h,mintue).pan(pai)
                    lr = kinliuren.Liuren( qtext.get("節氣"),lunar_month, gz[2], gz[3]).result(0)
                    qd = [qtext.get("地盤").get(i) for i in eg]
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                    qt = [qtext.get('天盤', {}).get(i) for i in eg]
                    god = [qtext.get("神").get(i) for i in eg]
                    door = [qtext.get("門").get(i) for i in eg]
                    star = [qtext.get("星").get(i) for i in eg]
                    md = qtext.get("地盤").get("中")
                    print("時家奇門 | {}".format(qtext.get("排盤方式")))
                    print("{}年{}月{}日{}時\n".format(y,m,d,h))
                    print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"),  j_q,  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
                    print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                    print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                    print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                    print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                    print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                    print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                    print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                    print(" 　├───────────┼───────────┼───────────┤")
                    print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                    print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                    print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                    expander = st.expander("原始碼")
                    expander.write(str(qtext))
                if num == 2:
                    qtext = kinqimen.Qimen(y,m,d,h,mintue).pan_minute()
                    lr = kinliuren.Liuren( qtext.get("節氣"),lunar_month, gz[3], gz[4]).result(0)
                    qd = [qtext.get("地盤").get(i) for i in eg]
                    e_to_s = lr.get("地轉天盤")
                    e_to_g = lr.get("地轉天將")
                    qt = [qtext.get('天盤', {}).get(i) for i in eg]
                    god = [qtext.get("神").get(i) for i in eg]
                    door = [qtext.get("門").get(i) for i in eg]
                    star = [qtext.get("星").get(i) for i in eg]
                    md = qtext.get("地盤").get("中")
                    print("刻家奇門{}".format(qtext.get("排盤方式")))
                    print("{}年{}月{}日{}時\n".format(y,m,d,h))
                    print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"),  j_q,  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
                    print("＼  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ／".format(e_to_s.get("巳"),e_to_g.get("巳"),e_to_s.get("午"),e_to_g.get("午"),e_to_s.get("未"),e_to_g.get("未"),e_to_s.get("申"),e_to_g.get("申")))
                    print("  ＼────────┴──┬─────┴─────┬──┴────────／")
                    print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
                    print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
                    print(" {}├───────────┼───────────┼───────────┤{}".format(e_to_s.get("辰"),e_to_s.get("酉")))
                    print(" {}│　　{}　　　 │　　　　　　 │　　{}　　　 │{}".format(e_to_g.get("辰"),god[3], god[4],e_to_g.get("酉")))
                    print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
                    print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
                    print(" 　├───────────┼───────────┼───────────┤")
                    print("　 │　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[5], god[6], god[7]))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_s.get("卯"),door[5], qt[5], door[6], qt[6], door[7], qt[7], e_to_s.get("戌")))
                    print(" {}│　　{}　　{} │　　{}　　{} │　　{}　　{} │{}".format(e_to_g.get("卯"),star[5], qd[5], star[6], qd[6], star[7], qd[7], e_to_g.get("戌")))
                    print("  ／────────┬──┴─────┬─────┴──┬────────＼")
                    print("／  {}{}  　 │  {}{}　 │  {}{}　 │  　 {}{}　 ＼".format(e_to_s.get("寅"),e_to_g.get("寅"),e_to_s.get("丑"),e_to_g.get("丑"),e_to_s.get("子"),e_to_g.get("子"),e_to_s.get("亥"),e_to_g.get("亥")))
                    expander = st.expander("原始碼")
                    expander.write(str(qtext))
                else:
                    output4 = st.empty()
        except ValueError:
            st.empty()
