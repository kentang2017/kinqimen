import math
import os
import json
from urllib import error as urllib_error
from urllib import request as urllib_request
import streamlit as st
import pendulum as pdlm
import datetime, pytz

import kinqimen
import config
from cerebras_client import CerebrasClient, RateLimitError, DEFAULT_MODEL as DEFAULT_CEREBRAS_MODEL

def load_local_md(filepath):
    """讀取本地 Markdown 檔案，若檔案不存在則回傳提示訊息。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ 找不到檔案：{filepath}"

# ------------------- AI 相關常數與函數 -------------------
CEREBRAS_FREE_MODEL_OPTIONS = [
    "qwen-3-235b-a22b-instruct-2507",
    "llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b",
    "deepseek-r1-distill-llama-70b",
    "llama3.1-8b",
]
CEREBRAS_MODEL_DESCRIPTIONS = {
    "qwen-3-235b-a22b-instruct-2507": "Cerebras 免費模型：推理速度快，適合日常分析。",
    "llama-4-scout-17b-16e-instruct": "Cerebras 免費模型：指令遵循穩定，整體均衡。",
    "llama-3.3-70b": "Cerebras 免費模型：能力較強，適合複雜問題。",
    "deepseek-r1-distill-llama-70b": "Cerebras 免費模型：推理風格偏強。",
    "llama3.1-8b": "Cerebras 免費模型：輕量低成本。",
}
DEFAULT_OPENAI_COMPATIBLE_SERVER = "https://api.openai.com/v1"
PROVIDER_CEREBRAS = "Cerebras"
PROVIDER_OPENAI_COMPATIBLE = "OpenAICompatible"
PROVIDER_LABELS = {
    PROVIDER_CEREBRAS: "Cerebras 免費模型",
    PROVIDER_OPENAI_COMPATIBLE: "OpenAI 相容服務（自訂）",
}

SYSTEM_PROMPTS_FILE = "data/system_prompts.json"

def load_system_prompts():
    DEFAULT_SYSTEM_PROMPT = (
        "你是一位奇門遁甲大師，精通《奇門遁甲統宗》、《奇門遁甲秘笈大全》、《煙波釣叟歌》等古籍及歷史案例。"
        "請根據提供的奇門遁甲排盤數據，進行以下操作：\n"
        "1. 解釋盤局的關鍵要素（九宮、天盤、地盤、九星、八門、八神、值符值使等）。\n"
        "2. 結合奇門遁甲理論，分析盤局的吉凶格局和潛在影響。\n"
        "3. 詳細評估各宮位的組合關係。\n"
        "4. 提供實用的建議或應對策略。\n"
        "請以清晰的結構（分段、標題）呈現，語言專業且易懂，適當引用歷史案例或經典理論。"
    )
    try:
        with open(SYSTEM_PROMPTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        default_data = {
            "prompts": [{"name": "奇門遁甲大師", "content": DEFAULT_SYSTEM_PROMPT}],
            "selected": "奇門遁甲大師",
        }
        with open(SYSTEM_PROMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)
        return default_data

def save_system_prompts(prompts_data):
    try:
        with open(SYSTEM_PROMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump(prompts_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        st.error(f"儲存系統提示時發生錯誤：{e}")
        return False

def _extract_message_text(content):
    """Extract plain text from provider message content formats."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)
        return "\n".join(parts).strip()
    return str(content)

def _normalize_base_url(base_url):
    """Normalize API base URL and strip a trailing chat/completions suffix."""
    base = (base_url or "").strip().rstrip("/")
    if not base:
        raise ValueError("請輸入 Server URL。")
    if base.endswith("/chat/completions"):
        return base[: -len("/chat/completions")]
    return base

def call_openai_compatible_chat_completion(messages, model, api_key, base_url, **kwargs):
    """Call an OpenAI-compatible Chat Completions endpoint and return response text."""
    if not api_key:
        raise ValueError("請輸入 API Key。")
    if not model:
        raise ValueError("請輸入模型名稱。")

    endpoint = f"{_normalize_base_url(base_url)}/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": kwargs.get("max_tokens", 8192),
        "temperature": kwargs.get("temperature", 0.7),
    }
    req = urllib_request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + api_key,
        },
        method="POST",
    )
    try:
        with urllib_request.urlopen(req, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib_error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="ignore")
        if e.code == 429:
            raise RateLimitError("已達 API 配額上限，請稍後再試或更換模型。") from e
        raise Exception(f"調用自訂 LLM 服務失敗（HTTP {e.code}）：{raw}") from e
    except urllib_error.URLError as e:
        raise Exception(f"無法連線到自訂 LLM 服務：{e.reason}") from e

    choices = data.get("choices") or []
    if not choices:
        raise Exception("自訂 LLM 服務未返回有效內容。")
    content = ((choices[0] or {}).get("message") or {}).get("content", "")
    text = _extract_message_text(content)
    if not text:
        raise Exception("自訂 LLM 服務返回空白內容。")
    return text

def request_ai_completion(messages, model, provider, api_key, base_url=None, **kwargs):
    """Route completion requests to the selected provider implementation."""
    if provider == PROVIDER_CEREBRAS:
        client = CerebrasClient(api_key=api_key)
        response = client.get_chat_completion(messages=messages, model=model, **kwargs)
        return response.choices[0].message.content
    if provider == PROVIDER_OPENAI_COMPATIBLE:
        return call_openai_compatible_chat_completion(
            messages=messages,
            model=model,
            api_key=api_key,
            base_url=base_url,
            **kwargs,
        )
    raise ValueError(f"不支援的 LLM 服務類型：{provider}")

def format_qimen_results_for_prompt(q, gz_str, jq_str, lunar_info, paipan_info, is_shijia, y, m, d, h, minute):
    """Format Qi Men Dun Jia chart data into a text prompt for AI analysis."""
    eg_keys = list("巽離坤震兌艮坎乾")
    lines = [
        "以下是奇門遁甲排盤的計算結果，請根據這些數據提供詳細的分析和解釋：",
        f"日期時間：{y}年{m}月{d}日 {h}時{minute}分",
        f"起盤方式：{'時家奇門' if is_shijia else '刻家奇門'} | 排盤方式：{paipan_info}",
        f"干支：{q.get('干支', '')}",
        f"排局：{q.get('排局', '')}",
        f"節氣：{jq_str}",
        f"農曆：{lunar_info}",
    ]
    zfzs = q.get("值符值使", {})
    if zfzs:
        zf = zfzs.get("值符星宮", ["", ""])
        zs = zfzs.get("值使門宮", ["", ""])
        if len(zf) > 1:
            lines.append(f"值符星宮：天{zf[1]}宮")
        if len(zs) > 1:
            lines.append(f"值使門宮：{zs[0]}門{zs[1]}宮")

    lines.append(f"\n旬首：{q.get('旬首', '')}")

    lines.append("\n【九宮盤局】")
    for gua in eg_keys:
        dp = q.get("地盤", {}).get(gua, "")
        tp = q.get("天盤", {}).get(gua, "")
        shen = q.get("神", {}).get(gua, "")
        men = q.get("門", {}).get(gua, "")
        xing = q.get("星", {}).get(gua, "")
        lines.append(f"  {gua}宮：地盤={dp}，天盤={tp}，九星={xing}，八門={men}，八神={shen}")
    lines.append(f"  中宮：地盤={q.get('地盤', {}).get('中', '')}")

    return "\n\n".join(lines)

# ------------------- 頁面設定 -------------------
st.set_page_config(page_title="堅奇門 - 奇門排盤", page_icon="🧮", layout="wide")

# ------------------- 固定聊天區域 CSS -------------------
st.markdown("""
<style>
    /* Add padding at bottom so main content is not hidden behind the fixed chat input */
    .stMainBlockContainer {
        padding-bottom: 120px !important;
    }

    /* Ensure the fixed bottom area has a solid background */
    section[data-testid="stBottom"] {
        background-color: var(--background-color, #1A1C23);
        border-top: 1px solid rgba(128, 128, 128, 0.2);
    }
    section[data-testid="stBottom"] > div {
        background-color: var(--background-color, #1A1C23);
    }
</style>
""", unsafe_allow_html=True)

pan, example, guji, log, links = st.tabs(['🧮 排盤', '📜 案例', '📚 古籍', '🆕 更新', '🔗 連結'])

with example:
    st.subheader("📜 案例")
    st.info("案例內容即將更新，敬請期待。")

with guji:
    st.markdown(load_local_md("docs/guji.md"), unsafe_allow_html=True)

with log:
    st.markdown(load_local_md("docs/log.md"), unsafe_allow_html=True)

with links:
    st.subheader("🔗 相關連結")
    st.markdown("""
- 💬 [Telegram 討論群](https://t.me/haizhonggum)
- 🐛 [GitHub Issues](https://github.com/kentang2017/kinqimen/issues)
- 📦 [PyPI - kinqimen](https://pypi.org/project/kinqimen/)
- ☕ [支持作者 (PayPal)](https://www.paypal.me/kinyeah)
""")

# ------------------- 側邊欄 -------------------
with st.sidebar:
    pp_date = st.date_input("日期", pdlm.now(tz='Asia/Shanghai').date())
    pp_time = st.text_input('時間 (如 18:30)', '')
    method = st.selectbox('起盤方式', ('時家奇門', '刻家奇門'))
    paipan = st.selectbox('排盤方式', ('置閏', '拆補'))
    manual = st.button('手動起盤')
    instant = st.button('即時起盤')

    is_shijia = method == '時家奇門'
    pai = 2 if paipan == '置閏' else 1   # 1=拆補 2=置閏

    # ------------------- AI 設置 -------------------
    st.markdown("---")
    st.header("🤖 AI設置")

    llm_provider = st.selectbox(
        "LLM 服務",
        options=[PROVIDER_CEREBRAS, PROVIDER_OPENAI_COMPATIBLE],
        format_func=lambda p: PROVIDER_LABELS.get(p, p),
        index=0,
        key="llm_provider_selector",
    )

    if llm_provider == PROVIDER_CEREBRAS:
        cerebras_default_key = st.secrets.get("CEREBRAS_API_KEY", "") or os.getenv("CEREBRAS_API_KEY", "")
        llm_api_key = st.text_input(
            "Cerebras API Key",
            value=cerebras_default_key,
            type="password",
            key="cerebras_api_key_input",
            help="可留空使用 .streamlit/secrets.toml 或環境變數 CEREBRAS_API_KEY。",
        )
        selected_model = st.selectbox(
            "Cerebras 免費模型",
            options=CEREBRAS_FREE_MODEL_OPTIONS,
            index=0,
            key="cerebras_model_selector",
            help="\n".join(f"• {k}: {v}" for k, v in CEREBRAS_MODEL_DESCRIPTIONS.items()),
        )
        custom_cerebras_model = st.text_input(
            "自訂 Cerebras 模型（可選）",
            value="",
            key="custom_cerebras_model_input",
            placeholder="例如：qwen-3-235b-a22b-instruct-2507",
        )
        selected_model = custom_cerebras_model.strip() or selected_model
        llm_server = None
    else:
        llm_api_key = st.text_input(
            "API Key",
            value=st.secrets.get("OPENAI_API_KEY", "") or os.getenv("OPENAI_API_KEY", ""),
            type="password",
            key="custom_llm_api_key_input",
        )
        selected_model = st.text_input(
            "模型名稱",
            value=st.secrets.get("OPENAI_MODEL", "") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            key="custom_llm_model_input",
            placeholder="例如：gpt-4.1-mini / qwen-plus / deepseek-chat",
        )
        llm_server = st.text_input(
            "Server URL",
            value=st.secrets.get("OPENAI_BASE_URL", "") or os.getenv("OPENAI_BASE_URL", DEFAULT_OPENAI_COMPATIBLE_SERVER),
            key="custom_llm_server_input",
            placeholder="例如：https://api.openai.com/v1",
            help="需為 OpenAI Chat Completions 相容 API。",
        )

    system_prompts_data = load_system_prompts()
    prompts_list = system_prompts_data.get("prompts", [])
    prompt_names = [p["name"] for p in prompts_list]
    selected_prompt = system_prompts_data.get("selected")

    if prompt_names:
        selected_index = 0
        if selected_prompt in prompt_names:
            selected_index = prompt_names.index(selected_prompt)

        selected_name = st.selectbox(
            "選擇系統提示",
            options=prompt_names,
            index=selected_index,
            key="qimen_system_prompt_selector",
            help="選擇用於AI模型的系統提示，指導其分析奇門遁甲排盤結果",
        )

        system_prompts_data["selected"] = selected_name

        selected_content = ""
        for prompt in prompts_list:
            if prompt["name"] == selected_name:
                selected_content = prompt["content"]
                break

        if "qimen_system_prompt" not in st.session_state:
            st.session_state.qimen_system_prompt = selected_content
        elif selected_name != st.session_state.get("last_selected_qimen_prompt"):
            st.session_state.qimen_system_prompt = selected_content

        st.session_state.last_selected_qimen_prompt = selected_name

        new_content = st.text_area(
            "編輯系統提示",
            value=st.session_state.qimen_system_prompt,
            height=150,
            placeholder="範例：你是一位奇門遁甲專家，根據排盤數據提供詳細分析...",
            key="qimen_system_editor",
        )
        st.session_state.qimen_system_prompt = new_content

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 更新提示", key="update_qimen_prompt_button"):
                for prompt in prompts_list:
                    if prompt["name"] == selected_name:
                        prompt["content"] = new_content
                        break
                if save_system_prompts(system_prompts_data):
                    st.toast(f"已更新提示：{selected_name}")
        with col2:
            if st.button("🗑️ 刪除提示", key="delete_qimen_prompt_button",
                         disabled=len(prompts_list) <= 1):
                prompts_list = [p for p in prompts_list if p["name"] != selected_name]
                system_prompts_data["prompts"] = prompts_list
                if selected_name == selected_prompt and prompts_list:
                    system_prompts_data["selected"] = prompts_list[0]["name"]
                if save_system_prompts(system_prompts_data):
                    st.toast(f"已刪除提示：{selected_name}")
                    st.rerun()

    if "qimen_form_key_suffix" not in st.session_state:
        st.session_state.qimen_form_key_suffix = 0

    name_key = f"new_qimen_prompt_name_{st.session_state.qimen_form_key_suffix}"
    content_key = f"new_qimen_prompt_content_{st.session_state.qimen_form_key_suffix}"

    with st.expander("➕ 新增系統提示", expanded=False):
        new_prompt_name = st.text_input("提示名稱", key=name_key)
        new_prompt_content = st.text_area(
            "提示內容",
            height=100,
            placeholder="輸入AI分析指令...",
            key=content_key,
        )
        if st.button("新增提示", key="add_qimen_prompt_button",
                     disabled=not new_prompt_name or not new_prompt_content):
            if new_prompt_name in prompt_names:
                st.error(f"提示名稱「{new_prompt_name}」已存在")
            else:
                prompts_list.append({"name": new_prompt_name, "content": new_prompt_content})
                system_prompts_data["prompts"] = prompts_list
                if save_system_prompts(system_prompts_data):
                    st.session_state.qimen_form_key_suffix += 1
                    st.toast(f"已新增提示：{new_prompt_name}")
                    st.rerun()

    if st.toggle("⚙️ 進階設置", key="qimen_advanced_settings_toggle"):
        st.session_state.qimen_max_tokens = st.slider(
            "最大 Tokens",
            1024, 32768,
            st.session_state.get("qimen_max_tokens", 8192),
            step=1024,
            key="qimen_max_tokens_slider",
            help="控制AI回應的最大長度（較低的值可減少配額消耗）",
        )
        st.session_state.qimen_temperature = st.slider(
            "Temperature",
            0.0, 1.5,
            st.session_state.get("qimen_temperature", 0.7),
            step=0.05,
            key="qimen_temperature_slider",
            help="控制AI回應的創造性（0=精確，1.5=高創造性）",
        )

# ------------------- 共用函數 -------------------
eg = list("巽離坤震兌艮坎乾")

# ------------------- 閉六戊法 SVG 產生器 -------------------
_LIUYI_TO_XUN = {
    "戊": "甲子", "己": "甲戌", "庚": "甲申",
    "辛": "甲午", "壬": "甲辰", "癸": "甲寅",
}
_SIXWU_POS = {
    "甲子": "辰", "甲戌": "寅", "甲申": "子",
    "甲午": "戌", "甲辰": "申", "甲寅": "午",
}
_BRANCH_TO_GONG = {
    "子": "坎", "丑": "艮", "寅": "艮", "卯": "震",
    "辰": "巽", "巳": "巽", "午": "離", "未": "坤",
    "申": "坤", "酉": "兌", "戌": "乾", "亥": "乾",
}

def generate_closed_sixwu_svg(xun_head: str, version: str = "演義版") -> str:
    """回傳完整的 SVG 字串 for 真人閉六戊法圓形十二地支圈。

    Args:
        xun_head: 當前旬首，如 "甲子"、"甲戌" 等六個甲XX旬之一。
        version: "演義版" 為逆布連土；"寶鑑版" 為順布連土。

    Returns:
        完整的 SVG XML 字串，可直接嵌入 HTML / st.markdown。
    """
    wu_branch = _SIXWU_POS.get(xun_head, "子")

    dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    yang_set = {"子", "寅", "辰", "午", "申", "戌"}
    yang_cw = ["子", "寅", "辰", "午", "申", "戌"]  # 六陽支順時針排序

    cx, cy, r, node_r = 250, 250, 175, 22

    positions = {}
    for i, dz in enumerate(dizhi):
        angle = math.radians(i * 30)
        positions[dz] = (cx + r * math.sin(angle), cy - r * math.cos(angle))

    start_idx = yang_cw.index(wu_branch)
    if version == "演義版":
        path_order = [yang_cw[(start_idx - i) % 6] for i in range(7)]
    else:
        path_order = [yang_cw[(start_idx + i) % 6] for i in range(7)]

    def shorten(x1, y1, x2, y2, m=node_r + 6):
        """Shorten a segment by margin m from both ends to avoid overlapping nodes."""
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        if d == 0:
            return x1, y1, x2, y2
        return x1 + dx / d * m, y1 + dy / d * m, x2 - dx / d * m, y2 - dy / d * m

    arrows = []
    for i in range(6):
        p1 = positions[path_order[i]]
        p2 = positions[path_order[i + 1]]
        x1, y1, x2, y2 = shorten(*p1, *p2)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        d = math.sqrt(dx * dx + dy * dy)
        nx, ny = (-dy / d * 13, dx / d * 13) if d > 0 else (0, 0)
        arrows.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#CC3300" stroke-width="3.5" marker-end="url(#arw)" opacity="0.82"/>'
            f'<circle cx="{mx + nx:.1f}" cy="{my + ny:.1f}" r="10" fill="#CC3300" opacity="0.85"/>'
            f'<text x="{mx + nx:.1f}" y="{my + ny + 4.5:.1f}" text-anchor="middle" '
            f'font-size="11" fill="white" font-weight="bold">{i + 1}</text>'
        )

    nodes = []
    for dz in dizhi:
        x, y = positions[dz]
        is_wu = dz == wu_branch
        is_yang = dz in yang_set

        if is_wu:
            fill, stroke, sw = "#FFD700", "#CC0000", 3.5
            tf, fw, fs = "#CC0000", "bold", 18
        elif is_yang:
            fill, stroke, sw = "#DCF0FF", "#3A7CC7", 2.0
            tf, fw, fs = "#1A4A8A", "bold", 18
        else:
            fill, stroke, sw = "#F0F0F0", "#888888", 1.5
            tf, fw, fs = "#555555", "normal", 16

        nodes.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>'
        )
        nodes.append(
            f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" font-size="{fs}" '
            f'fill="{tf}" font-family="serif" font-weight="{fw}">{dz}</text>'
        )

        if is_wu:
            ax = math.atan2(x - cx, -(y - cy))
            ox = cx + (r + node_r + 22) * math.sin(ax)
            oy = cy - (r + node_r + 22) * math.cos(ax)
            nodes.append(
                f'<circle cx="{ox:.1f}" cy="{oy:.1f}" r="16" fill="#CC0000" opacity="0.92"/>'
                f'<text x="{ox:.1f}" y="{oy + 6:.1f}" text-anchor="middle" font-size="19" '
                f'fill="white" font-weight="bold" font-family="serif">戊</text>'
            )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" '
        f'style="width:100%;height:auto;display:block;margin:0 auto">'
        f'<defs>'
        f'<marker id="arw" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="6" markerHeight="6" orient="auto">'
        f'<path d="M0 0 L10 5 L0 10 z" fill="#CC3300"/>'
        f'</marker>'
        f'<radialGradient id="bgg" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" style="stop-color:#FFFDF0"/>'
        f'<stop offset="100%" style="stop-color:#FFF0C8"/>'
        f'</radialGradient>'
        f'</defs>'
        f'<rect width="500" height="500" fill="url(#bgg)" rx="14"/>'
        f'<circle cx="{cx}" cy="{cy}" r="218" fill="none" stroke="#8B6914" '
        f'stroke-width="2.5" opacity="0.35"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#C4A44A" '
        f'stroke-width="1.5" stroke-dasharray="5 4" opacity="0.5"/>'
        f'<circle cx="{cx}" cy="{cy}" r="44" fill="#FFFBF0" stroke="#8B6914" '
        f'stroke-width="1.5" opacity="0.7"/>'
        f'<text x="{cx}" y="{cy - 5}" text-anchor="middle" font-size="14" '
        f'fill="#6B4C11" font-family="serif">六戊</text>'
        f'<text x="{cx}" y="{cy + 13}" text-anchor="middle" font-size="14" '
        f'fill="#6B4C11" font-family="serif">連土</text>'
        f'<text x="{cx}" y="28" text-anchor="middle" font-size="15" fill="#5C3317" '
        f'font-family="serif" font-weight="bold">'
        f'{xun_head}旬・戊在{wu_branch}・{version}</text>'
        f'{"".join(arrows)}'
        f'{"".join(nodes)}'
        f'</svg>'
    )

# Five-element color mapping for 星/神/門/干支 characters
_ELEMENT_COLORS = {
    # 火 (Fire) - red
    '蛇': '#FF4444', '雀': '#FF4444', '景': '#FF4444', '英': '#FF4444',
    '丁': '#FF4444', '丙': '#FF4444', '巳': '#FF4444', '午': '#FF4444',
    # 土 (Earth) - brown
    '勾': '#CD853F', '地': '#CD853F', '生': '#CD853F', '死': '#CD853F',
    '任': '#CD853F', '禽': '#CD853F', '芮': '#CD853F', '己': '#CD853F',
    '戊': '#CD853F', '丑': '#CD853F', '辰': '#CD853F', '未': '#CD853F', '戌': '#CD853F',
    # 木 (Wood) - green
    '合': '#4CAF50', '符': '#4CAF50', '傷': '#4CAF50', '杜': '#4CAF50',
    '輔': '#4CAF50', '沖': '#4CAF50', '乙': '#4CAF50', '甲': '#4CAF50',
    '寅': '#4CAF50', '卯': '#4CAF50',
    # 水 (Water) - blue
    '蓬': '#4499FF', '休': '#4499FF', '玄': '#4499FF', '壬': '#4499FF',
    '癸': '#4499FF', '子': '#4499FF', '亥': '#4499FF',
    # 金 (Metal) - golden
    '天': '#FFB800', '陰': '#FFB800', '虎': '#FFB800', '開': '#FFB800',
    '驚': '#FFB800', '柱': '#FFB800', '心': '#FFB800', '辛': '#FFB800',
    '庚': '#FFB800', '申': '#FFB800', '酉': '#FFB800',
}


def _element_colored_tspan(char: str, default_color: str) -> str:
    """Return an SVG tspan for char with the appropriate five-element color."""
    color = _ELEMENT_COLORS.get(char, default_color)
    return f'<tspan fill="{color}">{char}</tspan>'


def generate_qimen_pan_svg(q: dict, sixwu_gong: str = "") -> str:
    """回傳九宮奇門排盤 SVG，並把閉六戊對應宮位著色。"""
    # Standard Qimen nine-palace layout: South at top (離9), North at bottom (坎1)
    palace_grid = [
        ["巽", "離", "坤"],
        ["震", "中", "兌"],
        ["艮", "坎", "乾"],
    ]
    highlighted_gong = sixwu_gong

    svg_w, svg_h = 720, 720
    cell = 200
    start = 60
    title_y = 30

    cells = []
    for row_idx, row in enumerate(palace_grid):
        for col_idx, gong in enumerate(row):
            x = start + col_idx * cell
            y = start + row_idx * cell
            is_highlight = gong == highlighted_gong and gong != "中"
            fill = "#46330D" if is_highlight else "#152030"
            stroke = "#FFB800" if is_highlight else "#5A7399"
            default_text_color = "#FFE9A8" if is_highlight else "#E8F0FF"

            if gong == "中":
                di_zhong = q.get('地盤', {}).get('中', '')
                title_svg = (
                    f'<tspan fill="{default_text_color}">中宮 | 地盤 </tspan>'
                    f'{_element_colored_tspan(di_zhong, default_text_color)}'
                )
                cells.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="12" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
                )
                cells.append(
                    f'<text x="{x + 16}" y="{y + 34}" font-size="24" '
                    f'font-weight="bold" font-family="sans-serif">{title_svg}</text>'
                )
            else:
                shen_v = q.get('神', {}).get(gong, '')
                men_v  = q.get('門', {}).get(gong, '')
                tian_v = q.get('天盤', {}).get(gong, '')
                xing_v = q.get('星', {}).get(gong, '')
                di_v   = q.get('地盤', {}).get(gong, '')

                line_svgs = [
                    (f'<tspan fill="{default_text_color}">神：</tspan>'
                     f'{_element_colored_tspan(shen_v, default_text_color)}'),
                    (f'<tspan fill="{default_text_color}">門/天：</tspan>'
                     f'{_element_colored_tspan(men_v, default_text_color)}'
                     f'<tspan fill="{default_text_color}"> / </tspan>'
                     f'{_element_colored_tspan(tian_v, default_text_color)}'),
                    (f'<tspan fill="{default_text_color}">星/地：</tspan>'
                     f'{_element_colored_tspan(xing_v, default_text_color)}'
                     f'<tspan fill="{default_text_color}"> / </tspan>'
                     f'{_element_colored_tspan(di_v, default_text_color)}'),
                ]

                cells.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="12" '
                    f'fill="{fill}" stroke="{stroke}" stroke-width="3"/>'
                )
                cells.append(
                    f'<text x="{x + 16}" y="{y + 34}" fill="{default_text_color}" font-size="24" '
                    f'font-weight="bold" font-family="sans-serif">{gong}宮</text>'
                )
                for i, line_svg in enumerate(line_svgs):
                    cells.append(
                        f'<text x="{x + 16}" y="{y + 82 + i * 42}" '
                        f'font-size="28" font-family="sans-serif">{line_svg}</text>'
                    )

    title_svg = ""

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" '
        f'style="width:100%;height:auto;display:block;margin:0 auto;">'
        f'<rect width="{svg_w}" height="{svg_h}" rx="18" fill="#0F1726"/>'
        f'{title_svg}'
        f'{"".join(cells)}'
        f'</svg>'
    )

def render_pan(y, m, d, h, minute, is_shijia=True):
    jq = config.jq(y, m, d, h,minute)

    if is_shijia:
        q = kinqimen.Qimen(y, m, d, h, minute).pan(pai)
    else:
        q = kinqimen.Qimen(y, m, d, h, minute).pan_minute(pai)

    # 提取資料
    zf_xing = q["值符值使"]["值符星宮"][1]
    zm_men  = q["值符值使"]["值使門宮"][0]
    zm_gong = q["值符值使"]["值使門宮"][1]
    xun_head_jiazi = _LIUYI_TO_XUN.get(q.get("旬首", ""), "甲子")
    wu_branch = _SIXWU_POS.get(xun_head_jiazi, "子")
    di_pan = q.get("地盤", {})
    wu_palace = next((gong for gong, val in di_pan.items() if val == "戊"), "")
    pan_svg = generate_qimen_pan_svg(q, wu_palace)
    st.markdown(
        f"**{('時家奇門' if is_shijia else '刻家奇門')}｜{q['排盤方式']}**  \n"
        f"**{y}年{m}月{d}日 {h}時{minute}分**  \n"
        f"{q['干支']}｜{q['排局']}｜節氣：{jq}  \n"
        f"值符星宮：天{zf_xing}宮｜值使門宮：{zm_men}門{zm_gong}宮"
    )
    st.markdown(
        f'<div style="max-width:760px;width:100%;margin:0 auto;padding:8px 0 12px">{pan_svg}</div>',
        unsafe_allow_html=True,
    )

    st.expander("原始資料").write(q)

    # ------------------- 閉六戊法 expander -------------------
    yang_cw = ["子", "寅", "辰", "午", "申", "戌"]
    start_idx = yang_cw.index(wu_branch)

    with st.expander("🔒 真人閉六戊法（法術奇門） - 十二地支圈 SVG 視覺化"):
        version_choice = st.radio(
            "選擇版本",
            ["演義版（逆布連土）", "寶鑑版（順布連土）"],
            horizontal=True,
            key="sixwu_version",
        )
        v = "演義版" if "演義版" in version_choice else "寶鑑版"

        svg_str = generate_closed_sixwu_svg(xun_head_jiazi, v)
        st.markdown(
            f'<div style="max-width:420px;width:100%;margin:0 auto;padding:12px 0">{svg_str}</div>',
            unsafe_allow_html=True,
        )

        if v == "演義版":
            path_order = [yang_cw[(start_idx - i) % 6] for i in range(7)]
            direction_text = "逆布（逆時針依六陽支）"
        else:
            path_order = [yang_cw[(start_idx + i) % 6] for i in range(7)]
            direction_text = "順布（順時針依六陽支）"

        path_text = "→".join(path_order[:6]) + f" → 回{path_order[0]}"

        st.markdown(f"""**📌 本旬六戊位置**：{xun_head_jiazi}旬，戊藏於 **{wu_branch}** 位

**🗺️ 連土路徑（{v} · {direction_text}）**  
{path_text}

---
**🪜 畫地儀式步驟**  
1. **起筆**：由鬼門（艮宮，東北方）起筆，以{path_order[0]}位為起點  
2. **禹步**：{"逆時針" if v == "演義版" else "順時針"}踏行，依序於六陽支（{" → ".join(path_order[:6])}）各落土一撮  
3. **天門留空**：乾宮（西北方）留「天門」不封，以納天氣  
4. **收筆**：回踏{path_order[0]}位，封閉六戊圈

---
**📿 共同主咒**
> 泰山之陽，黃河之陰，天有雷神，地有鬼兵，  
> 六戊封土，萬邪退散，護我{xun_head_jiazi}旬清淨之地，  
> 急急如九天玄女元君律令敕！

---
**⚠️ 注意事項**  
- 翌日必於乾門（西北方）開土散土，勿忘解封  
- 施法期間，施法者不可從乾門（西北）出入，否則法效消散  
- 若無法翌日解封，三日內必解，否則反傷自身
""")

    return q, jq, is_shijia


# 顯示原始 dict

# ------------------- 主畫面 -------------------
with pan:
    st.header('堅奇門排盤')

    # Track chart parameters for AI analysis
    chart_params = {}

    # 即時盤（預設）
    if instant or (not manual and not instant):  # 頁面初載也顯示即時
        now = datetime.datetime.now(pytz.timezone('Asia/Hong_Kong'))
        q_data, jq_str, _shijia = render_pan(now.year, now.month, now.day, now.hour, now.minute, is_shijia=True)
        chart_params = {
            "q": q_data, "jq": jq_str, "is_shijia": _shijia,
            "y": now.year, "m": now.month, "d": now.day,
            "h": now.hour, "minute": now.minute,
        }

    # 手動盤
    if manual and pp_time:
        try:
            h, mnt = map(int, pp_time.split(':'))
            q_data, jq_str, _shijia = render_pan(pp_date.year, pp_date.month, pp_date.day, h, mnt, is_shijia)
            chart_params = {
                "q": q_data, "jq": jq_str, "is_shijia": _shijia,
                "y": pp_date.year, "m": pp_date.month, "d": pp_date.day,
                "h": h, "minute": mnt,
            }
        except Exception:
            st.error("時間格式錯誤，請輸入如 18:30")

    # ------------------- AI 分析按鈕 -------------------
    if chart_params:
        if st.button("🔍 使用AI分析排盤結果", key="analyze_with_ai"):
            with st.spinner("AI正在分析奇門遁甲排盤結果..."):
                if not llm_api_key:
                    st.error("請先在左側 AI 設置填入 API Key。")
                else:
                    try:
                        cp = chart_params
                        lunar_info = config.lunar_date_d(cp["y"], cp["m"], cp["d"]).get("農曆月", "")
                        paipan_info = cp["q"].get("排盤方式", "")
                        qimen_prompt = format_qimen_results_for_prompt(
                            cp["q"], cp["q"].get("干支", ""), cp["jq"],
                            lunar_info, paipan_info, cp["is_shijia"],
                            cp["y"], cp["m"], cp["d"], cp["h"], cp["minute"],
                        )
                        messages = [
                            {"role": "system", "content": st.session_state.get("qimen_system_prompt", "")},
                            {"role": "user", "content": qimen_prompt},
                        ]
                        api_params = {
                            "messages": messages,
                            "model": selected_model,
                            "provider": llm_provider,
                            "api_key": llm_api_key,
                            "base_url": llm_server,
                            "max_tokens": st.session_state.get("qimen_max_tokens", 8192),
                            "temperature": st.session_state.get("qimen_temperature", 0.7),
                        }
                        raw_response = request_ai_completion(**api_params)
                        with st.expander("🤖 AI分析結果", expanded=True):
                            st.markdown(raw_response)
                    except RateLimitError as e:
                        st.error(f"⚠️ {e}")
                    except Exception as e:
                        st.error(f"調用AI時發生錯誤：{e}")


# ------------------- LLM 聊天（固定在頁面底部） -------------------
# --- session state for chat ---
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "chat_expanded" not in st.session_state:
    st.session_state.chat_expanded = False

def _build_chat_system_prompt(chart_params_local):
    """Build the system prompt for the chat, optionally including chart context."""
    base = st.session_state.get("qimen_system_prompt", "你是一位奇門遁甲大師。")
    if chart_params_local:
        cp = chart_params_local
        lunar_data = config.lunar_date_d(cp["y"], cp["m"], cp["d"])
        lunar_info = lunar_data.get("農曆月", "") if lunar_data else ""
        paipan_info = cp["q"].get("排盤方式", "")
        chart_text = format_qimen_results_for_prompt(
            cp["q"], cp["q"].get("干支", ""), cp["jq"],
            lunar_info, paipan_info, cp["is_shijia"],
            cp["y"], cp["m"], cp["d"], cp["h"], cp["minute"],
        )
        return base + "\n\n以下是當前排盤數據供參考：\n" + chart_text
    return base

# --- Fixed chat UI at bottom ---
with st.container():
    col_title, col_toggle, col_clear = st.columns([6, 2, 2])
    with col_title:
        st.markdown("#### 💬 AI 聊天")
    with col_toggle:
        if st.button("📜 展開/收起歷史", key="toggle_chat_history"):
            st.session_state.chat_expanded = not st.session_state.chat_expanded
    with col_clear:
        if st.button("🗑️ 清除對話", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()

# Show chat history in a scrollable container
if st.session_state.chat_expanded and st.session_state.chat_messages:
    history_container = st.container(height=300)
    with history_container:
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

# Chat input (at root level, auto-pins to bottom of viewport)
user_input = st.chat_input("輸入問題，向AI諮詢奇門遁甲...", key="chat_input")
if user_input:
    st.session_state.chat_messages.append({"role": "user", "content": user_input})
    # Auto-expand history when a message is sent
    st.session_state.chat_expanded = True

    if not llm_api_key:
        st.error("請先在左側 AI 設置填入 API Key。")
    else:
        try:
            system_prompt = _build_chat_system_prompt(chart_params or None)

            api_messages = [{"role": "system", "content": system_prompt}]
            # Include recent conversation history (last 20 messages to stay within token limits)
            for msg in st.session_state.chat_messages[-20:]:
                api_messages.append({"role": msg["role"], "content": msg["content"]})

            with st.spinner("AI 思考中..."):
                assistant_reply = request_ai_completion(
                    messages=api_messages,
                    model=selected_model,
                    provider=llm_provider,
                    api_key=llm_api_key,
                    base_url=llm_server,
                    max_tokens=st.session_state.get("qimen_max_tokens", 8192),
                    temperature=st.session_state.get("qimen_temperature", 0.7),
                )

            st.session_state.chat_messages.append({"role": "assistant", "content": assistant_reply})
            st.rerun()
        except RateLimitError as e:
            st.error(f"⚠️ {e}")
        except Exception as e:
            st.error(f"調用AI時發生錯誤：{e}")
