import streamlit as st
import pendulum as pdlm
from io import StringIO
from contextlib import contextmanager, redirect_stdout
import streamlit.components.v1 as components
import kinqimen
from kinliuren import kinliuren

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
        
st.set_page_config(layout="wide",page_title="堅奇門 - 奇門遁甲排盘")
pan,example,guji,update = st.tabs([' 排盤 ', ' 案例 ', ' 古籍 ',' 日誌 ' ])
with st.sidebar:
    pp_date=st.date_input("日期",pdlm.now(tz='Asia/Shanghai').date())
    pp_time=st.time_input("時間",pdlm.now(tz='Asia/Shanghai').time())
    p = str(pp_date).split("-")
    pp = str(pp_time).split(":")
    y = int(p[0])
    m = int(p[1])
    d = int(p[2])
    h = int(pp[0])
    min = int(pp[1])
    
with pan:
    st.header('奇門排盘')
    qtext = kinqimen.Qimen(y,m,d,h,min).pan()
    eg = list("巽離坤震兌艮坎乾")
    qd = [qtext.get("地盤").get(i) for i in eg]
    try:
        qt = [qtext.get("天盤").get(i)[0] for i in eg]
    except KeyError:
        qt = [qtext.get("天盤").get(i) for i in eg]
    god = [qtext.get("神").get(i) for i in eg]
    door = [qtext.get("門").get(i) for i in eg]
    star = [qtext.get("星").get(i) for i in eg]
    md = qtext.get("地盤").get("中")
    output4 = st.empty()
    with st_capture(output4.code):
        print("{} |\n{} | 節氣︰{} |\n值符星宮︰天{}宮 | 值使門宮︰{}\n".format(qtext.get("干支"), qtext.get("排局"), qtext.get("節氣"),  qtext.get("值符值使").get("值符星宮")[0]+"-"+qtext.get("值符值使").get("值符星宮")[1], qtext.get("值符值使").get("值使門宮")[0]+"門"+qtext.get("值符值使").get("值使門宮")[1]+"宮" ))
        print("＼          │        │        │          ／")
        print("  ＼────────┴──┬─────┴─────┬──┴────────／")
        print(" 　│　　{}　　　 │　　{}　　　 │　　{}　　　 │".format(god[0], god[1], god[2]))
        print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[0], qt[0], door[1], qt[1], door[2], qt[2]))
        print("　─┤　　{}　　{} │　　{}　　{} │　　{}　　{} ├─".format(star[0], qd[0], star[1], qd[1], star[2], qd[2]))
        print(" 　├───────────┼───────────┼───────────┤")
        print(" 　│　　{}　　　 │　　　　　　 │　　{}　　　 │".format(god[3], god[4]))
        print("　─┤　　{}　　{} │　　　　　　 │　　{}　　{} ├─".format(door[3], qt[3],  door[4], qt[4]))
        print(" 　│　　{}　　{} │　　　　　{} │　　{}　　{} │".format(star[3], qd[3], md, star[4], qd[4]))
        print(" 　├───────────┼───────────┼───────────┤")
        print("　─┤　　{}　　　 │　　{}　　　 │　　{}　　　 ├─".format(god[5], god[6], god[7]))
        print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(door[5], qt[5], door[6], qt[6], door[7], qt[7]))
        print(" 　│　　{}　　{} │　　{}　　{} │　　{}　　{} │".format(star[5], qd[5], star[6], qd[6], star[7], qd[7]))
        print("  ／────────┬──┴─────┬─────┴──┬────────＼")
        print("／          │        │        │          ＼")
    expander = st.expander("原始碼")
    expander.write(str(qtext))
