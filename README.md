# Django-Library-Time-Logging-Webapp（図書室時間記録webアプリ）

## 概要
私の在籍してる大学学部の図書室で使用する、入退室の時間を記録するとともに、司書の方がそのデータを保存したり、分析したりすることを支援するシステムである。

## 目的
目的は以下の通りである。
- 従来、紙で記録していたものをWebアプリ化することで、素早い入退室の時間記録を可能にする
- 今まで管理者が紙のデータを手動でPCに打ち直していた時間を大幅に短縮する
- データ分析を支援する

## システム構成
![システム構成](README/sys.png)

## ファイル構成
```
library_time_log/
├── time_log/
│   ├── accounts/
│   │   ├── templates/
│   │   │   ├── accounts/
│   │   │   │   └── user_page.html
│   │   │   └── registration/
│   │   │       ├── login.html
│   │   │       └── signup.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── management/
│   │   ├── templates/
│   │   │   └── management/
│   │   │       ├── analysis.html
│   │   │       ├── index.html
│   │   │       ├── lsit.html
│   │   │       └── download.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── style_manager.css
│   │   │   └── style.css
│   │   ├── img/
│   │   │   ├── barchart.png
│   │   │   ├── download.png
│   │   │   ├── home.png
│   │   │   ├── icon.png
│   │   │   ├── list.png
│   │   │   ├── logout.png
│   │   │   └── user.png
│   │   ├── js/
│   │   │   └── script.js
│   ├── templates/
│   │   ├── base_manager.html
│   │   └── base.html
│   ├── time_log/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── settings.py
├── time_logging/
│   ├── templates/
│   │   └── time_logging/
│   │       ├── exit_do.html
│   │       ├── exit.html
│   │       ├── forms.html
│   │       ├── index.html
│   │       ├── message.html
│   │       └── use.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── manage.py
└── README.md
```
## テスト環境
- Google Chrome
- FireFox

## 使用方法
想定している使用方法は以下の通りである。
- 従来の紙が置いてある部分にPCやタブレットを置いてもらい、そこで使用する
- サーバー側で、パスワードや、IPアドレス、MACアドレスによるホワイトリスト認証によるアクセス制限

## 実際の画像
ホーム画面
![実際の画像](README/1.png)
入室時間記録画面
![実際の画像](README/2.png)
退室時間記録画面
![実際の画像](README/3.png)
管理者ホーム画面
![実際の画像](README/4.png)
データ分析画面
![実際の画像](README/5.png)
データ分析画面
![実際の画像](README/6.png)
データ可視化
![実際の画像](README/7.png)
データの保存
![実際の画像](README/8.png)
アプリロゴ（フッター画像）
![実際の画像](README/9.png)
