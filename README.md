<div align="center">

# 🔮 堅奇門 · KinQiMen

### Python 奇門遁甲排盤系統 | Python Qimen Dunjia Divination System

![banner](https://github.com/kentang2017/kinqimen/blob/master/assets/banner.png)

**千年玄術，一行代碼 · Ancient Wisdom, Modern Code**

[![Python](https://img.shields.io/pypi/pyversions/kinqimen?label=Python&logo=python)](https://pypi.org/project/kinqimen/)
[![PIP Version](https://img.shields.io/pypi/v/kinqimen?label=PyPI&logo=pypi)](https://pypi.org/project/kinqimen/)
[![Downloads](https://img.shields.io/pypi/dm/kinqimen?label=Downloads&logo=pypi&color=blue)](https://pypi.org/project/kinqimen/)
[![License](https://img.shields.io/github/license/kentang2017/kinqimen?label=License)](LICENSE)
[![Telegram](https://img.shields.io/badge/Chat-Telegram-blue?logo=telegram)](https://t.me/haizhonggum)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?logo=paypal)](https://www.paypal.me/kinyeah)

**🌐 線上排盤 · Live Demo → [kinqimen.streamlitapp.com](https://kinqimen.streamlitapp.com)**

</div>

---

## 📖 導讀 · Introduction

> 奇門遁甲與大六壬、太乙神數並稱**中國三大神秘預測術**，歷代只有天子身邊的國師、軍師方能習得。
>
> *Qimen Dunjia is one of the legendary **Three Arts** of Chinese metaphysical divination — historically reserved for imperial advisors and military strategists.*

**奇門遁甲**（Qimen Dunjia）乃中國古代最高深的預測學之一。以洛書九宮為盤，配合陰陽五行、八卦、天干地支及二十四節氣，構建出一個時空旋轉的宇宙能量矩陣。全盤共有**1,080種局**，每個時辰輪換，精準捕捉天地人三才之氣，廣泛應用於決策、方位、商業及個人趨吉避凶。

Qimen Dunjia is an ancient Chinese cosmic divination art that maps heaven, earth and human energies onto a 3×3 magic square of **Nine Palaces**. Rotating through **1,080 unique configurations** — one per double-hour — it incorporates yin-yang theory, the Five Elements, Eight Trigrams, Heavenly Stems, Earthly Branches, and the 24 Solar Terms. Used for centuries in military strategy, business decisions, travel planning, and personal forecasting.

---

## ✨ 功能特色 · Features

| 功能 Feature | 說明 Description |
|---|---|
| 🕐 **時家奇門** Hour-based Qimen | 以時辰起盤，最常用之傳統起盤方式 · Classic hour-based divination chart |
| ⏱ **刻家奇門** Minute-based Qimen | 以分鐘精算，適合精確預測 · High-precision minute-level chart |
| 📜 **金函玉鏡** Golden Mirror | 金函日家奇門，古典日家排盤 · Classic daily Golden Letter Jade Mirror style |
| 🔄 **拆補 / 置閏** Two Calculation Methods | 支援拆補法及置閏法，靈活對應各派 · Supports both Chabu & Zhirun methods |
| 🖥 **Web 排盤介面** Web UI | Streamlit 互動式線上排盤 · Interactive online chart via Streamlit |
| 🐍 **純 Python** Pure Python | 輕量易用，可嵌入任何 Python 項目 · Lightweight and easy to integrate |

---

## 🚀 安裝 · Installation

```bash
pip install sxtwl
pip install kinqimen
```

---

## ⚡ 快速上手 · Quickstart

```python
from kinqimen import kinqimen

year, month, day, hour, minute = 2024, 6, 15, 14, 30

# 時家奇門（拆補法） | Hour-based Qimen (Chabu method)
result = kinqimen.Qimen(year, month, day, hour, minute).pan(1)   # 1=拆補, 2=置閏

# 刻家奇門（置閏法） | Minute-based Qimen (Zhirun method)
result = kinqimen.Qimen(year, month, day, hour, minute).pan_minute(2)

# 金函玉鏡日家奇門 | Golden Letter Jade Mirror daily chart
result = kinqimen.Qimen(year, month, day, hour, minute).gpan()

# 綜合排盤（時家 + 金函） | Combined chart (Hour-based + Golden Mirror)
result = kinqimen.Qimen(year, month, day, hour, minute).overall()
```

---

## 🗺 排盤示意 · Chart Preview

```
＼  天蓬神　 │  天芮神　 │  天沖神　／
 ─────────┬──┴─────┬─────┴──────────
 　│　　螣蛇　　　 │　　太陰　　　 │　　六合　　　 │
 　│　　休門　　天乙│　　死門　　天英│　　傷門　　天柱│
 　│　　天蓬　　坎一│　　天芮　　坤二│　　天沖　　震三│
 辰├───────────┼───────────┼───────────┤酉
 勾│　　白虎　　　 │　　　　　　 │　　玄武　　　 │陳
 陳│　　杜門　　天沖│　　　　　戊  │　　開門　　天任│武
 　│　　天輔　　巽四│　　　　　　 │　　天心　　乾六│
 　├───────────┼───────────┼───────────┤
 　│　　朱雀　　　 │　　九地　　　 │　　九天　　　 │
 卯│　　景門　　天任│　　生門　　天柱│　　驚門　　天芮│戌
 　│　　天英　　離九│　　天心　　兌七│　　天蓬　　艮八│
 ／─────────┬──┴─────┬─────┴──┬────────＼
／  寅　　　 │  丑　　 │  子　　 │  　 亥　　 ＼
```

---

## 📦 依賴套件 · Dependencies

- [`sxtwl`](https://pypi.org/project/sxtwl/) — 中國農曆/節氣計算 · Chinese lunar calendar & solar terms
- [`kinliuren`](https://pypi.org/project/kinliuren/) — 大六壬排盤 · Da Liu Ren divination
- [`streamlit`](https://streamlit.io/) — Web 互動介面 · Web UI framework
- [`pendulum`](https://pendulum.eustace.io/) — 時區處理 · Timezone handling

---

## 🌐 線上排盤 · Web App

無需安裝，直接在瀏覽器中體驗奇門排盤：

**Try it instantly in your browser — no installation needed:**

👉 **[https://kinqimen.streamlitapp.com](https://kinqimen.streamlitapp.com)**

---

## 💬 社群 · Community

| 平台 Platform | 連結 Link |
|---|---|
| 💬 Telegram 討論群 | [@haizhonggum](https://t.me/haizhonggum) |
| 🐛 問題回報 Issues | [GitHub Issues](https://github.com/kentang2017/kinqimen/issues) |
| ☕ 支持作者 Donate | [PayPal](https://www.paypal.me/kinyeah) |

---

## 📣 微信公眾號 · WeChat Official Account

<div align="center">

![WeChat QR](https://raw.githubusercontent.com/kentang2017/kinliuren/refs/heads/master/pic/%E5%9C%96%E7%89%87_20260316084148.jpg)

*掃碼關注，獲取更多玄學資訊 · Scan to follow for more metaphysics content*

</div>

---

## 📄 授權 · License

本項目以 MIT 授權條款開源 · This project is open-sourced under the [MIT License](LICENSE).

---

<div align="center">

**如果這個項目對您有幫助，歡迎點亮 ⭐ Star！**

*If you find this project useful, please give it a ⭐ Star — it means a lot!*

Made with ❤️ by [kentang2017](https://github.com/kentang2017)

</div>





