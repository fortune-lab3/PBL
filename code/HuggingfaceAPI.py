# ============================================
# Streamlit × Hugging Face 要約アプリ（文字数指定完全版）
# ============================================
import os
import time
import base64
import streamlit as st
from huggingface_hub import InferenceClient
from httpx import ConnectTimeout, ReadTimeout, HTTPError

# ------------------------------------------------
# 🔑 Hugging Face トークン
# ------------------------------------------------
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "APIkey")
MODEL_ID = "Qwen/Qwen3-4B-Instruct-2507"

# ------------------------------------------------
# ✅ 要約関数（バックエンド）
# ------------------------------------------------
def summarize_api(text: str, target_chars: int, temperature: float = 0.3) -> str:
    """
    target_chars: ユーザー指定の文字数にできるだけ近づける
    """
    if not HF_TOKEN:
        raise RuntimeError("HUGGINGFACEHUB_API_TOKEN が設定されていません。")

    client = InferenceClient(model=MODEL_ID, token=HF_TOKEN, timeout=60.0)

    prompt = (
        f"次の文章を、日本語で、だいたい {target_chars} 文字程度に自然に要約してください。\n"
        f"・出力は必ず日本語のみ\n"
        f"・英語や推論過程（など）を出力しない\n"
        f"・結果だけ簡潔に\n\n"
        f"【文章】\n{text}\n\n【要約】"
    )

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=target_chars,  # 上限もユーザー指定文字数に合わせる
                temperature=temperature,
            )
            summary = resp.choices[0].message["content"].strip()
            return summary

        except (ConnectTimeout, ReadTimeout):
            time.sleep(2 ** attempt)
        except HTTPError as e:
            if getattr(e.response, "status_code", 500) >= 500:
                time.sleep(2 ** attempt)
            else:
                raise

    raise TimeoutError("API の呼び出しに繰り返し失敗しました。")

# ------------------------------------------------
# 📄 ダウンロードリンク生成
# ------------------------------------------------
def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 要約結果をダウンロード</a>'
    return href

# ------------------------------------------------
# 🎨 Streamlit UI
# ------------------------------------------------
def main():
    st.title("📝 日本語要約アプリ（文字数完全指定版）")

    option = st.radio("入力方法を選択してください", ("テキスト入力", "ファイルアップロード"))
    text = ""

    if option == "テキスト入力":
        text = st.text_area("テキストを入力してください", height=200)
    else:
        uploaded_file = st.file_uploader("ファイルを選択してください（txt, md, pdf など）")
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")
            st.success("ファイルを読み込みました")

    # 完全自由入力で文字数指定
    target_chars = st.number_input(
        "出力文字数（文字数指定）",
        value=200,
        step=1,
        format="%d"
    )

    if st.button("要約する"):
        if not text.strip():
            st.warning("テキストを入力してください")
            return

        with st.spinner("要約中です..."):
            try:
                summary = summarize_api(text, target_chars=target_chars)
                st.success("✅ 要約が完了しました！")

                # 結果表示＋文字数表示
                st.text_area("要約結果", summary, height=200)
                st.markdown(f"**要約文字数:** {len(summary)} 文字")

                st.markdown(create_download_link(summary, "summary.txt"), unsafe_allow_html=True)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

# ------------------------------------------------
# 実行
# ------------------------------------------------
if __name__ == "__main__":
    main()
