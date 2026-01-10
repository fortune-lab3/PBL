# はじめに
このアプリは、南海放送のTV番組のナレーション原稿から新聞に掲載するTV番組の広告文を生成するものである

# HuggingfaceAPIキーについて
## HuggingfaceAPIキーの取得
[Huggingface](https://huggingface.co/)のサイトへアクセス
アカウントの作成、またはサインインを行い、Access Tokensをクリック
右上にある '+ Create new token' をクリック
Token type を Read にして Token name に好きな名前を入力し、Create token をクリックする
表示されたAPIキーをコピー(このときしか表示されないので必ずコピーしてください)

## HuggingfaceAPIキーの設定
[share streamlit](https://share.streamlit.io/)のサイトへアクセス
main/app.py の右端にある︙をクリック
Setting → Secrets の順にクリックして、HUGGINGFACEHUB_API_TOKEN = "" の "" の間にコピーしたAPIキーを貼り付ける
右下にある Save changes をクリック

# 利用方法
[https://nankai-lab.streamlit.app/](https://nankai-lab.streamlit.app/)のサイトにアクセスし、Yes, get this app back up! を押すと表示される
左にあるサイドバーで入力方法を選び、詳細設定ができる
'広告文を生成' ボタンを押すと数秒で広告文が生成され、生成された内容はその場で編集できる
編集した場合は 'Ctrl+Enter' を押すと文字数表示が変化し、ダウンロードする際にも反映される
