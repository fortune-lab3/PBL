import os, time, re, base64, io
import streamlit as st
import google.generativeai as genai
from docx import Document

# ==============================
# Gemini 設定
# ==============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_ID = "models/gemini-2.5-flash-lite"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ==============================
# CSS / 画像
# ==============================
def load_css(path: str):
    with open(path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def load_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo_light = load_base64_image("img/logo_black.PNG")
logo_dark  = load_base64_image("img/logo_white.PNG")

# ==============================
# セッション
# ==============================
def init_session_state():
    st.session_state.setdefault("current_ad", "")
    st.session_state.setdefault("edited_ad", "")
    st.session_state.setdefault("current_char_count", 0)

# ==============================
# 前後処理
# ==============================
def preprocess(text: str) -> str:
    pattern = re.compile(r'【.*?】|[ＲR][ー-]\d+|■|＊')
    return pattern.sub('', text or "")

def postprocess(text: str) -> str:
    return (text or "").strip().replace("\n", "").replace("\r", "")

def count(text: str) -> int:
    return len((text or "").replace("\n", "").replace("\r", ""))

def realtime_count():
    st.session_state["current_char_count"] = count(
        st.session_state.get("edited_ad", "")
    )

# ==============================
# 保存
# ==============================
def save_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# ==============================
# Gemini 呼び出し
# ==============================
def gemini_chat(prompt, temperature=0.2, max_tokens=512):
    model = genai.GenerativeModel(
        MODEL_ID,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        },
    )
    res = model.generate_content(prompt)
    return res.text.strip()

# ==============================
# キーワード / トーン
# ==============================
def split_keywords(keywords: str):
    return [w for w in re.split(r"[ 　]+", keywords.strip()) if w]

def build_keyword(keywords: str):
    words = split_keywords(keywords)
    if not words:
        return ""
    return (
        f"・キーワード指定: { '、'.join(words) }\n"
        "・各キーワードは文章中に絶対に1回だけ\n"
        "・キーワードが文の繋がりを邪魔しないよう、自然に組み込んでください。\n"
    )

def build_tone(tone: str) -> str:
    if tone == "やわらかい":
        return (
            "・漢語（熟語）を避け、和語（訓読みの言葉）を優先して使うこと\n"
            "・ひらがなの比率を上げ、見た目の威圧感をなくすこと\n"
            "・専門用語や難しい概念は、身近な例えに置き換えること\n"
        )
    return ""

# ==============================
# 文字数調整
# ==============================
def adjust_length(ad, target_length, tone):
    ad = postprocess(ad)

    for _ in range(2):
        diff = target_length - len(ad)
        if abs(diff) <= 5 and ad.endswith("。"):
            return ad

        cmd = "補ってください" if diff > 0 else "削ってください"

        prompt = (
            "次の文章の意味と構成をできるだけ変えずに、"
            "文字数だけを調整してください。\n"
            f"{tone}"
            f"現在 {len(ad)}文字 → {target_length}文字に{cmd}\n"
            "生成文のみを出力してください。\n\n"
            f"【元の文章】{ad}"
        )

        ad = postprocess(
            gemini_chat(prompt, temperature=0.1, max_tokens=int(target_length * 1.2))
        )

    return ad

# ==============================
# 広告生成
# ==============================
def generate_advertisement(text, target_length, keywords, tone, temperature=0.2):
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY が設定されていません。")

    cleaned = preprocess(text)
    tone_txt = build_tone(tone)
    keyword_txt = build_keyword(keywords)

    prompt = (
        f"次の原稿をもとに、新聞のラテ欄風の広告文を書いてください。\n"
        f"文字数は日本語でちょうど {target_length} 文字\n"
        f"次にある文体ルールを厳密に守ってください。\n"
        f"・文の主語・場所・行動が明確になるように書くこと\n"
        f"・文末には視聴者の興味を引くフックを必ず入れる\n"
        f"・感情やインパクトのある言葉を使う\n"
        f"・季節感やテーマがあれば冒頭に入れる\n"
        f"・応募やプレゼントキャンペーンについては書かない\n"
        f"【条件】日本語のみ・改行なし\n"
        f"{tone_txt}"
        f"{keyword_txt}\n"
        f"文字数が {target_length} ±5 の範囲に入っていない場合は、文章を修正して再生成してください。\n"
        f"【原稿】\n{cleaned}\n\n【広告文】"
    )

    ad = gemini_chat(
        prompt,
        temperature=temperature,
        max_tokens=int(target_length * 1.5),
    )

    ad = postprocess(ad)
    #ad = adjust_length(ad, target_length, tone_txt)
    return ad

# ==============================
# Streamlit UI
# ==============================
def main():
    st.set_page_config(page_title="南海ことば工房", page_icon="img/favicon.JPG")
    load_css("style.css")
    init_session_state()

    st.markdown(
        f'<div class="logo-container">'
        f'<img src="data:image/png;base64,{logo_light}" class="logo-light">'
        f'<img src="data:image/png;base64,{logo_dark}" class="logo-dark">'
        f'</div>',
        unsafe_allow_html=True,
    )

    option = st.sidebar.radio("入力方法を選択", ("テキスト", "ファイル"))
    text = ""

    if option == "テキスト":
        text = st.text_area("広告文にしたい原稿を入力してください", height=260)
        text = re.sub(r"\s+", " ", text.strip())

    else:
        uploadfile = st.file_uploader("ファイルを選択", type=["txt", "docx"])
        if uploadfile:
            if uploadfile.name.endswith(".txt"):
                text = uploadfile.read().decode("utf-8", errors="ignore")
            else:
                doc = Document(uploadfile)
                text = "\n".join(p.text for p in doc.paragraphs)

    target_length = st.sidebar.number_input("文字数", 10, 500, 100)
    tone = st.sidebar.radio("文章のスタイル", ["かたい", "やわらかい"], horizontal=True)
    keywords = st.sidebar.text_input("キーワード指定（スペース区切り）")

    filename = st.sidebar.text_input("保存するファイル名", "newspaper")
    ext = st.sidebar.radio("保存形式", [".txt", ".docx"], horizontal=True)

    if st.button("広告文を生成"):
        with st.spinner("広告文を生成中..."):
            ad = generate_advertisement(text, target_length, keywords, tone)
            st.session_state["current_ad"] = ad
            st.session_state["edited_ad"] = ad
            st.session_state["current_char_count"] = len(ad)

    if st.session_state["current_ad"]:
        st.text_area("生成結果", key="edited_ad", on_change=realtime_count, height=200)
        st.markdown(f"文字数：{st.session_state['current_char_count']} 文字")

        data = (
            save_docx(st.session_state["edited_ad"])
            if ext == ".docx"
            else st.session_state["edited_ad"]
        )

        st.download_button(
            "ダウンロード",
            data,
            file_name=filename + ext,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            if ext == ".docx"
            else "text/plain",
        )

if __name__ == "__main__":
    main()
