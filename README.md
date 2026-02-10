# 目次
- [はじめに](#はじめに)
- [環境設定](#環境設定)
   - [GitHub](#githubについて)
   - [Hugging Face](#hugging-face-について)
   - [Streamlitshare](#streamlit-cloud-について)
- [利用方法](#利用方法)
   - [アプリの利用](#アプリの利用について)
   - [APIキーと利用制限](#APIキーと利用制限について)

# はじめに
このアプリは、南海放送のTV番組のナレーション原稿から、新聞に掲載するTV番組の広告文を生成するものである  

# 環境設定
## GitHubについて
### アカウント作成
1. [GitHub](https://github.com)のサイトへアクセス
2. 右上の `Sign up` をクリック
3. メールアドレス、パスワード、ユーザーネームなどを入力し、`Create account` ボタンをクリックしてアカウントを作成

### リポジトリをコピー
1. [GitHub](https://github.com/fortune-lab3/PBL/)にアクセス
2. 右上の `Fork` ボタンをクリック
3. 右下の緑色 `Create Fork` ボタンをクリックして自分のリポジトリにコピー

## Hugging Face について
### アカウント作成
1. [Hugging Face](https://huggingface.co)のサイトへアクセス
2. 右上の `Sign Up` ボタンをクリック
3. メールアドレス、パスワード、ユーザーネームを入力してアカウントを作成

### Hugging Face APIキーを取得
1. [Hugging Face](https://huggingface.co)にログイン
2. 右上の丸いアイコンをクリックし、`Settings` ボタンをクリック
3. 左側にある `Access Tokens` をクリック
4. 右上にある `+ Create new token` をクリック
5. Token type を `Read` にして Token name に任意の名前を入力
6. `Create token` ボタンをクリックしてAPIキーを作成
7. 表示される `hf_` からはじまるAPIキーをコピー（このときにしか表示されないので絶対にコピーしておく）
8. APIキーは絶対に外部に公開しない

## Streamlit Cloud について
### アカウント作成
1. [Streamlit Cloud](https://share.streamlit.io/)にアクセス
2. `Continue to sign-in` ボタンをクリック
3. `GitHubで続行` を選択し、連携を許可

### アプリを作成
1. [share.streamlit](https://share.streamlit.io/)にアクセス
2. 右上の `Create app` をクリック
3. `Deploy a public app from GitHub` を選択
4. Repositoryに `アカウント名/PBL`、Branchに `main`、Main file pathに `app.py` を選択（枠をクリックすると候補がでてきます）
5. App URLに任意の名前を入力（これがアプリのURLになります）
6. `Deploy` をクリックしてアプリを作成

### APIキー設定
1. [share.streamlit](https://share.streamlit.io/)にアクセス
2. 作成したアプリ（pbl・main・app.py）の右端にある︙をクリックし、`Settings` をクリック
3. 左側にある `Secrets` をクリック
4. 枠の中に以下を入力（`""` の間に、先ほど取得してコピーしたAPIキーを貼り付け）
   ```text
   HUGGINGFACEHUB_API_TOKEN = "取得したAPIキー"
5. 右下の `Save changes` をクリックして保存
6. これで、作成したアプリ（pbl・main・app.py）をクリックすると使えます
7. 一定期間アクセスしなかったらアプリがスリープ状態になるので、表示される `Yes, get this app back up!` ボタンをクリックして少し待てば起動します

# 利用方法
## アプリの利用について
左側のサイドバーで詳細設定を行い、原稿を入力して `広告文を生成` ボタンを押すと、数秒で広告文と文字数が表示される  
テキストボックスに入力した際、右下に小さく `Press Enter to apply` や `Press Ctrl+Enter to apply` と表示されるので、指示に従って入力内容を確定する  
出力された広告文は手動で編集することが可能である  
編集後に **Ctrl+Enter** を押すと、文字数表示も更新される  
ダウンロードボタンを押すと、選択したファイル形式および指定したファイル名で、広告文を保存することができる  

## APIキーと利用制限について
[Huggingface](https://huggingface.co/settings/inference-providers/overview)の `Inference Providers` のページにて、APIキーの利用状況を確認することができる  
無料利用枠には使用回数やトークン数の制限があり、基本的には毎月1日の9時にリセットされる  
ただし利用状況やシステムの都合により、1日後や1週間後に再度利用可能となる場合もある  
利用上限に達した場合の対応として、別のメールアドレスでHuggingfaceのアカウントを新規作成し、APIキーを取得するという方法がある  
