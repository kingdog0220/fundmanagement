# fundmanagement

 
資産管理を行うツール。

Pythonの学習を主目的としており、かつ自分用に使用できる便利ツールとして開発。
 
## 簡単な説明
 
投資信託の基本情報（商品名や基準価額、純資産など）をWebから取得する。

自分が保持している銀行や証券の口座残高や損益などをWebから取得する。

取得した情報をGoogleSpreadSheetに書き込む。


## 必要要件
 
私の開発環境など。バージョンは厳密ではないです。
- Windows 10
- Python (3.9.5)
- GoogleChrome(Latest)

ライブラリはrequirements.txt を参照。

仮想環境はvenv を使用。


## インストール
 
https://github.com/kingdog0220/fundmanagement

タグ付けしたソース

https://github.com/kingdog0220/fundmanagement/tags
 
## 使い方
 
1 .env.sampleを編集し、.envにファイル名を変更する。

2 fundmanagement.bat を実行。

fundmanagement.batはvenv の仮想環境をアクティベイトし、処理が終わったら仮想環境を抜けるbatファイル。
 
## テスト
 
unittest を使用しています。

 
## その他
 
Seleniumによるブラウザの自動操作、BeautifulSoupを使用したスクレイピング、GoogleSpreadSheetの操作、unitttest などpythonの標準的かつ利用者の多い技術を使用した実装をしています。

あくまで私の学習が主目的なので他者がこのツールをそのまま使用することはできませんが、初学者などの参考にはなりえるとは思います。
 
## 作者
 
kingdog

mail to: kingdog0220@gmail.com
 
## ライセンス
 
ご自由に