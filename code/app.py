import streamlit as st
import base64
import time

def main():
    st.title("要約")
    
    option = st.radio("選択してください", ("テキスト入力", "ファイルアップロード"))
    
    if option == "テキスト入力":
        text_area = st.text_area("テキストを入力してください")
    else:
        uploaded_file = st.file_uploader("ファイルを選択してください")
        if uploaded_file is not None:
            st.write(uploaded_file)
    
    st.selectbox('文字数指定', [100, 200, 300])
        
    if st.button("要約する"):
        with st.spinner('processiong...'):
            time.sleep(3)
            
    output = st.text_area("要約結果")
    st.text("文字数：")
    
def create_download_link(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">要約結果をダウンロード</a>'
    return href    

if __name__ == '__main__':
    main()